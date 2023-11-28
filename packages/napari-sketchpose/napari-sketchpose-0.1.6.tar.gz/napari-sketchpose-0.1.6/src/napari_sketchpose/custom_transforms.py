import mgen
import numpy as np
import warnings
import cv2
import scipy
import torch
import math

import logging

import skimage
from omnipose.core import omnipose_logger, mode_filter, masks_to_flows, diameters
from skimage.filters import gaussian
from skimage.morphology import dilation, disk
from skimage.util import random_noise
from skimage.measure import regionprops

transforms_logger = logging.getLogger(__name__)

from omnipose import utils
import itertools  # ND tiling

# import omnipose, edt, fastremap
# OMNI_INSTALLED = True

try:
    import omnipose, edt, fastremap

    OMNI_INSTALLED = True
except:
    OMNI_INSTALLED = False
    print('OMNIPOSE NOT INSTALLED')
SKIMAGE_ENABLED = True


def _taper_mask(ly=224, lx=224, sig=7.5):
    bsize = max(224, max(ly, lx))
    xm = np.arange(bsize)
    xm = np.abs(xm - xm.mean())
    mask = 1 / (1 + np.exp((xm - (bsize / 2 - 20)) / sig))
    mask = mask * mask[:, np.newaxis]
    mask = mask[bsize // 2 - ly // 2: bsize // 2 + ly // 2 + ly % 2,
           bsize // 2 - lx // 2: bsize // 2 + lx // 2 + lx % 2]
    return mask


def _taper_mask_ND(shape=(224, 224), sig=7.5):
    dim = len(shape)
    bsize = max(shape)
    xm = np.arange(bsize)
    xm = np.abs(xm - xm.mean())
    # 1D distribution
    mask = 1 / (1 + np.exp((xm - (bsize / 2 - 20)) / sig))
    # extend to ND
    for j in range(dim - 1):
        mask = mask * mask[..., np.newaxis]
    slc = tuple([slice(bsize // 2 - s // 2, bsize // 2 + s // 2 + s % 2) for s in shape])
    mask = mask[slc]
    return mask


def unaugment_tiles(y, unet=False):
    """ reverse test-time augmentations for averaging

    Parameters
    ----------

    y: float32
        array that's ntiles_y x ntiles_x x chan x Ly x Lx where chan = (dY, dX, cell prob)

    unet: bool (optional, False)
        whether or not unet output or cellpose output

    Returns
    -------

    y: float32

    """
    for j in range(y.shape[0]):
        for i in range(y.shape[1]):
            if j % 2 == 0 and i % 2 == 1:
                y[j, i] = y[j, i, :, ::-1, :]
                if not unet:
                    y[j, i, 0] *= -1
            elif j % 2 == 1 and i % 2 == 0:
                y[j, i] = y[j, i, :, :, ::-1]
                if not unet:
                    y[j, i, 1] *= -1
            elif j % 2 == 1 and i % 2 == 1:
                y[j, i] = y[j, i, :, ::-1, ::-1]
                if not unet:
                    y[j, i, 0] *= -1
                    y[j, i, 1] *= -1
    return y


def get_flip(idx):
    """
    ND slices for flipping arrays along particular axes
    based on the tile indices. Used in augment_tiles_ND()
    and unaugment_tiles_ND().
    """
    return tuple([slice(None, None, None) if i % 2 else
                  slice(None, None, -1) for i in idx])


def unaugment_tiles_ND(y, inds, unet=False):
    """ reverse test-time augmentations for averaging

    Parameters
    ----------

    y: float32
        array that's ntiles x chan x Ly x Lx where
        chan = (dY, dX, dist, boundary)

    unet: bool (optional, False)
        whether or not unet output or cellpose output

    Returns
    -------

    y: float32

    """
    dim = len(inds[0])

    for i, idx in enumerate(inds):

        # repeat the flip to undo it
        flip = get_flip(idx)

        # flow field componenets need to be flipped
        factor = np.array([1 if i % 2 else -1 for i in idx])

        # apply the flip
        y[i] = y[i][(Ellipsis,) + flip]

        # apply the flow field flip
        if not unet:
            y[i][:dim] = [s * f for s, f in zip(y[i][:dim], factor)]

    return y


def average_tiles(y, ysub, xsub, Ly, Lx):
    """ average results of network over tiles

    Parameters
    -------------

    y: float, [ntiles x nclasses x bsize x bsize]
        output of cellpose network for each tile

    ysub : list
        list of arrays with start and end of tiles in Y of length ntiles

    xsub : list
        list of arrays with start and end of tiles in X of length ntiles

    Ly : int
        size of pre-tiled image in Y (may be larger than original image if
        image size is less than bsize)

    Lx : int
        size of pre-tiled image in X (may be larger than original image if
        image size is less than bsize)

    Returns
    -------------

    yf: float32, [nclasses x Ly x Lx]
        network output averaged over tiles

    """
    Navg = np.zeros((Ly, Lx))
    yf = np.zeros((y.shape[1], Ly, Lx), np.float32)
    # taper edges of tiles
    mask = _taper_mask(ly=y.shape[-2], lx=y.shape[-1])
    for j in range(len(ysub)):
        yf[:, ysub[j][0]:ysub[j][1], xsub[j][0]:xsub[j][1]] += y[j] * mask
        Navg[ysub[j][0]:ysub[j][1], xsub[j][0]:xsub[j][1]] += mask
    yf /= Navg
    return yf


def average_tiles_ND(y, subs, shape):
    """ average results of network over tiles

    Parameters
    -------------

    y: float, [ntiles x nclasses x bsize x bsize]
        output of cellpose network for each tile

    subs : list
        list of slices for each subtile

    shape : int, list or tuple
        shape of pre-tiled image (may be larger than original image if
        image size is less than bsize)

    Returns
    -------------

    yf: float32, [nclasses x Ly x Lx]
        network output averaged over tiles

    """
    Navg = np.zeros(shape)
    yf = np.zeros((y.shape[1],) + shape, np.float32)
    # taper edges of tiles
    mask = _taper_mask_ND(y.shape[-len(shape):])
    for j, slc in enumerate(subs):
        yf[(Ellipsis,) + slc] += y[j] * mask
        Navg[slc] += mask
    yf /= Navg
    return yf


def make_tiles(imgi, bsize=224, augment=False, tile_overlap=0.1):
    """ make tiles of image to run at test-time

    if augmented, tiles are flipped and tile_overlap=2.
        * original
        * flipped vertically
        * flipped horizontally
        * flipped vertically and horizontally

    Parameters
    ----------
    imgi : float32
        array that's nchan x Ly x Lx

    bsize : float (optional, default 224)
        size of tiles

    augment : bool (optional, default False)
        flip tiles and set tile_overlap=2.

    tile_overlap: float (optional, default 0.1)
        fraction of overlap of tiles

    Returns
    -------
    IMG : float32
        array that's ntiles x nchan x bsize x bsize

    ysub : list
        list of arrays with start and end of tiles in Y of length ntiles

    xsub : list
        list of arrays with start and end of tiles in X of length ntiles


    """

    nchan, Ly, Lx = imgi.shape
    if augment:
        bsize = np.int32(bsize)
        # pad if image smaller than bsize
        if Ly < bsize:
            imgi = np.concatenate((imgi, np.zeros((nchan, bsize - Ly, Lx))), axis=1)
            Ly = bsize
        if Lx < bsize:
            imgi = np.concatenate((imgi, np.zeros((nchan, Ly, bsize - Lx))), axis=2)
        Ly, Lx = imgi.shape[-2:]
        # tiles overlap by half of tile size
        ny = max(2, int(np.ceil(2. * Ly / bsize)))
        nx = max(2, int(np.ceil(2. * Lx / bsize)))
        ystart = np.linspace(0, Ly - bsize, ny).astype(int)
        xstart = np.linspace(0, Lx - bsize, nx).astype(int)

        ysub = []
        xsub = []

        # flip tiles so that overlapping segments are processed in rotation
        IMG = np.zeros((len(ystart), len(xstart), nchan, bsize, bsize), np.float32)
        for j in range(len(ystart)):
            for i in range(len(xstart)):
                ysub.append([ystart[j], ystart[j] + bsize])
                xsub.append([xstart[i], xstart[i] + bsize])
                IMG[j, i] = imgi[:, ysub[-1][0]:ysub[-1][1], xsub[-1][0]:xsub[-1][1]]
                # flip tiles to allow for augmentation of overlapping segments
                if j % 2 == 0 and i % 2 == 1:
                    IMG[j, i] = IMG[j, i, :, ::-1, :]
                elif j % 2 == 1 and i % 2 == 0:
                    IMG[j, i] = IMG[j, i, :, :, ::-1]
                elif j % 2 == 1 and i % 2 == 1:
                    IMG[j, i] = IMG[j, i, :, ::-1, ::-1]
    else:
        tile_overlap = min(0.5, max(0.05, tile_overlap))
        bsizeY, bsizeX = min(bsize, Ly), min(bsize, Lx)
        bsizeY = np.int32(bsizeY)
        bsizeX = np.int32(bsizeX)
        # tiles overlap by 10% tile size
        ny = 1 if Ly <= bsize else int(np.ceil((1. + 2 * tile_overlap) * Ly / bsize))
        nx = 1 if Lx <= bsize else int(np.ceil((1. + 2 * tile_overlap) * Lx / bsize))
        ystart = np.linspace(0, Ly - bsizeY, ny).astype(int)
        xstart = np.linspace(0, Lx - bsizeX, nx).astype(int)

        ysub = []
        xsub = []
        IMG = np.zeros((len(ystart), len(xstart), nchan, bsizeY, bsizeX), np.float32)
        for j in range(len(ystart)):
            for i in range(len(xstart)):
                ysub.append([ystart[j], ystart[j] + bsizeY])
                xsub.append([xstart[i], xstart[i] + bsizeX])
                IMG[j, i] = imgi[:, ysub[-1][0]:ysub[-1][1], xsub[-1][0]:xsub[-1][1]]

    return IMG, ysub, xsub, Ly, Lx


def make_tiles_ND(imgi, bsize=224, augment=False, tile_overlap=0.1):
    """ make tiles of image to run at test-time

    if augmented, tiles are flipped and tile_overlap=2.
        * original
        * flipped vertically
        * flipped horizontally
        * flipped vertically and horizontally

    Parameters
    ----------
    imgi : float32
        array that's nchan x Ly x Lx

    bsize : float (optional, default 224)
        size of tiles

    augment : bool (optional, default False)
        flip tiles and set tile_overlap=2.

    tile_overlap: float (optional, default 0.1)
        fraction of overlap of tiles

    Returns
    -------
    IMG : float32
        array that's ntiles x nchan x bsize x bsize

    ysub : list
        list of arrays with start and end of tiles in Y of length ntiles

    xsub : list
        list of arrays with start and end of tiles in X of length ntiles


    """

    nchan = imgi.shape[0]
    shape = imgi.shape[1:]
    dim = len(shape)
    inds = []
    if augment:
        bsize = np.int32(bsize)
        # pad if image smaller than bsize
        pad_seq = [(0, 0)] + [(0, max(0, bsize - s)) for s in shape]
        imgi = np.pad(imgi, pad_seq)
        shape = imgi.shape[-dim:]

        # tiles overlap by half of tile size
        ntyx = [max(2, int(np.ceil(2. * s / bsize))) for s in shape]
        start = [np.linspace(0, s - bsize, n).astype(int) for s, n in zip(shape, ntyx)]

        intervals = [[slice(si, si + bsize) for si in s] for s in start]
        subs = list(itertools.product(*intervals))
        indexes = [np.arange(len(s)) for s in start]
        inds = list(itertools.product(*indexes))

        IMG = []

        # here I flip if the index is odd
        for slc, idx in zip(subs, inds):
            flip = get_flip(idx)  # avoid repetition with unaugment
            IMG.append(imgi[(Ellipsis,) + slc][(Ellipsis,) + flip])

        IMG = np.stack(IMG)
    else:
        tile_overlap = min(0.5, max(0.05, tile_overlap))
        # bsizeY, bsizeX = min(bsize, Ly), min(bsize, Lx)
        # B = [np.int32(min(b,s)) for s,b in zip(im.shape,bsize)] if bzise variable
        bbox = tuple([np.int32(min(bsize, s)) for s in shape])

        # tiles overlap by 10% tile size
        ntyx = [1 if s <= bsize else int(np.ceil((1. + 2 * tile_overlap) * s / bsize))
                for s in shape]
        start = [np.linspace(0, s - b, n).astype(int) for s, b, n in zip(shape, bbox, ntyx)]

        intervals = [[slice(si, si + bsize) for si in s] for s in start]
        subs = list(itertools.product(*intervals))

        # IMG = np.zeros((len(ystart), len(xstart), nchan,  bsizeY, bsizeX), np.float32)
        # IMG = np.zeros(tuple([len(s) for s in start])+(nchan,)+bbox, np.float32)
        IMG = np.stack([imgi[(Ellipsis,) + slc] for slc in subs])

    return IMG, subs, shape, inds


# needs to have a wider range to avoid weird effects with few cells in frame
# also turns out previous formulation can give negative numbers, messes up log operations etc.
def normalize99(Y, lower=0.01, upper=99.99, omni=False):
    """ normalize image so 0.0 is 0.01st percentile and 1.0 is 99.99th percentile """
    if omni and OMNI_INSTALLED:
        X = omnipose.utils.normalize99(Y)
    else:
        X = Y.copy()
        x01 = np.percentile(X, 1)
        x99 = np.percentile(X, 99)
        X = (X - x01) / (x99 - x01)
    return X


def move_axis(img, m_axis=-1, first=True):
    """ move axis m_axis to first or last position """
    if m_axis == -1:
        m_axis = img.ndim - 1
    m_axis = min(img.ndim - 1, m_axis)
    axes = np.arange(0, img.ndim)
    if first:
        axes[1:m_axis + 1] = axes[:m_axis]
        axes[0] = m_axis
    else:
        axes[m_axis:-1] = axes[m_axis + 1:]
        axes[-1] = m_axis
    img = img.transpose(tuple(axes))
    return img


# This was edited to fix a bug where single-channel images of shape (y,x) would be
# transposed to (x,y) if x<y, making the labels no longer correspond to the data.
def move_min_dim(img, force=False):
    """ move minimum dimension last as channels if < 10, or force==True """
    if len(img.shape) > 2:  # only makese sense to do this if channel axis is already present, not best for 3D though!
        min_dim = min(img.shape)
        if min_dim < 10 or force:
            if img.shape[-1] == min_dim:
                channel_axis = -1
            else:
                channel_axis = (img.shape).index(min_dim)
            img = move_axis(img, m_axis=channel_axis, first=False)
    return img


def update_axis(m_axis, to_squeeze, ndim):
    if m_axis == -1:
        m_axis = ndim - 1
    if (to_squeeze == m_axis).sum() == 1:
        m_axis = None
    else:
        inds = np.ones(ndim, bool)
        inds[to_squeeze] = False
        m_axis = np.nonzero(np.arange(0, ndim)[inds] == m_axis)[0]
        if len(m_axis) > 0:
            m_axis = m_axis[0]
        else:
            m_axis = None
    return m_axis


def convert_image(x, channels, channel_axis=None, z_axis=None,
                  do_3D=False, normalize=True, invert=False,
                  nchan=2, dim=2, omni=False):
    """ return image with z first, channels last and normalized intensities """

    # squeeze image, and if channel_axis or z_axis given, transpose image
    if x.ndim > 3:
        to_squeeze = np.array([int(isq) for isq, s in enumerate(x.shape) if s == 1])
        # remove channel axis if number of channels is 1
        if len(to_squeeze) > 0:
            channel_axis = update_axis(channel_axis, to_squeeze, x.ndim) if channel_axis is not None else channel_axis
            z_axis = update_axis(z_axis, to_squeeze, x.ndim) if z_axis is not None else z_axis
        x = x.squeeze()
    # print('shape00',x.shape)
    # put z axis first
    if z_axis is not None and x.ndim > 2:
        x = move_axis(x, m_axis=z_axis, first=True)
        if channel_axis is not None:
            channel_axis += 1
        if x.ndim == 3:
            x = x[..., np.newaxis]
    # print('shape01',x.shape)
    # put channel axis last
    if channel_axis is not None and x.ndim > 2:
        x = move_axis(x, m_axis=channel_axis, first=False)
    elif x.ndim == dim:
        x = x[..., np.newaxis]

    # print('shape02',x.shape)

    if do_3D:
        if x.ndim < 3:
            transforms_logger.critical('ERROR: cannot process 2D images in 3D mode')
            raise ValueError('ERROR: cannot process 2D images in 3D mode')
        elif x.ndim < 4:
            x = x[..., np.newaxis]

    # print('shape03',x.shape)

    # this one must be the cuplrit... no, in fact it is not
    if channel_axis is None:
        x = move_min_dim(x)
        channel_axis = -1  # moves to last

    # print('shape04',x.shape)

    if x.ndim > 3:
        transforms_logger.info('multi-stack tiff read in as having %d planes %d channels' %
                               (x.shape[0], x.shape[-1]))

    if channels is not None:
        channels = channels[0] if len(channels) == 1 else channels
        if len(channels) < 2:
            transforms_logger.critical('ERROR: two channels not specified')
            raise ValueError('ERROR: two channels not specified')
        x = reshape(x, channels=channels, channel_axis=channel_axis)
        # print('AAA',x.shape,channels)
    else:
        # print('BBB',do_3D,x.ndim,x.shape,nchan)
        # code above put channels last, so its making sure nchan matches below
        # not sure when this condition would be met, but it conflicts with 3D
        if x.shape[-1] > nchan and x.ndim > dim:
            transforms_logger.warning(('WARNING: more than %d channels given, use '
                                       '"channels" input for specifying channels -'
                                       'just using first %d channels to run processing') % (nchan, nchan))
            x = x[..., :nchan]

        if not do_3D and x.ndim > 3 and dim == 2:  # error should only be thrown for 2D mode
            transforms_logger.critical('ERROR: cannot process 4D images in 2D mode')
            raise ValueError('ERROR: cannot process 4D images in 2D mode')

        if x.shape[-1] < nchan:
            x = np.concatenate((x,
                                np.tile(np.zeros_like(x), (1, 1, nchan - 1))),
                               axis=-1)

    if normalize or invert:
        x = normalize_img(x, invert=invert, omni=omni)

    return x


def reshape(data, channels=[0, 0], chan_first=False, channel_axis=0):
    """ reshape data using channels

    Parameters
    ----------

    data : numpy array that's (Z x ) Ly x Lx x nchan
        if data.ndim==8 and data.shape[0]<8, assumed to be nchan x Ly x Lx

    channels : list of int of length 2 (optional, default [0,0])
        First element of list is the channel to segment (0=grayscale, 1=red, 2=green, 3=blue).
        Second element of list is the optional nuclear channel (0=none, 1=red, 2=green, 3=blue).
        For instance, to train on grayscale images, input [0,0]. To train on images with cells
        in green and nuclei in blue, input [2,3].

    channel_axis : int, default 0
        the axis that corresponds to channels (usually 0 or -1)

    Returns
    -------
    data : numpy array that's (Z x ) Ly x Lx x nchan (if chan_first==False)

    """
    data = data.astype(np.float32)
    if data.ndim < 3:  # plain 2D images get a new channel azis
        data = data[..., np.newaxis]
    elif data.shape[
        0] < 8 and data.ndim == 3:  # Assume stack of this sort ar nchan x Ly x Lx, so reorder to Ly x Lx x nchan
        data = np.transpose(data, (1, 2, 0))
    # use grayscale image
    if data.shape[-1] == 1:
        data = np.concatenate((data, np.zeros_like(data)), axis=-1)
    else:
        if channels[0] == 0:
            # data = data.mean(axis=-1, keepdims=True) # why do this? Seems like it would be smashing channels together instead of taking the 0th one.
            data = data.mean(axis=channel_axis,
                             keepdims=True)  # also had a big bug: 3D volumes get squashed to 2D along x axis!!! Assumptions bad.

            data = np.concatenate((data, np.zeros_like(data)),
                                  axis=-1)  # forces images to always have 2 channels, possibly bad for multidimensional pytorch limitations
        else:
            chanid = [channels[0] - 1]  # oh so [0,0] would do a mean and [1,0] would actually take the first channel?
            if channels[1] > 0:
                chanid.append(channels[1] - 1)
            data = data[..., chanid]
            for i in range(data.shape[-1]):
                if np.ptp(data[..., i]) == 0.0:
                    if i == 0:
                        warnings.warn("chan to seg' has value range of ZERO")
                    else:
                        warnings.warn("'chan2 (opt)' has value range of ZERO, can instead set chan2 to 0")
            if data.shape[-1] == 1:
                data = np.concatenate((data, np.zeros_like(data)), axis=-1)
    if chan_first:
        if data.ndim == 4:
            data = np.transpose(data, (3, 0, 1, 2))
        else:
            data = np.transpose(data, (2, 0, 1))
    return data


def normalize_img(img, axis=-1, invert=False, omni=False):
    """ normalize each channel of the image so that so that 0.0=1st percentile
    and 1.0=99th percentile of image intensities

    optional inversion

    Parameters
    ------------

    img: ND-array (at least 3 dimensions)

    axis: channel axis to loop over for normalization

    Returns
    ---------------

    img: ND-array, float32
        normalized image of same size

    """
    if img.ndim < 3:
        error_message = 'Image needs to have at least 3 dimensions'
        transforms_logger.critical(error_message)
        raise ValueError(error_message)

    img = img.astype(np.float32)
    img = np.moveaxis(img, axis, 0)
    for k in range(img.shape[0]):
        # ptp can still give nan's with weird images
        if np.percentile(img[k], 99) > np.percentile(img[k], 1) + 1e-3:  # np.ptp(img[k]) > 1e-3:
            img[k] = normalize99(img[k], omni=omni)
            if invert:
                img[k] = -1 * img[k] + 1
    img = np.moveaxis(img, 0, axis)
    return img


def reshape_train_test(train_data, train_labels, test_data, test_labels, channels, channel_axis=0, normalize=True,
                       dim=2, omni=False):
    """ check sizes and reshape train and test data for training """
    nimg = len(train_data)
    # check that arrays are correct size
    if nimg != len(train_labels):
        error_message = 'train data and labels not same length'
        transforms_logger.critical(error_message)
        raise ValueError(error_message)
        return

    if train_labels[0].ndim < 2 or train_data[0].ndim < 2:
        error_message = 'training data or labels are not at least two-dimensional'
        transforms_logger.critical(error_message)
        raise ValueError(error_message)
        return

    if train_data[0].ndim > 3:
        error_message = 'training data is more than three-dimensional (should be 2D or 3D array)'
        transforms_logger.critical(error_message)
        raise ValueError(error_message)
        return

    # check if test_data correct length
    if not (test_data is not None and test_labels is not None and
            len(test_data) > 0 and len(test_data) == len(test_labels)):
        test_data = None

    print('reshape_train_test', train_data[0].shape, channels, normalize, omni)
    # make data correct shape and normalize it so that 0 and 1 are 1st and 99th percentile of data
    # reshape_and_normalize_data pads the train_data with an eplty channel axis if it doesn't have one (single channel images/volumes).
    train_data, test_data, run_test = reshape_and_normalize_data(train_data, test_data=test_data,
                                                                 channels=channels, channel_axis=channel_axis,
                                                                 normalize=normalize, omni=omni, dim=dim)
    print('reshape_train_test_2', train_data[0].shape)

    if train_data is None:
        error_message = 'training data do not all have the same number of channels'
        transforms_logger.critical(error_message)
        raise ValueError(error_message)
        return

    if not run_test:
        test_data, test_labels = None, None

    return train_data, train_labels, test_data, test_labels, run_test


def reshape_and_normalize_data(train_data, test_data=None, channels=None, channel_axis=0, normalize=True, omni=False,
                               dim=2):
    """ inputs converted to correct shapes for *training* and rescaled so that 0.0=1st percentile
    and 1.0=99th percentile of image intensities in each channel

    Parameters
    --------------

    train_data: list of ND-arrays, float
        list of training images of size [Ly x Lx], [nchan x Ly x Lx], or [Ly x Lx x nchan]

    test_data: list of ND-arrays, float (optional, default None)
        list of testing images of size [Ly x Lx], [nchan x Ly x Lx], or [Ly x Lx x nchan]

    channels: list of int of length 2 (optional, default None)
        First element of list is the channel to segment (0=grayscale, 1=red, 2=green, 3=blue).
        Second element of list is the optional nuclear channel (0=none, 1=red, 2=green, 3=blue).
        For instance, to train on grayscale images, input [0,0]. To train on images with cells
        in green and nuclei in blue, input [2,3].

    normalize: bool (optional, True)
        normalize data so 0.0=1st percentile and 1.0=99th percentile of image intensities in each channel

    Returns
    -------------

    train_data: list of ND-arrays, float
        list of training images of size [2 x Ly x Lx]

    test_data: list of ND-arrays, float (optional, default None)
        list of testing images of size [2 x Ly x Lx]

    run_test: bool
        whether or not test_data was correct size and is useable during training

    """

    for test, data in enumerate([train_data, test_data]):
        if data is None:
            return train_data, test_data, False
        nimg = len(data)
        # print('reshape_and_normalize_data',nimg,channels,data[0].shape)
        for i in range(nimg):
            if channels is not None:
                data[i] = move_min_dim(data[i],
                                       force=True)  ## consider changign this to just use the channel_axis, not min dim
            # print('3454354',data[i].shape)
            if channels is not None:
                data[i] = reshape(data[i], channels=channels, chan_first=True,
                                  channel_axis=channel_axis)  # the cuplrit with 3D
                # print('fgddgfgdfg',data[i].shape)

            # if data[i].ndim < 3:
            #     data[i] = data[i][np.newaxis,:,:]
            # we actually want this padding for single-channel volumes too

            # data with multiple channels will have channels defined and have an axis already; could also pass in nchan to avoid this assumption
            if channels is None and data[i].ndim == dim:
                data[i] = data[i][np.newaxis]

            # instead of this, we could just make the other parts of the code not rely on a channel axis and slice smarter

            if normalize:
                data[i] = normalize_img(data[i], axis=0, omni=omni)
        nchan = [data[i].shape[0] for i in range(nimg)]
    print('reshape_and_normalize_data_2', nimg, channels, data[0].shape, train_data[0].shape)
    return train_data, test_data, True


def resize_image(img0, Ly=None, Lx=None, rsz=None, interpolation=cv2.INTER_LINEAR, no_channels=False):
    """ resize image for computing flows / unresize for computing dynamics

    Parameters
    -------------

    img0: ND-array
        image of size [Y x X x nchan] or [Lz x Y x X x nchan] or [Lz x Y x X]

    Ly: int, optional

    Lx: int, optional

    rsz: float, optional
        resize coefficient(s) for image; if Ly is None then rsz is used

    interpolation: cv2 interp method (optional, default cv2.INTER_LINEAR)

    Returns
    --------------

    imgs: ND-array
        image of size [Ly x Lx x nchan] or [Lz x Ly x Lx x nchan]

    """
    if Ly is None and rsz is None:
        error_message = 'must give size to resize to or factor to use for resizing'
        transforms_logger.critical(error_message)
        raise ValueError(error_message)

    if Ly is None:
        # determine Ly and Lx using rsz
        if not isinstance(rsz, list) and not isinstance(rsz, np.ndarray):
            rsz = [rsz, rsz]
        if no_channels:
            Ly = int(img0.shape[-2] * rsz[-2])
            Lx = int(img0.shape[-1] * rsz[-1])
        else:
            Ly = int(img0.shape[-3] * rsz[-2])
            Lx = int(img0.shape[-2] * rsz[-1])

    # no_channels useful for z-stacks, so the third dimension is not treated as a channel
    # but if this is called for grayscale images, they first become [Ly,Lx,2] so ndim=3 but
    if (img0.ndim > 2 and no_channels) or (img0.ndim == 4 and not no_channels):
        if no_channels:
            imgs = np.zeros((img0.shape[0], Ly, Lx), np.float32)
        else:
            imgs = np.zeros((img0.shape[0], Ly, Lx, img0.shape[-1]), np.float32)
        for i, img in enumerate(img0):
            imgs[i] = cv2.resize(img, (Lx, Ly), interpolation=interpolation)
            # imgs[i] = scipy.ndimage.zoom(img, resize/np.array(img.shape), order=order)

    else:
        imgs = cv2.resize(img0, (Lx, Ly), interpolation=interpolation)
    return imgs


def pad_image_ND(img0, div=16, extra=1, dim=2):
    """ pad image for test-time so that its dimensions are a multiple of 16 (2D or 3D)

    Parameters
    -------------

    img0: ND-array
        image of size [nchan (x Lz) x Ly x Lx]

    div: int (optional, default 16)

    Returns
    --------------

    I: ND-array
        padded image

    ysub: array, int
        yrange of pixels in I corresponding to img0

    xsub: array, int
        xrange of pixels in I corresponding to img0

    """

    inds = [k for k in range(-dim, 0)]
    Lpad = [int(div * np.ceil(img0.shape[i] / div) - img0.shape[i]) for i in inds]
    pad1 = [extra * div // 2 + Lpad[k] // 2 for k in range(dim)]
    pad2 = [extra * div // 2 + Lpad[k] - Lpad[k] // 2 for k in range(dim)]

    emptypad = tuple([[0, 0]] * (img0.ndim - dim))
    pads = emptypad + tuple(np.stack((pad1, pad2), axis=1))
    I = np.pad(img0, pads, mode='reflect')  # changed from 'constant' - avoids a lot of edge artifacts!!!

    shape = img0.shape[-dim:]
    subs = [np.arange(pad1[k], pad1[k] + shape[k]) for k in range(dim)]

    return I, subs


def normalize99_torch(Y, lower=0.01, upper=99.99, epsilon=1e-7):
    batch_size, channels, height, width = Y.shape

    # Flatten the input tensor for each image in the batch
    Y_flat = Y.view(batch_size, channels, -1)

    # Calculate lower and upper percentile values for each image in the batch
    lower_val = torch.quantile(Y_flat, lower / 100, dim=2)
    upper_val = torch.quantile(Y_flat, upper / 100, dim=2)

    # Add epsilon to avoid division by zero
    lower_val += epsilon
    upper_val += epsilon

    # Expand dimensions for broadcasting
    lower_val = lower_val.unsqueeze(-1).unsqueeze(-1)
    upper_val = upper_val.unsqueeze(-1).unsqueeze(-1)

    # Clamp and normalize the tensor for each image
    normalized = torch.clamp((Y - lower_val) / (upper_val - lower_val), 0, 1)

    # Check for NaN values
    if torch.isnan(normalized).any():
        print("Warning: NaN values found in the normalized tensor.")

    return normalized


def random_poisson_noise_batch_torch_gpu(batch, rng=None):
    """
    Add Poisson-distributed noise to each image in a batch of PyTorch tensors on the GPU.

    Parameters
    ----------
    batch : torch.Tensor
        Input batch of images with shape (batch_size, channels, height, width).
    rng : torch.Generator or int, optional
        Pseudo-random number generator. If not provided, a default generator will be used.

    Returns
    -------
    noisy_batch : torch.Tensor
        Output batch with Poisson noise added to each image on the GPU.
    """
    if rng is None:
        # Use the GPU's random number generator if available
        if torch.cuda.is_available():
            device = torch.device("cuda")
            rng = torch.Generator(device=device)
        else:
            rng = torch.Generator()

        rng.manual_seed(torch.seed())

    # Move the batch to the GPU if not already
    batch = batch.to(device)

    # Convert to float and ensure non-negative values
    batch = torch.clamp(batch, 0.0, float('inf')).float()

    # Generate Poisson noise for each image in the batch on the GPU
    noisy_batch = torch.poisson(batch, generator=rng)

    # Clip to ensure values are in the valid image range
    noisy_batch = torch.clamp(noisy_batch, 0.0, 1.0)

    return noisy_batch


def random_crop_warp_new(X, Y, D, S, links, nt, tyx, nchan, scale, rescale, scale_range, gamma_range,
                     do_flip, ind, dist_bg, depth=0):
    """
    This sub-function of `random_rotate_and_resize()` recursively performs random cropping until
    a minimum number of cell pixels are found, then proceeds with augmentations.

    Parameters
    ----------
    X: float, list of ND arrays
        image array of size [nchan x Lt x Ly x Lx] or [Lt x Ly x Lx]
    Y: float, ND array
        image label array of size [nlabels x Lt x Ly x Lx] or [Lt x Ly x Lx].. The 1st channel
        of Y is always nearest-neighbor interpolated (assumed to be masks or 0-1 representation).
        If Y.shape[0]==3, then the labels are assumed to be [cell probability, T flow, Y flow, X flow].
    tyx: int, tuple
        size of transformed images to return, e.g. (Ly,Lx) or (Lt,Ly,Lx)
    nchan: int
        number of channels the images have
    rescale: float, array or list
        how much to resize images by before performing augmentations
    scale_range: float
        Range of resizing of images for augmentation. Images are resized by
        (1-scale_range/2) + scale_range * np.random.rand()
    gamma_range: float
       images are gamma-adjusted im**gamma for gamma in (1-gamma_range,1+gamma_range)
    do_flip: bool (optional, default True)
        whether or not to flip images horizontally
    ind: int
        image index (for debugging)
    dist_bg: float
        non-negative value X for assigning -X to where distance=0 (deprecated, now adapts to field values)
    depth: int
        how many times this function has been called on an image

    Returns
    -------
    imgi: float, ND array
        transformed images in array [nchan x xy[0] x xy[1]]
    lbl: float, ND array
        transformed labels in array [nchan x xy[0] x xy[1]]
    scale: float, 1D array
        scalar by which the image was resized

    """

    dim = len(tyx)
    batch_size = len(X)

    # COMPUTATION OF RESCALING FACTORS
    # Compute ds
    ds = scale_range / 2

    # Generate random scales with anisotropic scaling
    scales = np.random.uniform(low=1 - ds, high=1 + ds, size=(len(rescale), dim))

    # Convert scales to a PyTorch tensor
    scale_tensor = torch.tensor(scales, dtype=torch.float32).to("cuda")

    # Apply the rescale factor if rescale is not None
    if rescale is not None:
        scale_tensor /= torch.tensor(rescale, dtype=torch.float32).to("cuda").unsqueeze(1)

    # Generate random theta values in PyTorch for rotation
    theta_tensor = torch.rand_like(scale_tensor[:, 0]) * 2 * torch.tensor(np.pi, dtype=torch.float32).to("cuda")
    dg = gamma_range / 2

    # Calculate the square crop size based on sqrt(2) * tyx then reduced to tyx after rotation
    crop_size = int(math.ceil(math.sqrt(2) * max(tyx)))

    # Create a tensor of zeros with the same shape as lbl
    lbl = torch.zeros((batch_size, nt,) + (crop_size, crop_size), dtype=torch.float32).to("cuda")
    imgi = torch.zeros((batch_size, nchan,) + (crop_size, crop_size), dtype=torch.float32).to("cuda")
    D_t = torch.zeros((batch_size, 1,) + (crop_size, crop_size), dtype=torch.float32).to("cuda")
    S_t = torch.zeros((batch_size, 1,) + (crop_size, crop_size), dtype=torch.float32).to("cuda")

    # for each image of the batch, we have to choose a labelled pixel we will center a crop on
    # Initialize lists to store coordinates and crops
    cropped_masks = []
    for i, mask in enumerate(Y):

        patch = X[i]
        Di = D[i]
        Si = S[i]
        # Find the coordinates of all labeled pixels in the mask
        labeled_coordinates = np.transpose(np.where(mask[0] != 0))

        # Randomly select one labeled pixel's coordinates
        random_index = np.random.choice(len(labeled_coordinates))
        random_pixel_coord = labeled_coordinates[random_index]

        # Calculate padding needed to ensure the crop is the desired size
        pad_y = max(crop_size // 2 - random_pixel_coord[0], 0)
        pad_x = max(crop_size // 2 - random_pixel_coord[1], 0)

        # Pad the mask symmetrically to ensure the crop is the desired size
        padded_mask = np.pad(mask, ((0, 0), (pad_y, crop_size - pad_y), (pad_x, crop_size - pad_x)),
                             mode='constant')
        padded_patch = np.pad(patch, ((0, 0), (pad_y, crop_size - pad_y), (pad_x, crop_size - pad_x)),
                              mode='constant')
        padded_D = np.pad(Di, ((pad_y, crop_size - pad_y), (pad_x, crop_size - pad_x)), mode='constant')
        padded_S = np.pad(Si, ((pad_y, crop_size - pad_y), (pad_x, crop_size - pad_x)), mode='constant')

        # Extract the square crop centered around the randomly selected labeled pixel
        y, x = random_pixel_coord + (pad_y, pad_x)
        mask_crop = padded_mask[:, y - crop_size // 2:y + crop_size // 2 + 1, x - crop_size // 2:x + crop_size // 2 + 1]
        patch_crop = padded_patch[:, y - crop_size // 2:y + crop_size // 2 + 1, x - crop_size // 2:x + crop_size // 2 + 1]
        D_crop = padded_D[y - crop_size // 2:y + crop_size // 2 + 1, x - crop_size // 2:x + crop_size // 2 + 1]
        S_crop = padded_S[y - crop_size // 2:y + crop_size // 2 + 1, x - crop_size // 2:x + crop_size // 2 + 1]

        # Append the coordinates and crop to the respective lists
        lbl[i, :2, :] = torch.tensor(mask_crop, dtype=torch.from_numpy(mask_crop).dtype)
        imgi[i, :] = torch.tensor(patch_crop, dtype=torch.from_numpy(patch_crop).dtype)
        D_t[i, 0, :] = torch.tensor(D_crop, dtype=torch.from_numpy(D_crop).dtype)
        S_t[i, 0, :] = torch.tensor(S_crop, dtype=torch.from_numpy(S_crop).dtype)

    # Compute the rotation and scaling matrices using the given theta and scales values
    cos_theta = torch.cos(theta_tensor)
    sin_theta = torch.sin(theta_tensor)
    rotation_matrix = torch.stack([cos_theta, -sin_theta, sin_theta, cos_theta], dim=1).view(-1, 2, 2).to("cuda")
    scaling_matrix = torch.stack([scale_tensor[:, 0], torch.zeros_like(scale_tensor[:, 0]),
                                 torch.zeros_like(scale_tensor[:, 0]), scale_tensor[:, 1]],
                                 dim=1).view(-1, 2, 2).to("cuda")

    affine_matrices = torch.inverse(torch.matmul(scaling_matrix, rotation_matrix))
    affine_matrices = torch.cat((affine_matrices, torch.zeros(batch_size, 2, 1).to("cuda")), dim=2)

    # Apply the affine transformations to lbl
    # Assuming lbl is a tensor of shape (batch_size, nt, crop_size, crop_size)
    lbl_transformed = torch.nn.functional.affine_grid(affine_matrices, lbl.size(), align_corners=False)
    lbl = torch.nn.functional.grid_sample(lbl, lbl_transformed, align_corners=False, mode="nearest", padding_mode="reflection")

    # Computation of flows (no optimized on gpu)
    if nt > 2:
        lbl = lbl.cpu().numpy()
        for b in range(batch_size):
            l = lbl[b, 0].astype(np.uint16)
            l, dist, bd, T, mu = masks_to_flows(l, links=links, omni=True,
                                                dim=dim)  # should add normalize argument maybe
            lbl[b, 1] = l > 0  # used to interpolate the mask, now thinking it is better to stay perfectly consistent
            lbl[b, 2] = bd  # posisiton 2 store boundary, now returned as part of linked flow computation
            cutoff = diameters(l, T) / 2  # used to use dist, but dist does not work for multilabel objects

            smooth_dist = T
            smooth_dist[dist <= 0] = - cutoff  # -dist_bg
            lbl[b, 3] = smooth_dist  # position 3 stores the smooth distance field
            lbl[b, -dim:] = mu * 5.0  # x5 puts this in the same range as boundary logits

            mask = lbl[b, 1]  # binary mask,
            bg_edt = edt.edt(mask == 0, black_border=True)  # last arg gives weight to the border
            lbl[b, 4] = (gaussian(1 - np.clip(bg_edt, 0, cutoff) / cutoff, 1) + 0.5)

    lbl = torch.tensor(lbl, dtype=torch.from_numpy(lbl).dtype).to("cuda")
    # Data augmentation on the image

    imgi_transformed = torch.nn.functional.affine_grid(affine_matrices, imgi.size(), align_corners=False)
    imgi = torch.nn.functional.grid_sample(imgi, imgi_transformed, align_corners=False, padding_mode="reflection")

    # gamma augmentation
    gamma = torch.rand((batch_size, nchan), dtype=torch.float32).to("cuda") * (2 * dg) + (1 - dg)
    imgi = imgi ** gamma.unsqueeze(-1).unsqueeze(-1)

    # percentile clipping augmentation
    imgi = normalize99_torch(imgi, lower=0.01, upper=99.99)

    # Noise augmentation
    #imgi = random_poisson_noise_batch_torch_gpu(imgi)

    # Data augmentation on D and S
    D_t_transformed = torch.nn.functional.affine_grid(affine_matrices, D_t.size(), align_corners=False)
    D_t = torch.nn.functional.grid_sample(D_t, D_t_transformed, align_corners=False, mode="nearest", padding_mode="reflection")

    S_t_transformed = torch.nn.functional.affine_grid(affine_matrices, S_t.size(), align_corners=False)
    S_t = torch.nn.functional.grid_sample(S_t, S_t_transformed, align_corners=False, mode="nearest", padding_mode="reflection")

    # Now we apply flips to each image
    # Create random flips for each image in the batch
    random_flips_height = torch.randint(0, 2, (batch_size,))
    random_flips_width = torch.randint(0, 2, (batch_size,))

    # Apply flips along the height dimension (dimension -2)
    for i in range(batch_size):
        if random_flips_height[i]:
            imgi[i] = imgi[i].flip(-2)
            D_t[i] = D_t[i].flip(-2)
            S_t[i] = S_t[i].flip(-2)
            if Y is not None:
                lbl[i] = lbl[i].flip(-2)
                if nt > 1:
                    lbl[i, -2] = -lbl[i, -2]

    # Apply flips along the width dimension (dimension -1)
        elif random_flips_width[i]:
            imgi[i] = imgi[i].flip(-1)
            D_t[i] = D_t[i].flip(-1)
            S_t[i] = S_t[i].flip(-1)
            if Y is not None:
                lbl[i] = lbl[i].flip(-1)

    # Cropping and back to np array

    imgi = imgi.cpu().numpy()
    D = D_t[:, 0, :, :].cpu().numpy()
    S = S_t[:, 0, :, :].cpu().numpy()
    lbl = lbl.cpu().numpy()

    # Compute padding
    y_padding = int(math.ceil(math.sqrt(2) * max(tyx))) - tyx[0]
    x_padding = int(math.ceil(math.sqrt(2) * max(tyx))) - tyx[1]

    # Delete padding
    imgi = imgi[:, :, y_padding:y_padding + int(math.ceil(math.sqrt(2) * max(tyx))),
                         x_padding:x_padding + int(math.ceil(math.sqrt(2) * max(tyx)))]
    lbl = lbl[:, :, y_padding:y_padding + int(math.ceil(math.sqrt(2) * max(tyx))),
                          x_padding:x_padding + int(math.ceil(math.sqrt(2) * max(tyx)))]
    D = D[:, y_padding:y_padding + int(math.ceil(math.sqrt(2) * max(tyx))), x_padding:x_padding + int(math.ceil(math.sqrt(2) * max(tyx)))]
    S = S[:, y_padding:y_padding + int(math.ceil(math.sqrt(2) * max(tyx))), x_padding:x_padding + int(math.ceil(math.sqrt(2) * max(tyx)))]

    return imgi, lbl, D, S, scale


def random_crop_warp(img, Y, D, S, links, nt, tyx, nchan, scale, rescale, scale_range, gamma_range,
                     do_flip, ind, dist_bg, depth=0):
    """
    This sub-fuction of `random_rotate_and_resize()` recursively performs random cropping until
    a minimum number of cell pixels are found, then proceeds with augemntations.

    Parameters
    ----------
    X: float, list of ND arrays
        image array of size [nchan x Lt x Ly x Lx] or [Lt x Ly x Lx]
    Y: float, ND array
        image label array of size [nlabels x Lt x Ly x Lx] or [Lt x Ly x Lx].. The 1st channel
        of Y is always nearest-neighbor interpolated (assumed to be masks or 0-1 representation).
        If Y.shape[0]==3, then the labels are assumed to be [cell probability, T flow, Y flow, X flow].
    tyx: int, tuple
        size of transformed images to return, e.g. (Ly,Lx) or (Lt,Ly,Lx)
    nchan: int
        number of channels the images have
    rescale: float, array or list
        how much to resize images by before performing augmentations
    scale_range: float
        Range of resizing of images for augmentation. Images are resized by
        (1-scale_range/2) + scale_range * np.random.rand()
    gamma_range: float
       images are gamma-adjusted im**gamma for gamma in (1-gamma_range,1+gamma_range)
    do_flip: bool (optional, default True)
        whether or not to flip images horizontally
    ind: int
        image index (for debugging)
    dist_bg: float
        nonegative value X for assigning -X to where distance=0 (deprecated, now adapts to field values)
    depth: int
        how many time this function has been called on an image

    Returns
    -------
    imgi: float, ND array
        transformed images in array [nchan x xy[0] x xy[1]]
    lbl: float, ND array
        transformed labels in array [nchan x xy[0] x xy[1]]
    scale: float, 1D array
        scalar by which the image was resized

    """

    dim = len(tyx)
    # np.random.seed(depth)
    if depth > 100:
        error_message = """Sparse or over-dense image detected. 
        Problematic index is: {}. 
        Image shape is: {}. 
        tyx is: {}. 
        rescale is {}""".format(ind, img.shape, tyx, rescale)
        omnipose_logger.critical(error_message)
        skimage.io.imsave('/home/kcutler/DataDrive/debug/img' + str(depth) + '.png', img[0])
        raise ValueError(error_message)

    if depth > 200:
        error_message = """Recusion depth exceeded. Check that your images contain cells and background within a typical crop. 
                           Failed index is: {}.""".format(ind)
        omnipose_logger.critical(error_message)
        raise ValueError(error_message)
        return

    # labels that will be passed to the loss function
    #
    lbl = np.zeros((nt,) + tyx, np.float32)

    numpx = np.prod(tyx)
    if Y is not None:
        labels = Y.copy()
        # print(labels.shape,'A')
        # We want the scale distibution to have a mean of 1
        # There may be a better way to skew the distribution to
        # interpolate the parameter space without skewing the mean
        ds = scale_range / 2
        scale = np.random.uniform(low=1 - ds, high=1 + ds, size=dim)  # anisotropic scaling
        if rescale is not None:
            scale *= 1. / rescale

    # image dimensions are always the last <dim> in the stack (again, convention here is different)
    s = img.shape[-dim:]

    # generate random augmentation parameters
    dg = gamma_range / 2
    theta = np.random.rand() * np.pi * 2

    # first two basis vectors in any dimension
    v1 = [0] * (dim - 1) + [1]
    v2 = [0] * (dim - 2) + [1, 0]
    # M = mgen.rotation_from_angle_and_plane(theta,v1,v2) #not generalizing correctly to 3D? had -theta before
    M = mgen.rotation_from_angle_and_plane(-theta, v2, v1).dot(np.diag(scale))  # equivalent
    # could define v3 and do another rotation here and compose them

    axes = range(dim)
    s = img.shape[-dim:]
    rt = (np.random.rand(dim, ) - .5)  # random translation -.5 to .5
    dxy = [rt[a] * (np.maximum(0, s[a] - tyx[a])) for a in axes]

    c_in = 0.5 * np.array(s) + dxy
    c_out = 0.5 * np.array(tyx)
    offset = c_in - np.dot(np.linalg.inv(M), c_out)

    # M = np.vstack((M,offset))
    mode = 'reflect'
    if Y is not None:
        for k in [0]:  # [i for i in range(nt) if i not in range(2,5)]: used to do first two and flows, now just labels
            l = labels[k].copy()
            if k == 0:
                # print(l.shape,M,tyx)
                lbl[k] = do_warp(l, M, tyx, offset=offset, order=0, mode=mode)  # order 0 is 'nearest neighbor'
                lbl[k] = mode_filter(lbl[k])
                # check to make sure the region contains at enough cell pixels; if not, retry
                cellpx = np.sum(lbl[k] > 0)
                cutoff = (numpx / 10 ** (dim + 1))  # .1 percent of pixels must be cells
                # print('after warp',len(np.unique(lbl[k])),np.max(lbl[k]),np.min(lbl[k]),cutoff,numpx, cellpx, theta)
                if cellpx < cutoff:  # or cellpx==numpx: # had to disable the overdense feature for cyto2
                    # may not actually be a problem now anyway
                    # print('toosmall',nt)
                    # skimage.io.imsave('/home/kcutler/DataDrive/debug/img'+str(depth)+'.png',img[0])
                    # skimage.io.imsave('/home/kcutler/DataDrive/debug/training'+str(depth)+'.png',lbl[0])
                    return random_crop_warp(img, Y, D, S, links, nt, tyx, nchan, scale, rescale, scale_range,
                                            gamma_range, do_flip, ind, dist_bg, depth=depth + 1)
            else:
                lbl[k] = do_warp(l, M, tyx, offset=offset, mode=mode)

                # if k==1:
                #     print('fgd', np.sum(lbl[k]))

        # LABELS ARE NOW (masks,mask) for semantic seg with additional (bd,dist,weight,flows) for instance seg
        # semantic seg label transformations taken care of above, those are simple enough. Others
        # must be computed after mask transformations are made.
        if nt > 2:
            l = lbl[0].astype(np.uint16)
            l, dist, bd, T, mu = masks_to_flows(l, links=links, omni=True,
                                                dim=dim)  # should add normalize argument maybe
            lbl[1] = l > 0  # used to interpolate the mask, now thinking it is better to stay perfectly consistent
            lbl[2] = bd  # posisiton 2 store boundary, now returned as part of linked flow computation
            cutoff = diameters(l, T) / 2  # used to use dist, but dist does not work for multilabel objects

            smooth_dist = T
            smooth_dist[dist <= 0] = - cutoff  # -dist_bg
            lbl[3] = smooth_dist  # position 3 stores the smooth distance field
            lbl[-dim:] = mu * 5.0  # x5 puts this in the same range as boundary logits

            # print('dists',np.max(dist),np.max(smooth_dist))
            # the black border arg may not be good in 3D, as it highlights a larger fraction?
            mask = lbl[1]  # binary mask,
            bg_edt = edt.edt(mask == 0, black_border=True)  # last arg gives weight to the border
            lbl[4] = (gaussian(1 - np.clip(bg_edt, 0, cutoff) / cutoff, 1) + 0.5)

    # Makes more sense to spend time on image augmentations
    # after the label augmentation succeeds without triggering recursion
    imgi = np.zeros((nchan,) + tyx, np.float32)
    for k in range(nchan):
        I = do_warp(img[k], M, tyx, offset=offset, mode=mode)

        # gamma agumentation
        gamma = np.random.uniform(low=1 - dg, high=1 + dg)
        imgi[k] = I ** gamma

        # percentile clipping augmentation
        dp = 10
        dpct = np.random.triangular(left=0, mode=0, right=dp, size=2)  # weighted toward 0
        imgi[k] = utils.normalize99(imgi[k], upper=100 - dpct[0], lower=dpct[1])

        # noise augmentation
        if SKIMAGE_ENABLED:

            # imgi[k] = random_noise(utils.rescale(imgi[k]), mode="poisson")#, seed=None, clip=True)
            imgi[k] = random_noise(utils.rescale(imgi[k]), mode="poisson")  # , seed=None, clip=True)

        else:
            # this is quite different
            # imgi[k] = np.random.poisson(imgi[k])
            print('warning,no randomnoise')

        # bit depth augmentation
        bit_shift = int(np.random.triangular(left=0, mode=8, right=16, size=1))
        im = (imgi[k] * (2 ** 16 - 1)).astype(np.uint16)
        imgi[k] = utils.normalize99(im >> bit_shift)

    # Rotation and cropping for D and S
    D = do_warp(D, M, tyx, offset=offset, mode=mode)
    S = do_warp(S, M, tyx, offset=offset, mode=mode)

    # print('aaa',imgi.shape,lbl.shape,nt)
    # Moved to the end because it conflicted with the recursion.
    # Also, flipping the crop is ultimately equivalent and slightly faster.
    # We now flip along every axis (randomly); could make do_flip a list to avoid some axes if needed
    if do_flip:
        for d in range(1, dim + 1):
            flip = np.random.choice([0, 1])
            if flip:
                imgi = np.flip(imgi, axis=-d)
                if Y is not None:
                    lbl = np.flip(lbl, axis=-d)
                    if nt > 1:
                        lbl[-d] = -lbl[-d]
                D = np.flip(D, axis=-d)
                S = np.flip(S, axis=-d)

    return imgi, lbl, D, S, scale


def do_warp(A, M, tyx, offset=0, order=1, mode='constant', **kwargs):  # ,mode,method):
    """ Wrapper function for affine transformations during augmentation.
    Uses scipy.ndimage.affine_transform().

    Parameters
    --------------
    A: NDarray, int or float
        input image to be transformed
    M: NDarray, float
        tranformation matrix
    order: int
        interpolation order, 1 is equivalent to 'nearest',
    """
    # dim = A.ndim'
    # if dim == 2:
    #     return cv2.warpAffine(A, M, rshape, borderMode=mode, flags=method)
    # else:
    #     return np.stack([cv2.warpAffine(A[k], M, rshape, borderMode=mode, flags=method) for k in range(A.shape[0])])
    # print('debug',A.shape,M.shape,tyx)

    return scipy.ndimage.affine_transform(A, np.linalg.inv(M), offset=offset,
                                          output_shape=tyx, order=order, mode=mode, **kwargs)


def omni_random_rotate_and_resize(X, Y, D, S, links=None, scale_range=1., gamma_range=0.5, tyx=(224, 224),
                             do_flip=True, rescale=None, inds=None, nchan=1, nclasses=4):
    """ augmentation by random rotation and resizing

        X and Y are lists or arrays of length nimg, with channels x Lt x Ly x Lx (channels optional, Lt only in 3D)

        Parameters
        ----------
        X: float, list of ND arrays
            list of image arrays of size [nchan x Lt x Ly x Lx] or [Lt x Ly x Lx]
        Y: float, list of ND arrays
            list of image labels of size [nlabels x Lt x Ly x Lx] or [Lt x Ly x Lx]. The 1st channel
            of Y is always nearest-neighbor interpolated (assumed to be masks or 0-1 representation).
            If Y.shape[0]==3, then the labels are assumed to be [distance, T flow, Y flow, X flow].
        links: list of label links
            lists of label pairs linking parts of multi-label object together
            this is how omnipose gets around boudary artifacts druing image warps
        scale_range: float (optional, default 1.0)
            Range of resizing of images for augmentation. Images are resized by
            (1-scale_range/2) + scale_range * np.random.rand()
        gamma_range: float
           images are gamma-adjusted im**gamma for gamma in (1-gamma_range,1+gamma_range)
        tyx: int, tuple
            size of transformed images to return, e.g. (Ly,Lx) or (Lt,Ly,Lx)
        do_flip: bool (optional, default True)
            whether or not to flip images horizontally
        rescale: float, array or list
            how much to resize images by before performing augmentations
        inds: int, list
            image indices (for debugging)
        nchan: int
            number of channels the images have

        Returns
        -------
        imgi: float, ND array
            transformed images in array [nimg x nchan x xy[0] x xy[1]]
        lbl: float, ND array
            transformed labels in array [nimg x nchan x xy[0] x xy[1]]
        scale: float, 1D array
            scalar(s) by which each image was resized

    """
    dist_bg = 5  # background distance field was set to -dist_bg; now is variable
    dim = len(tyx)  # 2D will just have yx dimensions, 3D will be tyx

    nimg = len(X)
    imgi = np.zeros((nimg, nchan) + tyx, np.float32)
    D_ti = np.zeros((nimg,) + tyx, np.float32)
    S_ti = np.zeros((nimg,) + tyx, np.float32)
    # print(np.array(Y).shape,'C',imgi.shape)

    if Y is not None:
        for n in range(nimg):
            masks = Y[n]  # now assume straight labels
            iscell = masks > 0
            if np.sum(iscell) == 0:
                error_message = 'No cell pixels. Index is' + str(n)
                omnipose_logger.critical(error_message)
                raise ValueError(error_message)
            Y[n] = np.stack([masks, iscell])

    nt = 2  # instance seg (labels), semantic seg (cellprob)
    if nclasses > 3:
        nt += 3 + dim  # add boundary, distance, weight, flow components

    lbl = np.zeros((nimg, nt) + tyx, np.float32)
    scale = np.zeros((nimg, dim), np.float32)

    # print('bbb',lbl.shape,nclasses, nt)
    for n in range(nimg):
        img = X[n].copy()
        y = None if Y is None else Y[n]
        lnk = None if links is None else links[n]
        # print(y.shape,'B')
        # use recursive function here to pass back single image that was cropped appropriately
        # # print(y.shape)
        # skimage.io.imsave('/home/kcutler/DataDrive/debug/img_orig.png',img[0])
        # skimage.io.imsave('/home/kcutler/DataDrive/debug/label_orig.tiff',y[n]) #so at this point the bad label is just fine
        imgi[n], lbl[n], D_ti[n], S_ti[n], scale[n] = random_crop_warp(img, y, D[n], S[n], lnk, nt, tyx, nchan, scale[n],
                                                     rescale is None if rescale is None else rescale[n],
                                                     scale_range, gamma_range, do_flip,
                                                     inds is None if inds is None else inds[n], dist_bg)

    return imgi, lbl, D_ti, S_ti, np.mean(scale)  # for size training, must output scalar size (need to check this again)


def omni_random_rotate_and_resize_new(X, Y, D, S, links=None, scale_range=1., gamma_range=0.5, tyx=(224, 224),
                             do_flip=True, rescale=None, inds=None, nchan=1, nclasses=4):
    """ augmentation by random rotation and resizing

        X and Y are lists or arrays of length nimg, with channels x Lt x Ly x Lx (channels optional, Lt only in 3D)

        Parameters
        ----------
        X: float, list of ND arrays
            list of image arrays of size [nchan x Lt x Ly x Lx] or [Lt x Ly x Lx]
        Y: float, list of ND arrays
            list of image labels of size [nlabels x Lt x Ly x Lx] or [Lt x Ly x Lx]. The 1st channel
            of Y is always nearest-neighbor interpolated (assumed to be masks or 0-1 representation).
            If Y.shape[0]==3, then the labels are assumed to be [distance, T flow, Y flow, X flow].
        links: list of label links
            lists of label pairs linking parts of multi-label object together
            this is how omnipose gets around boudary artifacts druing image warps
        scale_range: float (optional, default 1.0)
            Range of resizing of images for augmentation. Images are resized by
            (1-scale_range/2) + scale_range * np.random.rand()
        gamma_range: float
           images are gamma-adjusted im**gamma for gamma in (1-gamma_range,1+gamma_range)
        tyx: int, tuple
            size of transformed images to return, e.g. (Ly,Lx) or (Lt,Ly,Lx)
        do_flip: bool (optional, default True)
            whether or not to flip images horizontally
        rescale: float, array or list
            how much to resize images by before performing augmentations
        inds: int, list
            image indices (for debugging)
        nchan: int
            number of channels the images have

        Returns
        -------
        imgi: float, ND array
            transformed images in array [nimg x nchan x xy[0] x xy[1]]
        lbl: float, ND array
            transformed labels in array [nimg x nchan x xy[0] x xy[1]]
        scale: float, 1D array
            scalar(s) by which each image was resized

    """
    dist_bg = 5  # background distance field was set to -dist_bg; now is variable
    dim = len(tyx)  # 2D will just have yx dimensions, 3D will be tyx

    nimg = len(X)
    imgi = np.zeros((nimg, nchan) + tyx, np.float32)
    D_ti = np.zeros((nimg,) + tyx, np.float32)
    S_ti = np.zeros((nimg,) + tyx, np.float32)
    # print(np.array(Y).shape,'C',imgi.shape)

    if Y is not None:
        for n in range(nimg):
            masks = Y[n]  # now assume straight labels
            iscell = masks > 0
            if np.sum(iscell) == 0:
                error_message = 'No cell pixels. Index is' + str(n)
                omnipose_logger.critical(error_message)
                raise ValueError(error_message)
            Y[n] = np.stack([masks, iscell])

    nt = 2  # instance seg (labels), semantic seg (cellprob)
    if nclasses > 3:
        nt += 3 + dim  # add boundary, distance, weight, flow components

    lbl = np.zeros((nimg, nt) + tyx, np.float32)
    scale = np.zeros((nimg, dim), np.float32)

    imgi, lbl, D_ti, S_ti, scale = random_crop_warp(X, Y, D, S, None, nt, tyx, nchan, scale,
                                                    rescale, scale_range, gamma_range, do_flip, inds, dist_bg)

    return imgi, lbl, D_ti, S_ti, np.mean(scale)  # for size training, must output scalar size (need to check this again)


def random_rotate_and_resize(X, Y, D, S, links=None, scale_range=1., gamma_range=0.5, tyx=None,
                             do_flip=True, rescale=None, unet=False,
                             inds=None, omni=False, dim=2, nchan=1, nclasses=3, kernel_size=2, cp_data_aug=True):
    """ augmentation by random rotation and resizing

        X and Y are lists or arrays of length nimg, with dims channels x Ly x Lx (channels optional)

        Parameters
        ----------
        X: LIST of ND-arrays, float
            list of image arrays of size [nchan x Ly x Lx] or [Ly x Lx]

        Y: LIST of ND-arrays, float (optional, default None)
            list of image labels of size [nlabels x Ly x Lx] or [Ly x Lx]. The 1st channel
            of Y is always nearest-neighbor interpolated (assumed to be masks or 0-1 representation).
            If Y.shape[0]==3 and not unet, then the labels are assumed to be [cell probability, Y flow, X flow].
            If unet, second channel is dist_to_bound.

        links: list of label links
            lists of label pairs linking parts of multi-label object together
            this is how omnipose gets around boudary artifacts druing image warps

        scale_range: float (optional, default 1.0)
            Range of resizing of images for augmentation. Images are resized by
            (1-scale_range/2) + scale_range * np.random.rand()

        gamma_range: float (optional, default 0.5)
           Images are gamma-adjusted im**gamma for gamma in (1-gamma_range,1+gamma_range)

        xy: tuple, int (optional, default (224,224))
            size of transformed images to return

        do_flip: bool (optional, default True)
            whether or not to flip images horizontally

        rescale: array, float (optional, default None)
            how much to resize images by before performing augmentations

        unet: bool (optional, default False)

        Returns
        -------
        imgi: ND-array, float
            transformed images in array [nimg x nchan x xy[0] x xy[1]]

        lbl: ND-array, float
            transformed labels in array [nimg x nchan x xy[0] x xy[1]]

        scale: array, float
            amount each image was resized by

    """
    scale_range = max(0, min(2, float(scale_range)))  # limit overall range to [0,2] i.e. 1+-1

    if inds is None:  # only relevant when debugging
        nimg = len(X)
        inds = np.arange(nimg)

    if omni and OMNI_INSTALLED and not cp_data_aug:
        n = 16
        base = kernel_size
        L = max(round(224 / (base ** 4)), 1) * (base ** 4)  # rounds 224 up to the right multiple to work for base
        # not sure if 4 downsampling or 3, but the "multiple of 16" elsewhere makes me think it must be 4,
        # but it appears that multiple of 8 actually works? maybe the n=16 above conflates my experiments in 3D
        if tyx is None:
            tyx = (L,) * dim if dim == 2 else (8 * n,) + (8 * n,) * (dim - 1)  # must be divisible by 2**3 = 8
        return omni_random_rotate_and_resize(X, Y, D, S, links=links, scale_range=scale_range,
                                                      gamma_range=gamma_range,
                                                      tyx=tyx, do_flip=do_flip, rescale=rescale, inds=inds,
                                                      nchan=nchan, nclasses=nclasses)

    elif omni and OMNI_INSTALLED and cp_data_aug:
        # Sketchpose version, so we do not compute flows on the fly during data augmentation.
        if tyx is None:
            xy = (224,) * dim
        D = np.stack(D, axis=0)
        S = np.stack(S, axis=0)
        return sketchpose_random_rotate_and_resize(X, Y, D=D, S=S,
                                                   scale_range=scale_range, xy=xy, do_flip=do_flip, rescale=rescale,
                                                   unet=unet)

    else:
        # backwards compatibility; completely 'stock', no gamma augmentation or any other extra frills.
        # [Y[i][1:] for i in inds] is necessary because the original transform function does not use masks (entry 0).
        # This used to be done in the original function call.
        if tyx is None:
            xy = (224,) * dim
        return original_random_rotate_and_resize(X, Y=[y[1:] for y in Y] if Y is not None else None,
                                                 scale_range=scale_range, xy=xy,
                                                 do_flip=do_flip, rescale=rescale, unet=unet)


# I have the omni flag here just in case, but it actually does not affect the tests
def normalize_field(mu, omni=False):
    if omni and OMNI_INSTALLED:
        mu = omnipose.utils.normalize_field(mu)
    else:
        mu /= (1e-20 + (mu ** 2).sum(axis=0) ** 0.5)
    return mu


def _X2zoom(img, X2=1):
    """ zoom in image

    Parameters
    ----------
    img : numpy array that's Ly x Lx

    Returns
    -------
    img : numpy array that's Ly x Lx

    """
    ny, nx = img.shape[:2]
    img = cv2.resize(img, (int(nx * (2 ** X2)), int(ny * (2 ** X2))))
    return img


def _image_resizer(img, resize=512, to_uint8=False):
    """ resize image

    Parameters
    ----------
    img : numpy array that's Ly x Lx

    resize : int
        max size of image returned

    to_uint8 : bool
        convert image to uint8

    Returns
    -------
    img : numpy array that's Ly x Lx, Ly,Lx<resize

    """
    ny, nx = img.shape[:2]
    if to_uint8:
        if img.max() <= 255 and img.min() >= 0 and img.max() > 1:
            img = img.astype(np.uint8)
        else:
            img = img.astype(np.float32)
            img -= img.min()
            img /= img.max()
            img *= 255
            img = img.astype(np.uint8)
    if np.array(img.shape).max() > resize:
        if ny > nx:
            nx = int(nx / ny * resize)
            ny = resize
        else:
            ny = int(ny / nx * resize)
            nx = resize
        shape = (nx, ny)
        img = cv2.resize(img, shape)
        img = img.astype(np.uint8)
    return img


def original_random_rotate_and_resize(X, Y, scale_range=1., xy=(224, 224),
                                      do_flip=True, rescale=None, unet=False):
    """ augmentation by random rotation and resizing
        X and Y are lists or arrays of length nimg, with dims channels x Ly x Lx (channels optional)

        Parameters
        ----------
        X: LIST of ND-arrays, float
            list of image arrays of size [nchan x Ly x Lx] or [Ly x Lx]
        Y: LIST of ND-arrays, float (optional, default None)
            list of image labels of size [nlabels x Ly x Lx] or [Ly x Lx]. The 1st channel
            of Y is always nearest-neighbor interpolated (assumed to be masks or 0-1 representation).
            If Y.shape[0]==3 and not unet, then the labels are assumed to be [cell probability, Y flow, X flow].
            If unet, second channel is dist_to_bound.
        scale_range: float (optional, default 1.0)
            Range of resizing of images for augmentation. Images are resized by
            (1-scale_range/2) + scale_range * np.random.rand()
        xy: tuple, int (optional, default (224,224))
            size of transformed images to return
        do_flip: bool (optional, default True)
            whether or not to flip images horizontally
        rescale: array, float (optional, default None)
            how much to resize images by before performing augmentations
        unet: bool (optional, default False)

        Returns
        -------
        imgi: ND-array, float
            transformed images in array [nimg x nchan x xy[0] x xy[1]]
        lbl: ND-array, float
            transformed labels in array [nimg x nchan x xy[0] x xy[1]]
        scale: array, float
            amount by which each image was resized
    """
    scale_range = max(0, min(2, float(scale_range)))
    nimg = len(X)
    if X[0].ndim > 2:
        nchan = X[0].shape[0]
    else:
        nchan = 1
    imgi = np.zeros((nimg, nchan, xy[0], xy[1]), np.float32)

    lbl = []
    if Y is not None:
        if Y[0].ndim > 2:
            nt = Y[0].shape[0]
        else:
            nt = 1
        lbl = np.zeros((nimg, nt, xy[0], xy[1]), np.float32)

    scale = np.zeros(nimg, np.float32)
    for n in range(nimg):
        Ly, Lx = X[n].shape[-2:]

        # generate random augmentation parameters
        flip = np.random.rand() > .5
        theta = np.random.rand() * np.pi * 2
        scale[n] = (1 - scale_range / 2) + scale_range * np.random.rand()
        if rescale is not None:
            scale[n] *= 1. / rescale[n]
        dxy = np.maximum(0, np.array([Lx * scale[n] - xy[1], Ly * scale[n] - xy[0]]))
        dxy = (np.random.rand(2, ) - .5) * dxy

        # create affine transform
        cc = np.array([Lx / 2, Ly / 2])
        cc1 = cc - np.array([Lx - xy[1], Ly - xy[0]]) / 2 + dxy
        pts1 = np.float32([cc, cc + np.array([1, 0]), cc + np.array([0, 1])])
        pts2 = np.float32([cc1,
                           cc1 + scale[n] * np.array([np.cos(theta), np.sin(theta)]),
                           cc1 + scale[n] * np.array([np.cos(np.pi / 2 + theta), np.sin(np.pi / 2 + theta)])])
        M = cv2.getAffineTransform(pts1, pts2)

        img = X[n].copy()

        if Y is not None:
            labels = Y[n].copy()
            if labels.ndim < 3:
                labels = labels[np.newaxis, :, :]

        if flip and do_flip:
            img = img[..., ::-1]
            if Y is not None:
                labels = labels[..., ::-1]
                if nt > 1 and not unet:
                    labels[2] = -labels[2]

        for k in range(nchan):
            I = cv2.warpAffine(img[k], M, (xy[1], xy[0]), flags=cv2.INTER_LINEAR)
            imgi[n, k] = I

        if Y is not None:
            for k in range(nt):
                if k == 0:
                    lbl[n, k] = cv2.warpAffine(labels[k], M, (xy[1], xy[0]), flags=cv2.INTER_NEAREST)
                else:
                    lbl[n, k] = cv2.warpAffine(labels[k], M, (xy[1], xy[0]), flags=cv2.INTER_LINEAR)

            if nt > 1 and not unet:
                v1 = lbl[n, 2].copy()
                v2 = lbl[n, 1].copy()
                lbl[n, 1] = (-v1 * np.sin(-theta) + v2 * np.cos(-theta))
                lbl[n, 2] = (v1 * np.cos(-theta) + v2 * np.sin(-theta))

    return imgi, lbl, scale


def apply_transform(x, labels, random_pixel, xy, M, flags, d_translate):
    """
    rotate, rescale, translate and crop x matrix
    :param x:
    :param labels:
    :param random_pixel:
    :param xy:
    :param M:
    :param flags:
    :param d_translate
    :return:
    """
    # New origin, because of padding
    x0, y0 = int(random_pixel[0] + xy[0]), int(random_pixel[1] + xy[1])
    x_pad = np.pad(x, ((xy[0], xy[0]), (xy[1], xy[1])), mode="symmetric")
    D = cv2.warpAffine(x_pad.copy(), M, (labels[0].shape[1] + 2 * xy[1], labels[0].shape[0] + 2 * xy[0]), flags=flags)

    D_crop = D[x0 - xy[0] // 2 + d_translate[0]: x0 + xy[0] // 2 + d_translate[0],
               y0 - xy[1] // 2 + d_translate[1]: y0 + xy[1] // 2 + d_translate[1]]
    return D_crop


def sketchpose_random_rotate_and_resize(X, Y, D, S, scale_range=1., xy=(224, 224),
                                        do_flip=True, rescale=None, unet=False):
    """ augmentation by random rotation and resizing. This derives from Cellpose implementation
    and is adapted to Omnipose to avoid recomputing flows on the fly at each iteration to earn time.
        X and Y are lists or arrays of length nimg, with dims channels x Ly x Lx (channels optional)

        Parameters
        ----------
        X: LIST of ND-arrays, float
            list of image arrays of size [nchan x Ly x Lx] or [Ly x Lx]
        Y: LIST of ND-arrays, float (optional, default None)
            list of image labels of size [nlabels x Ly x Lx] or [Ly x Lx]. The 1st channel
            of Y is always nearest-neighbor interpolated (assumed to be masks or 0-1 representation).
            If Y.shape[0]==3 and not unet, then the labels are assumed to be [cell probability, Y flow, X flow].
            If unet, second channel is dist_to_bound.
        scale_range: float (optional, default 1.0)
            Range of resizing of images for augmentation. Images are resized by
            (1-scale_range/2) + scale_range * np.random.rand()
        xy: tuple, int (optional, default (224,224))
            size of transformed images to return
        do_flip: bool (optional, default True)
            whether or not to flip images horizontally
        rescale: array, float (optional, default None)
            how much to resize images by before performing augmentations
        unet: bool (optional, default False)

        Returns
        -------
        imgi: ND-array, float
            transformed images in array [nimg x nchan x xy[0] x xy[1]]
        lbl: ND-array, float
            transformed labels in array [nimg x nchan x xy[0] x xy[1]]
        scale: array, float
            amount by which each image was resized
    """
    dim = len(xy)

    scale_range = max(0, min(2, float(scale_range)))
    nimg = len(X)
    if X[0].ndim > 2:
        nchan = X[0].shape[0]
    else:
        nchan = 1
    imgi = np.zeros((nimg, nchan, xy[0], xy[1]), np.float32)

    lbl = []
    if Y is not None:
        nt = 7
        lbl = np.zeros((nimg, nt, xy[0], xy[1]), np.float32)
        D_crop = np.zeros((nimg, xy[0], xy[1]), np.float32)
        S_crop = np.zeros((nimg, xy[0], xy[1]), np.float32)

    scale = np.zeros(nimg, np.float32)
    for n in range(nimg):
        l, dist, bd, T, mu = Y[n][0], Y[n][1], Y[n][2], Y[n][3], Y[n][4]

        # labels is lbl before the various data augmentation including cropping
        labels = np.zeros((nt, l.shape[0], l.shape[1]), np.float32)

        labels[0] = Y[n][0]
        labels[1] = l > 0  # used to interpolate the mask, now thinking it is better to stay perfectly consistent
        labels[2] = bd  # posisiton 2 store boundary, now returned as part of linked flow computation

        cutoff = diameters(l, T) / 2  # used to use dist, but dist does not work for multilabel objects

        smooth_dist = T
        smooth_dist[dist <= 0] = - cutoff  # -dist_bg
        labels[3] = smooth_dist  # position 3 stores the smooth distance field
        labels[-dim:] = mu * 5.0  # x5 puts this in the same range as boundary logits

        # print('dists',np.max(dist),np.max(smooth_dist))
        # the black border arg may not be good in 3D, as it highlights a larger fraction?
        mask = labels[1]  # binary mask,
        bg_edt = edt.edt(mask == 0, black_border=False)  # last arg gives weight to the border
        labels[4] = (gaussian(1 - np.clip(bg_edt, 0, cutoff) / cutoff, 1) + 0.5)

        # generate random augmentation parameters
        flip = np.random.rand() > .5
        theta_degree = np.random.rand() * 360
        theta = theta_degree / 360 * np.pi * 2
        scale[n] = (1 - scale_range / 2) + scale_range * np.random.rand()
        if rescale is not None:
            scale[n] *= 1. / rescale[n]

        img = X[n].copy()

        if flip and do_flip:
            img = img[..., ::-1]
            if Y is not None:
                labels = labels[..., ::-1]
                D[n] = D[n, :, ::-1]
                S[n] = S[n, :, ::-1]
                # comprends pas
                if nt > 1 and not unet:
                    labels[6] = -labels[6]

        # Randomly select one labeled pixel's coordinates
        props = regionprops(labels[0].astype("uint16"))
        random_pixel = np.ceil(props[np.random.choice(len(props))].centroid)

        """min_distance_to_border = max(xy) // 2

        for i in range(2):
            random_pixel[i] = np.min(
                [labels[0].shape[i] - min_distance_to_border, np.max([min_distance_to_border, random_pixel[i]])])"""

        # rotation and scaling random matrix (taking into account the padding)
        M = cv2.getRotationMatrix2D((int(random_pixel[1] + xy[1]), int(random_pixel[0] + xy[0])), theta_degree, scale[0])

        # random translation factor
        d_translate = (np.random.randint(-xy[0] // 2, xy[0] // 2), np.random.randint(-xy[0] // 2, xy[0] // 2))

        # Affine transform and cropping on D and S
        D_crop[n] = apply_transform(D[n], labels, random_pixel, xy, M, cv2.INTER_NEAREST, d_translate)
        S_crop[n] = apply_transform(S[n], labels, random_pixel, xy, M, cv2.INTER_NEAREST, d_translate)

        for k in range(nchan):
            imgi[n, k] = apply_transform(img[k], labels, random_pixel, xy, M, cv2.INTER_LINEAR, d_translate)

        if Y is not None:
            norm_gradient = lbl[n, 5]**2 + lbl[n, 6]**2
            for k in range(nt):
                if k == 1:
                    lbl[n, k] = apply_transform(labels[k], labels, random_pixel, xy, M, cv2.INTER_NEAREST, d_translate)
                elif k == 2:
                    lbl[n, k] = dilation(lbl[n, k], disk(1))
                    lbl[n, k] = apply_transform(labels[k], labels, random_pixel, xy, M, cv2.INTER_LINEAR, d_translate)
                    lbl[n, k][lbl[n, k] > 0.1] = 1
                    lbl[n, k][lbl[n, k] <= 0.1] = 0
                elif k == 3:
                    lbl[n, k] = apply_transform(labels[k], labels, random_pixel, xy, M, cv2.INTER_LINEAR, d_translate)#, -cutoff)
                    lbl[n, k][lbl[n, k] >= 0] *= scale[0]
                elif k == 4:
                    lbl[n, k] = apply_transform(labels[k], labels, random_pixel, xy, M, cv2.INTER_LINEAR, d_translate)  # , 0.5)
                    bg_edt = edt.edt(mask == 0, black_border=False)  # last arg gives weight to the border
                    labels[4] = (gaussian(1 - np.clip(bg_edt, 0, cutoff) / cutoff, 1) + 0.5)
                elif k == 5 or k == 6:
                    lbl[n, k] = apply_transform(labels[k], labels, random_pixel, xy, M, cv2.INTER_LINEAR, d_translate)

            # rotation of vectors field
            if nt > 1 and not unet:
                v1 = lbl[n, 6].copy()
                v2 = lbl[n, 5].copy()
                lbl[n, 5] = (-v1 * np.sin(-theta) + v2 * np.cos(-theta))
                lbl[n, 6] = (v1 * np.cos(-theta) + v2 * np.sin(-theta))

    return imgi, lbl, D_crop, S_crop, np.mean(scale)
