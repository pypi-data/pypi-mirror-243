import logging
from datetime import datetime

import matplotlib.pyplot as plt

TORCH_ENABLED = True

from cellpose_omni.models import CellposeModel
from cellpose_omni.io import OMNI_INSTALLED
import torch
from torchvf.losses import ivp_loss

import os, time, datetime
import numpy as np

from scipy.stats import mode
from scipy.ndimage import gaussian_filter, zoom
from tqdm.auto import trange
from cellpose_omni import transforms, utils, io, dynamics
from ..custom_transforms import random_rotate_and_resize
import omnipose
from omnipose.core import masks_to_flows
from torchvision.transforms import GaussianBlur
from cellpose_omni.metrics import average_precision
models_logger = logging.getLogger(__name__)


try:
    import mxnet as mx
    from mxnet import gluon, nd
    from . import resnet_style
    MXNET_ENABLED = True
    mx_GPU = mx.gpu()
    mx_CPU = mx.cpu()
except:
    MXNET_ENABLED = False

try:
    import torch
    from torch.cuda.amp import autocast, GradScaler
    from torch import nn
    from torch.utils import mkldnn as mkldnn_utils
    TORCH_ENABLED = True
    from cellpose_omni.resnet_torch import torch_GPU, torch_CPU, CPnet, ARM
except Exception as e:
    TORCH_ENABLED = False
    print('core.py torch import error',e)

core_logger = logging.getLogger(__name__)
tqdm_out = utils.TqdmToLogger(core_logger, level=logging.INFO)


class CustomCellposeModel(CellposeModel):

    def sparse_omni_loss(self, lbl, y, S_t, D_t):
        """ Loss function for Omnipose with sparse labels.
        Parameters
        --------------
        lbl: ND-array, float
            transformed labels in array [nimg x nchan x xy[0] x xy[1]]
            lbl[:,0] cell masks
            lbl[:,1] thresholded mask layer
            lbl[:,2] boundary field
            lbl[:,3] smooth distance field
            lbl[:,4] boundary-emphasized weights
            lbl[:,5:] flow components

        y:  ND-tensor, float
            network predictions, with dimension D, these are:
            y[:,:D] flow field components at 0,1,...,D-1
            y[:,D] distance fields at D
            y[:,D+1] boundary fields at D+1

        """
        nt = lbl.shape[1]
        cellmask = lbl[:, 1]
        cellmask = self._to_device(cellmask > 0)  # .bool()

        if nt == 2:  # semantic segmentation
            loss1 = self.criterion(y[:, 0] * S_t, cellmask * S_t)  # MSE
            loss2 = self.criterion2(y[:, 0] * S_t, cellmask * S_t)  # BCElogits
            return loss1 + loss2

        else:  # instance segmentation
            cellmask = cellmask.bool()  # acts as a mask now, not output

            # flow components are stored as the last self.dim slices
            veci = self._to_device(lbl[:, 5:])
            dist = lbl[:, 3]  # now distance transform replaces probability
            boundary = lbl[:, 2]

            w = self._to_device(lbl[:, 4])
            dist = self._to_device(dist)
            boundary = self._to_device(boundary)
            flow = y[:, :self.dim]  # 0,1,...self.dim-1
            dt = y[:, self.dim]
            bd = y[:, self.dim + 1]
            a = 10.

            # stacked versions for weighting vector fields with scalars
            wt = torch.stack([w] * self.dim, dim=1)
            ct = torch.stack([cellmask] * self.dim, dim=1)

            # luckily, torch.gradient did exist after all and derivative loss was easy to implement. Could also fix divergenceloss, but I have not been using it.
            # the rest seem good to go.

            loss1 = 10. * self.criterion12(flow * D_t.unsqueeze(1), veci * D_t.unsqueeze(1), wt * D_t.unsqueeze(1))  # weighted MSE
            #         loss2 = self.criterion14(flow,veci,w,cellmask) #ArcCosDotLoss
            #         loss3 = self.criterion11(flow,veci,wt,ct)/a # DerivativeLoss
            #loss4 = 20. * nn.functional.l1_loss(bd * S_t, boundary * S_t)  # BCElogits
            alpha = 0.25
            sigma = 1.
            if sigma == 0:
                loss4 = 20 * (nn.functional.l1_loss((bd - boundary) * S_t, torch.zeros_like(bd)) \
                        + alpha * nn.functional.l1_loss(bd * S_t, torch.zeros_like(bd)))
            else:
                gauss_filter = GaussianBlur((4 * sigma) // 2 * 2 + 1, sigma)
                loss4 = 20 * (nn.functional.l1_loss(gauss_filter((bd - boundary) * S_t), torch.zeros_like(bd)) \
                        + alpha * nn.functional.l1_loss(bd * S_t, torch.zeros_like(bd)))

            loss5 = 2. * self.criterion15(flow * D_t.unsqueeze(1), veci * D_t.unsqueeze(1), w * D_t, (cellmask * D_t).type(torch.cuda.BoolTensor))  # loss on norm
            loss6 = 2. * self.criterion12(dt * D_t, dist * D_t, w * D_t)  # weighted MSE

            """if self.iepoch % 10 == 0:
                plt.imshow(bd[0].tolist())
                plt.colorbar()
                plt.title("epoch %i/%i" % (self.iepoch, self.n_epochs))
                plt.show()
                v_norm = flow[:, 0] ** 2 + flow[:, 1] ** 2
                plt.imshow(v_norm[0].tolist())
                plt.colorbar()
                plt.title("norme de v, epoch %i/%i" % (self.iepoch, self.n_epochs))
                plt.show()
                gt_norm = lbl[:, 5] ** 2 + lbl[:, 6] ** 2
                plt.imshow(gt_norm[0].tolist())
                plt.colorbar()
                plt.title("norme de gradient gt, epoch %i/%i" % (self.iepoch, self.n_epochs))
                plt.show()"""
            #         loss7 = self.criterion11(dt.unsqueeze(1),dist.unsqueeze(1),w.unsqueeze(1),cellmask.unsqueeze(1))/a
            #         loss8 = self.criterion16(flow,veci,cellmask) #divergence loss

            #         # print('loss1',loss1,loss1.type())
            #         # print('loss2',loss2,loss2.type())
            #         # print('loss3',loss3,loss3.type())
            #         # print('loss4',loss4,loss4.type())
            #         # print('loss5',loss5,loss5.type())
            #         # print('loss6',loss6,loss6.type())
            #         # print('loss7',loss7,loss7.type())
            #         return loss1 + loss2 + loss3 + loss4 + loss5 + loss6 + loss7 +loss8

            # dx is the step size, the flow magnitude is for training, so if we want
            # pixels to go 1 unit, should have a step size of 1/5. Might consider
            # doing less than that, but I'm not sure if that will give much benefit.
            # We care about trajectories for about the first three pixels of movement.
            # I may want to rescale by divergence like I do in the real postprocessing, but let's see...
            # it could also be sped up / refined by tracking just what happens to boundary pixels
            dx = 0.2
            steps = int(3 / dx)
            euler_loss = ivp_loss.IVPLoss(dx=dx, n_steps=steps, device=self.device)
            loss9 = euler_loss(flow * D_t.unsqueeze(1), veci * D_t.unsqueeze(1))

            print('flow:%1.2f -- bd:%1.2f -- flow2:%1.2f -- dist:%1.2f -- flow3:%1.2f' % (loss1, loss4, loss5, loss6, loss9))
            # print('loss1',loss1,loss1.type())
            # print('loss4',loss4,loss4.type())
            # print('loss5',loss5,loss5.type())
            # print('loss6',loss6,loss6.type())
            # print('loss9',loss9,loss6.type()) # this is quite a bight higher and more erratic

            # loss9 = self.ivp_loss(flow,veci)
            return loss1 + loss4 + loss5 + loss6 + loss9

    def sparse_cp_loss(self, lbl, y, S_t, D_t):
        """Loss function for Omnipose with sparse labels.
        Parameters
        --------------
        lbl: ND-array, float
            transformed labels in array [nimg x nchan x xy[0] x xy[1]]
            lbl[:,0] cell masks
            lbl[:,1] thresholded mask layer
            lbl[:,2] boundary field
            lbl[:,3] smooth distance field
            lbl[:,4] boundary-emphasized weights
            lbl[:,5:] flow components

        y:  ND-tensor, float
            network predictions, with dimension D, these are:
            y[:,:D] flow field components at 0,1,...,D-1
            y[:,D] distance fields at D
            y[:,D+1] boundary fields at D+1

        """
        veci = 5. * self._to_device(lbl[:, 1:])
        lbl = self._to_device(lbl[:, 0] > .5)
        loss = self.criterion(y[:, :2] * D_t, veci * D_t)
        if self.torch:
            loss /= 2.
        loss2 = self.criterion2(y[:, 2] * S_t, lbl * S_t)
        loss = loss + loss2
        return loss

    def loss_fn(self, lbl, y, S_t, D_t):
        """
        loss function between true labels lbl and prediction y
        This is the one used to train the instance segmentation network.

        """
        if self.omni and OMNI_INSTALLED:  # loss function for omnipose fields
            loss = self.sparse_omni_loss(lbl, y, S_t=S_t, D_t=D_t)
        else:  # original loss function
            loss = self.sparse_cp_loss(lbl, y, S_t=S_t, D_t=D_t)
        return loss

    def _set_optimizer(self, learning_rate, momentum, weight_decay, SGD=False):
        if hasattr(self, "optimizer") is False:
            if self.torch:
                if SGD:
                    self.optimizer = torch.optim.SGD(self.net.parameters(), lr=learning_rate,
                                                momentum=momentum, weight_decay=weight_decay)
                else:
                    import torch_optimizer as optim # for RADAM optimizer
                    self.optimizer = optim.RAdam(self.net.parameters(), lr=learning_rate, betas=(0.95, 0.999), #changed to .95
                                                eps=1e-08, weight_decay=weight_decay)
                    core_logger.info('>>> Using RAdam optimizer')
                    self.optimizer.current_lr = learning_rate
            else:
                self.optimizer = gluon.Trainer(self.net.collect_params(), 'sgd',{'learning_rate': learning_rate,
                                    'momentum': momentum, 'wd': weight_decay})

    @staticmethod
    def gradient_norm(x):
        """ Computation of gradient norm of x.
                Parameters
                --------------
                x: boundaries probabilities (nd array or torch tensor)
                return: gradient_norm(x) (nd array or torch tensor)
                """
        if isinstance(x, np.ndarray):
            g1 = np.zeros_like(x)
            g2 = np.zeros_like(x)
        else:
            g1 = torch.zeros_like(x)
            g2 = torch.zeros_like(x)
        g1[:, 1:, :] = x[:, 1:, :] - x[:, 0:-1, :]
        g2[:, :, 1:] = x[:, :, 1:] - x[:, :, 0:-1]
        ng = g1 ** 2 + g2 ** 2
        return ng

    def _run_cp(self, x, compute_masks=True, normalize=True, invert=False,
                rescale=1.0, net_avg=True, resample=True,
                augment=False, tile=True, tile_overlap=0.1,
                mask_threshold=0.0, diam_threshold=12., flow_threshold=0.4, niter=None, flow_factor=5.0, min_size=15,
                interp=True, cluster=False, boundary_seg=False, affinity_seg=False,
                anisotropy=1.0, do_3D=False, stitch_threshold=0.0,
                omni=False, calc_trace=False, verbose=False):

        tic = time.time()
        shape = x.shape
        nimg = shape[0]
        bd, tr, affinity = None, None, None

        # set up image padding for prediction
        pad = 3
        pad_seq = [(pad,) * 2] * self.dim + [(0,) * 2]  # do not pad channel axis
        unpad = tuple([slice(pad, -pad) if pad else slice(None, None)] * self.dim)  # works in case pad is zero

        if do_3D:
            img = np.asarray(x)
            if normalize or invert:  # possibly make normalize a vector of upper-lower values
                img = transforms.normalize_img(img, invert=invert, omni=omni)

            # have not tested padding in do_3d yet
            # img = np.pad(img,pad_seq,'reflect')

            yf, styles = self._run_3D(img, rsz=rescale, anisotropy=anisotropy,
                                      net_avg=net_avg, augment=augment, tile=tile,
                                      tile_overlap=tile_overlap)
            # unpadding
            # yf = yf[unpad+(Ellipsis,)]

            cellprob = np.sum([yf[k][2] for k in range(3)], axis=0) / 3 if omni else np.sum(
                [yf[k][2] for k in range(3)], axis=0)
            bd = np.sum([yf[k][3] for k in range(3)], axis=0) / 3 if self.nclasses == 4 else np.zeros_like(cellprob)
            dP = np.stack((yf[1][0] + yf[2][0], yf[0][0] + yf[2][1], yf[0][1] + yf[1][1]), axis=0)  # (dZ, dY, dX)
            if omni:
                dP = np.stack([gaussian_filter(dP[a], sigma=1.5) for a in range(3)])  # remove some artifacts
                bd = gaussian_filter(bd, sigma=1.5)
                cellprob = gaussian_filter(cellprob, sigma=1.5)
                dP = dP / 2  # should be averaging components
            del yf
        else:
            tqdm_out = utils.TqdmToLogger(models_logger, level=logging.INFO)
            iterator = trange(nimg, file=tqdm_out) if nimg > 1 else range(nimg)
            styles = np.zeros((nimg, self.nbase[-1]), np.float32)

            # indexing a little weird here due to channels being last now
            if resample:
                s = tuple(shape[-(self.dim + 1):-1])
            else:
                s = tuple(np.round(np.array(shape[-(self.dim + 1):-1]) * rescale).astype(int))

            dP = np.zeros((self.dim, nimg,) + s, np.float32)
            cellprob = np.zeros((nimg,) + s, np.float32)
            bounds = np.zeros((nimg,) + s, bool)

            for i in iterator:
                img = np.asarray(x[i])
                if normalize or invert:
                    img = transforms.normalize_img(img, invert=invert, omni=omni)

                # pad the image to get cleaner output at the edges
                # padding with edge values seems to work the best
                img = np.pad(img, pad_seq, 'edge')

                if rescale != 1.0:
                    # if self.dim>2:
                    #     print('WARNING, resample not updated for ND')
                    # img = transforms.resize_image(img, rsz=rescale)

                    if img.ndim > self.dim:  # then there is a channel axis, assume it is last here
                        img = np.stack([zoom(img[..., k], rescale, order=3) for k in range(img.shape[-1])], axis=-1)
                    else:
                        img = zoom(img, rescale, order=1)

                yf, style = self._run_nets(img, net_avg=net_avg,
                                           augment=augment, tile=tile,
                                           tile_overlap=tile_overlap)
                # unpadding
                yf = yf[unpad + (Ellipsis,)]

                # resample interpolates the network output to native resolution prior to running Euler integration
                # this means the masks will have no scaling artifacts. We could *upsample* by some factor to make
                # the clustering etc. work even better, but that is not implemented yet
                if resample:
                    # ND version actually gives better results than CV2 in some places.
                    yf = np.stack([zoom(yf[..., k], shape[1:1 + self.dim] / np.array(yf.shape[:2]), order=1)
                                   for k in range(yf.shape[-1])], axis=-1)
                    # scipy.ndimage.affine_transform(A, np.linalg.inv(M), output_shape=tyx,

                if self.nclasses > 1:
                    cellprob[i] = yf[..., self.dim]  # scalar field always after the vector field output
                    order = (self.dim,) + tuple([k for k in range(self.dim)])  # (2,0,1)
                    dP[:, i] = yf[..., :self.dim].transpose(order)
                else:
                    cellprob[i] = yf[..., 0]
                    # dP[i] =  np.zeros(cellprob)

                if self.nclasses >= 4:
                    if i == 0:
                        bd = np.zeros_like(cellprob)
                    bd[i] = yf[..., self.dim + 1]

                styles[i] = style
            del yf, style
        styles = styles.squeeze()

        net_time = time.time() - tic
        if nimg > 1:
            models_logger.info('network run in %2.2fs' % (net_time))

        # turn bd into gradient norm of bd instead
        bd = self.gradient_norm(bd)

        if compute_masks:
            tic = time.time()

            # allow user to specify niter
            # Cellpose default is 200
            # Omnipose default is None (dynamically adjusts based on distance field)
            if niter is None and not omni:
                niter = 200 if (do_3D and not resample) else (1 / rescale * 200)

            if do_3D:
                if not (omni and OMNI_INSTALLED):
                    # run cellpose compute_masks
                    masks, bounds, p, tr = dynamics.compute_masks(dP, cellprob, bd,
                                                                  niter=niter,
                                                                  resize=None,
                                                                  mask_threshold=mask_threshold,
                                                                  diam_threshold=diam_threshold,
                                                                  flow_threshold=flow_threshold,
                                                                  interp=interp,
                                                                  do_3D=do_3D,
                                                                  min_size=min_size,
                                                                  verbose=verbose,
                                                                  use_gpu=self.gpu,
                                                                  device=self.device,
                                                                  nclasses=self.nclasses,
                                                                  calc_trace=calc_trace)
                    affinity = []
                else:
                    # run omnipose compute_masks
                    masks, bounds, p, tr, affinity = omnipose.core.compute_masks(dP, cellprob, bd,
                                                                                 do_3D=do_3D,
                                                                                 niter=niter,
                                                                                 resize=None,
                                                                                 min_size=min_size,
                                                                                 mask_threshold=mask_threshold,
                                                                                 diam_threshold=diam_threshold,
                                                                                 flow_threshold=flow_threshold,
                                                                                 flow_factor=flow_factor,
                                                                                 interp=interp,
                                                                                 cluster=cluster,
                                                                                 boundary_seg=boundary_seg,
                                                                                 affinity_seg=affinity_seg,
                                                                                 calc_trace=calc_trace,
                                                                                 verbose=verbose,
                                                                                 use_gpu=self.gpu,
                                                                                 device=self.device,
                                                                                 nclasses=self.nclasses,
                                                                                 dim=self.dim)
            else:
                masks, bounds, p, tr, affinity = [], [], [], [], []
                resize = shape[-(self.dim + 1):-1] if not resample else None
                # print('compute masks 2',resize,shape,resample)
                for i in iterator:
                    if not (omni and OMNI_INSTALLED):
                        # run cellpose compute_masks
                        outputs = dynamics.compute_masks(dP[:, i], cellprob[i], niter=niter,
                                                         mask_threshold=mask_threshold,
                                                         flow_threshold=flow_threshold,
                                                         interp=interp,
                                                         resize=resize,
                                                         verbose=verbose,
                                                         use_gpu=self.gpu,
                                                         device=self.device,
                                                         nclasses=self.nclasses,
                                                         calc_trace=calc_trace)
                        outputs = outputs + ([],)  # affinity placeholder
                    else:
                        # run omnipose compute_masks

                        # important: resampling means that pixels need to go farther to cluser together;
                        # niter should be determined by dist, first of all; it currently is already scaled for resampling, good!
                        # dP needs to be scaled for magnitude to get pixels to move the same relative distance
                        # eps probably should be left the same if the above are changed
                        # if resample:
                        #     print('rescale is',rescale,resize)
                        # dP[:,i] /= rescale this does nothign here since I normalize the flow anyway, have to pass in

                        bdi = bd[i] if bd is not None else None
                        outputs = omnipose.core.compute_masks(dP[:, i], cellprob[i], bdi,
                                                              niter=niter,
                                                              rescale=rescale,
                                                              resize=resize,
                                                              min_size=min_size,
                                                              mask_threshold=mask_threshold,
                                                              diam_threshold=diam_threshold,
                                                              flow_threshold=flow_threshold,
                                                              flow_factor=flow_factor,
                                                              interp=interp,
                                                              cluster=cluster,
                                                              boundary_seg=boundary_seg,
                                                              affinity_seg=affinity_seg,
                                                              calc_trace=calc_trace,
                                                              verbose=verbose,
                                                              use_gpu=self.gpu,
                                                              device=self.device,
                                                              nclasses=self.nclasses,
                                                              dim=self.dim)
                    masks.append(outputs[0])
                    p.append(outputs[1])
                    tr.append(outputs[2])
                    bounds.append(outputs[3])
                    affinity.append(outputs[4])

                masks = np.array(masks)
                bounds = np.array(bounds)
                p = np.array(p)
                tr = np.array(tr)
                affinity = np.array(affinity)

                if stitch_threshold > 0 and nimg > 1:
                    models_logger.info(
                        f'stitching {nimg} planes using stitch_threshold={stitch_threshold:0.3f} to make 3D masks')
                    masks = utils.stitch3D(masks, stitch_threshold=stitch_threshold)

            flow_time = time.time() - tic
            if nimg > 1:
                models_logger.info('masks created in %2.2fs' % (flow_time))

            ret = [masks, styles, dP, cellprob, p, bd, tr, affinity, bounds]
            ret = [r.squeeze() if r is not None else r for r in ret]

        else:
            # pass back zeros if not compute_masks
            ret = [np.zeros(0)] * 9

        return (*ret,)

    def train(self, train_data, train_labels, train_D_t, train_S_t, train_links=None, train_files=None,
              test_data=None, test_labels=None, test_links=None, test_files=None,
              channels=None, channel_axis=0, normalize=True,
              save_path=None, save_every=100, save_each=False,
              learning_rate=0.2, n_epochs=500, momentum=0.9, SGD=True,
              weight_decay=0.00001, batch_size=8, nimg_per_epoch=None,
              rescale=True, min_train_masks=5, netstr=None, tyx=None, multi_threading=True,
              cp_data_aug=False):

        """ train network with images train_data

            Parameters
            ------------------

            train_data: list of arrays (2D or 3D)
                images for training

            train_labels: list of arrays (2D or 3D)
                labels for train_data, where 0=no masks; 1,2,...=mask labels
                can include flows as additional images

            train_D_t: list of arrays (2D or 3D)
                mask of admissible area where to compute distance map

            train_S_t: list of arrays (2D or 3D)
                mask of admissible area where to minimize loss on labels

            train_links: list of label links
                These lists of label pairs define which labels are "linked",
                i.e. should be treated as part of the same object. This is how
                Omnipose handles internal/self-contact boundaries during training.

            train_files: list of strings
                file names for images in train_data (to save flows for future runs)

            test_data: list of arrays (2D or 3D)
                images for testing

            test_labels: list of arrays (2D or 3D)
                See train_labels.

            test_links: list of label links
                See train_links.

            test_files: list of strings
                file names for images in test_data (to save flows for future runs)

            channels: list of ints (default, None)
                channels to use for training

            normalize: bool (default, True)
                normalize data so 0.0=1st percentile and 1.0=99th percentile of image intensities in each channel

            save_path: string (default, None)
                where to save trained model, if None it is not saved

            save_every: int (default, 100)
                save network every [save_every] epochs

            learning_rate: float or list/np.ndarray (default, 0.2)
                learning rate for training, if list, must be same length as n_epochs

            n_epochs: int (default, 500)
                how many times to go through whole training set during training

            weight_decay: float (default, 0.00001)

            SGD: bool (default, True)
                use SGD as optimization instead of RAdam

            batch_size: int (optional, default 8)
                number of tyx-sized patches to run simultaneously on the GPU
                (can make smaller or bigger depending on GPU memory usage)

            nimg_per_epoch: int (optional, default None)
                minimum number of images to train on per epoch,
                with a small training set (< 8 images) it may help to set to 8

            rescale: bool (default, True)
                whether or not to rescale images to diam_mean during training,
                if True it assumes you will fit a size model after training or resize your images accordingly,
                if False it will try to train the model to be scale-invariant (works worse)

            min_train_masks: int (default, 5)
                minimum number of masks an image must have to use in training set

            netstr: str (default, None)
                name of network, otherwise saved with name as params + training start time

            tyx: int, tuple (default, 224x224 in 2D)
                size of image patches used for training

            multi_threading: bool
                whether to compute using multithreading or not
            cp_data_aug: bool
                whether to use or not Cellpose data augmentation for Omnipose to avoid recomputing
                flows on the fly and make it faster
        """
        # loss list to plot
        loss_list = []
        if rescale:
            models_logger.info(f'Training with rescale = {rescale:.2f}')
        # images may need some dimension shuffling to conform to standard, this is link-independent

        train_data, train_labels, _, _, run_test = transforms.reshape_train_test(train_data,
                                                                                                   train_labels,
                                                                                                   [],
                                                                                                   [],
                                                                                                   channels,
                                                                                                   channel_axis,
                                                                                                   normalize,
                                                                                                   self.dim, self.omni)
        # check if train_labels have flows
        # if not, flows computed, returned with labels as train_flows[i][0]
        labels_to_flows = dynamics.labels_to_flows if not (
                    self.omni and OMNI_INSTALLED) else omnipose.core.labels_to_flows

        # Omnipose needs to recompute labels on-the-fly after image warping
        if self.omni and OMNI_INSTALLED:
            models_logger.info('No precomuting flows with Omnipose. Computed during training.')

            # We assume that if links are given, labels are properly formatted as 0,1,2,...,N
            # might be worth implementing a remapping for the links just in case...
            if train_links is None:
                train_labels = [omnipose.utils.format_labels(label) for label in train_labels]

            if cp_data_aug:
                train_labels = [masks_to_flows(l, omni=self.omni, device=self.device, dim=self.dim,
                                               use_gpu=self.gpu) for l in train_labels]
                nmasks = np.array([label[0].max() for label in train_labels])
            else:
                # nmasks is inflated when using multi-label objects, so keep that in mind if you care about min_train_masks
                nmasks = np.array([label.max() for label in train_labels])

        else:
            train_labels = labels_to_flows(train_labels, train_links, files=train_files, use_gpu=self.gpu,
                                           device=self.device, dim=self.dim)
            nmasks = np.array([label[0].max() for label in train_labels])

        """if run_test:
            test_labels = labels_to_flows(test_labels, test_links, files=test_files, use_gpu=self.gpu,
                                          device=self.device, dim=self.dim)
        else:
            test_labels = None"""

        nremove = (nmasks < min_train_masks).sum()
        if nremove > 0:
            models_logger.warning(
                f'{nremove} train images with number of masks less than min_train_masks ({min_train_masks}), removing from train set')
            ikeep = np.nonzero(nmasks >= min_train_masks)[0]
            train_data = [train_data[i] for i in ikeep]
            train_labels = [train_labels[i] for i in ikeep]

        if channels is None:
            models_logger.warning('channels is set to None, input must therefore have nchan channels (default is 2)')

        if multi_threading is False:
            model_path = self._train_net(train_data, train_labels, train_D_t, train_S_t, train_links,
                                         test_data=test_data, test_labels=test_labels, test_links=test_links,
                                         save_path=save_path, save_every=save_every, save_each=save_each,
                                         learning_rate=learning_rate, n_epochs=n_epochs,
                                         momentum=momentum, weight_decay=weight_decay,
                                         SGD=SGD, batch_size=batch_size, nimg_per_epoch=nimg_per_epoch,
                                         rescale=rescale, netstr=netstr, tyx=tyx)
        else:
            # Dirty version of _train_net to be able to yield epochs nb for the multi threading
            d = datetime.datetime.now()
            self.autocast = False
            self.n_epochs = n_epochs
            if isinstance(learning_rate, (list, np.ndarray)):
                if isinstance(learning_rate, np.ndarray) and learning_rate.ndim > 1:
                    raise ValueError('learning_rate.ndim must equal 1')
                elif len(learning_rate) != n_epochs:
                    raise ValueError('if learning_rate given as list or np.ndarray it must have length n_epochs')
                self.learning_rate = learning_rate
                self.learning_rate_const = mode(learning_rate)[0][0]
            else:
                self.learning_rate_const = learning_rate
                # Omnipose way to schedule LR
                """# set learning rate schedule
                if SGD:
                    LR = np.linspace(0, self.learning_rate_const, 10)
                    if self.n_epochs > 250:
                        LR = np.append(LR, self.learning_rate_const * np.ones(self.n_epochs - 100))
                        for i in range(10):
                            LR = np.append(LR, LR[-1] / 2 * np.ones(10))
                    else:
                        LR = np.append(LR, self.learning_rate_const * np.ones(max(0, self.n_epochs - 10)))
                else:
                    LR = self.learning_rate_const * np.ones(self.n_epochs)
                self.learning_rate = LR"""

                """# Replacement of LR scheduler by REX (https://arxiv.org/abs/2107.04197)
                self.learning_rate = self.rex_scheduler()
                plt.plot(range(1, self.n_epochs + 1), self.learning_rate)
                plt.xlabel('Epochs')
                plt.ylabel('Learning rate')
                plt.title('Scheduler REX - LR along epochs')
                plt.show()"""

                # if training is resumed, must relaunch from last epoch not to erase older weights

                if self.pretrained_model is False:
                    current_iepoch = 0
                else:
                    current_iepoch = int(self.pretrained_model[0].split("_")[-1]) + 1

                self.learning_rate = self.generate_learning_rates(learning_rate, current_iepoch, n_epochs)

                plt.plot(range(1, len(self.learning_rate) + 1), self.learning_rate)
                plt.xlabel('Epochs')
                plt.ylabel('Learning rate')
                plt.title('Scheduler - LR along epochs')
                plt.show()

            self.batch_size = batch_size
            self._set_optimizer(self.learning_rate[0], momentum, weight_decay, SGD)
            self._set_criterion()

            nimg = len(train_data)

            # debug
            # for k in range(len(train_labels)):
            #     print('ggg',train_labels[k][0].shape, np.unique(train_labels[k][0]))

            # compute average cell diameter
            if rescale:
                if train_links is not None:
                    core_logger.warning("""WARNING: rescaling not updated for multi-label objects. 
                                                Check rescaling manually for the right diameter.""")

                if cp_data_aug:
                    diam_train = np.array([utils.diameters(train_labels[k][0], omni=self.omni)[0]
                                       for k in range(len(train_labels))])
                else:
                    diam_train = np.array([utils.diameters(train_labels[k], omni=self.omni)[0]
                                           for k in range(len(train_labels))])
                diam_train[diam_train < 5] = 5.
                if test_data is not None:
                    diam_test = np.array([utils.diameters(test_labels[k], omni=self.omni)[0]
                                          for k in range(len(test_labels))])
                    diam_test[diam_test < 5] = 5.
                scale_range = 0.5
                core_logger.info('>>>> median diameter set to = %d' % self.diam_mean)
            else:
                scale_range = 1.0

            nchan = train_data[0].shape[0]
            core_logger.info('>>>> training network with %d channel input <<<<' % nchan)
            core_logger.info('>>>> LR: %0.5f, batch_size: %d, weight_decay: %0.5f' % (
                self.learning_rate_const, self.batch_size, weight_decay))

            if test_data is not None:
                core_logger.info(f'>>>> ntrain = {nimg}, ntest = {len(test_data)}')
            else:
                core_logger.info(f'>>>> ntrain = {nimg}')

            tic = time.time()

            lavg, nsum = 0, 0

            if save_path is not None:
                _, file_label = os.path.split(save_path)
                file_path = os.path.join(save_path, 'models/')

                # if not os.path.exists(file_path):
                #     os.makedirs(file_path)
                io.check_dir(file_path)
            else:
                core_logger.warning('WARNING: no save_path given, model not saving')

            ksave = 0
            rsc = 1.0

            # cannot train with mkldnn
            self.net.mkldnn = False

            # get indices for each epoch for training
            np.random.seed(0)
            inds_all = np.zeros((0,), 'int32')

            if nimg < batch_size:
                nimg_per_epoch = batch_size
            else:
                nimg_per_epoch = nimg
            """# mandatory to change it, otherwise in a frugal configuration, batch_size is gonna be to little
            nimg_per_epoch = nimg
            if nimg_per_epoch < batch_size:
                nimg_per_epoch = batch_size"""
            core_logger.info(f'>>>> nimg_per_epoch = {nimg_per_epoch}')
            while len(inds_all) < n_epochs * nimg_per_epoch:
                rperm = np.random.permutation(nimg)
                inds_all = np.hstack((inds_all, rperm))

            if self.autocast:
                self.scaler = GradScaler()

            for iepoch in range(current_iepoch, self.n_epochs):
                if SGD:
                    self._set_learning_rate(self.learning_rate[iepoch])
                np.random.seed(iepoch)
                rperm = inds_all[iepoch * nimg_per_epoch:(iepoch + 1) * nimg_per_epoch]
                for ibatch in range(0, nimg_per_epoch, batch_size):
                    inds = rperm[ibatch:ibatch + batch_size]
                    rsc = diam_train[inds] / self.diam_mean if rescale else np.ones(len(inds), np.float32)
                    # now passing in the full train array, need the labels for distance field
                    st0 = np.random.get_state()

                    self.iepoch = iepoch
                    imgi, lbl, D_ti, S_ti, scale = random_rotate_and_resize([train_data[i] for i in inds],
                                                                                              [train_labels[i] for i in
                                                                                               inds],
                                                                                              [train_D_t[i] for i in inds],
                                                                                              [train_S_t[i] for i in inds],
                                                                                              links=None if train_links is None else [
                                                                                                  train_links[i] for i in
                                                                                                  inds],
                                                                                              rescale=rsc,
                                                                                              scale_range=scale_range,
                                                                                              unet=self.unet,
                                                                                              tyx=tyx,
                                                                                              inds=inds,
                                                                                              omni=self.omni,
                                                                                              dim=self.dim,
                                                                                              nchan=self.nchan,
                                                                                              nclasses=self.nclasses,
                                                                                              cp_data_aug=cp_data_aug)

                    """plt.imshow(imgi[0, 0, :, :]); plt.show()
                    plt.imshow(D_ti[0, :]); plt.show()
                    plt.imshow(S_ti[0, :]); plt.show()"""

                    S_ti = torch.asarray(S_ti).to("cuda")
                    D_ti = torch.asarray(D_ti).to("cuda")

                    if self.unet and lbl.shape[1] > 1 and rescale:
                        lbl[:, 1] /= diam_batch[:, np.newaxis, np.newaxis] ** 2
                    train_loss = self._train_step(imgi, lbl, D_t=D_ti, S_t=S_ti)
                    lavg += train_loss
                    nsum += len(imgi)

                # loss to plot
                loss_list.append(lavg / nsum)
                # send epoch value to progress bar
                #yield (iepoch + 1, loss_list, self)


                if save_path is not None:
                    if iepoch == self.n_epochs - 1 or iepoch % save_every == 1 or save_every == 1:
                        # save model at the end
                        if save_each:  # separate files as model progresses
                            if netstr is None:
                                file_name = '{}_{}_{}_{}'.format(self.net_type, file_label,
                                                                 d.strftime("%Y_%m_%d_%H_%M_%S.%f"),
                                                                 'epoch_' + str(iepoch))
                            else:
                                file_name = '{}_{}'.format(netstr, 'epoch_' + str(iepoch))
                        else:
                            if netstr is None:
                                file_name = '{}_{}_{}'.format(self.net_type, file_label, d.strftime("%Y_%m_%d_%H_%M_%S.%f"))
                            else:
                                file_name = netstr
                        file_name = os.path.join(file_path, file_name)
                        ksave += 1
                        core_logger.info(f'saving network parameters to {file_name}')

                        # self.net.save_model(file_name)
                        # whether or not we are using dataparallel
                        # this logic appears elsewhere in models.py
                        if self.torch and self.gpu:
                            self.net.module.save_model(file_name)
                        else:
                            self.net.save_model(file_name)

                else:
                    file_name = save_path

                self.pretrained_model = file_name
                if iepoch % 40 == 0 or iepoch == 499:
                    lavg = lavg / nsum
                    iou_thresholds = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.85, 0.9]
                    ap0 = []
                    if test_data is not None:
                        diam_test = np.array([utils.diameters(test_labels[k], omni=True)[0]
                                              for k in range(len(test_labels))])
                        res_test = self.eval(test_data[:10], diameter=diam_test, flow_threshold=0, cellprob_threshold=None,
                                             channels=[2, 1], omni=self.omni, channel_axis=2)[0]
                        ap = average_precision(test_labels[:10], res_test, iou_thresholds)[0]
                        plt.imshow(res_test[0]); plt.title("res"); plt.colorbar(); plt.show()
                        plt.imshow(test_labels[0]); plt.title("labels"); plt.colorbar(); plt.show()
                        ap0.append(list(ap.mean(axis=0)))


                        plt.plot(iou_thresholds, ap.mean(axis=0), label="epoch : " + str(self.iepoch))

                        plt.legend()

                        plt.xlabel("IoU matching threshold")
                        plt.ylabel("Average Precision")

                        # Affichez le graphique
                        plt.show()


            # reset to mkldnn if available
            self.net.mkldnn = self.mkldnn

            model_path = file_name
        self.pretrained_model = model_path
        return model_path, loss_list

    def rex_scheduler(self):
        LR = []
        for t in range(0, self.n_epochs):
            LR.append(self.learning_rate_const * ((1 - (t / self.n_epochs)) / (0.5 + 0.5 * (1 - (t / self.n_epochs)))))
        return LR

    def _train_step(self, x, lbl, D_t, S_t):
        """plt.imshow(x[0, 0, :, :])
        plt.title("Patch")
        plt.show()
        plt.imshow(lbl[0, 0, :])
        plt.title("labels")
        plt.show()
        plt.imshow(D_t[0, :].cpu().numpy())
        plt.title("D")
        plt.show()
        plt.imshow(S_t[0, :].cpu().numpy())
        plt.title("S")
        plt.show()"""
        X = self._to_device(x)
        if self.torch:
            self.optimizer.zero_grad()
            self.net.train()

            if self.autocast:
                with autocast():
                    y = self.net(X)[0]
                    # The network output is now the gradient norm of the boundaries field
                    y[:, 3] = self.gradient_norm(y[:, 3])
                    del X
                    loss = self.loss_fn(lbl, y, D_t=D_t, S_t=S_t)
                self.scaler.scale(loss).backward()
                train_loss = loss.item()
                self.scaler.step(self.optimizer)
                train_loss *= len(x)
                self.scaler.update()
            else:
                y = self.net(X)[0]
                """
                MEMO
                y:  ND-tensor, float
                    network predictions, with dimension D, these are:
                    y[:,:D] flow field components at 0,1,...,D-1
                    y[:,D] distance fields at D
                    y[:,D+1] boundary fields at D+1
                """
                # The network output is now the gradient norm of the boundaries field
                y[:, 3] = self.gradient_norm(y[:, 3])
                del X
                loss = self.loss_fn(lbl, y, D_t=D_t, S_t=S_t)
                loss.backward()
                train_loss = loss.item()
                self.optimizer.step()
                train_loss *= len(x)
        else:
            with mx.autograd.record():
                y = self.net(X)[0]
                # The network output is now the gradient norm of the boundaries field
                y[:, 3] = self.gradient_norm(y[:, 3])
                del X
                loss = self.loss_fn(lbl, y, D_t=D_t, S_t=S_t)
            loss.backward()
            train_loss = nd.sum(loss).asscalar()
            self.optimizer.step(x.shape[0])
        return train_loss

    def _test_eval(self, x, lbl, D_t, S_t):
        X = self._to_device(x)
        if self.torch:
            self.net.eval()
            with torch.no_grad():
                y, style = self.net(X)
                del X
                loss = self.loss_fn(lbl, y, D_t, S_t)
                test_loss = loss.item()
                test_loss *= len(x)
        else:
            y, style = self.net(X)
            del X
            loss = self.loss_fn(lbl, y, D_t, S_t)
            test_loss = nd.sum(loss).asnumpy()
        return test_loss

    @staticmethod
    def generate_learning_rates(init_lr, current_iepoch, max_epochs):
        learning_rates = []

        for epoch in range(current_iepoch, max_epochs):
            if epoch < max_epochs / 2:
                lr = init_lr
            elif epoch < 0.975 * max_epochs:
                lr = init_lr / 10
            else:
                lr = init_lr / 100
            learning_rates.append(lr)

        return learning_rates

    def _train_net(self, train_data, train_labels, train_D_t, train_S_t, train_links, test_data=None, test_labels=None,
                   test_links=None, save_path=None, save_every=100, save_each=False,
                   learning_rate=0.2, n_epochs=500, momentum=0.9, weight_decay=0.00001,
                   SGD=True, batch_size=8, nimg_per_epoch=None, rescale=True, netstr=None,
                   do_autocast=False, tyx=None):
        """ train function uses loss function self.loss_fn in models.py"""

        d = datetime.datetime.now()
        self.autocast = do_autocast
        self.n_epochs = n_epochs
        if isinstance(learning_rate, (list, np.ndarray)):
            if isinstance(learning_rate, np.ndarray) and learning_rate.ndim > 1:
                raise ValueError('learning_rate.ndim must equal 1')
            elif len(learning_rate) != n_epochs:
                raise ValueError('if learning_rate given as list or np.ndarray it must have length n_epochs')
            self.learning_rate = learning_rate
            self.learning_rate_const = mode(learning_rate)[0][0]
        else:
            self.learning_rate_const = learning_rate
            # set learning rate schedule
            if SGD:
                LR = np.linspace(0, self.learning_rate_const, 10)
                if self.n_epochs > 250:
                    LR = np.append(LR, self.learning_rate_const * np.ones(self.n_epochs - 100))
                    for i in range(10):
                        LR = np.append(LR, LR[-1] / 2 * np.ones(10))
                else:
                    LR = np.append(LR, self.learning_rate_const * np.ones(max(0, self.n_epochs - 10)))
            else:
                LR = self.learning_rate_const * np.ones(self.n_epochs)
            self.learning_rate = LR

        self.batch_size = batch_size
        self._set_optimizer(self.learning_rate[0], momentum, weight_decay, SGD)
        self._set_criterion()

        nimg = len(train_data)

        # debug
        # for k in range(len(train_labels)):
        #     print('ggg',train_labels[k][0].shape, np.unique(train_labels[k][0]))

        # compute average cell diameter
        if rescale:
            if train_links is not None:
                core_logger.warning("""WARNING: rescaling not updated for multi-label objects. 
                                    Check rescaling manually for the right diameter.""")

            diam_train = np.array([utils.diameters(train_labels[k], omni=self.omni)[0]
                                   for k in range(len(train_labels))])
            diam_train[diam_train < 5] = 5.
            if test_data is not None:
                diam_test = np.array([utils.diameters(test_labels[k], omni=self.omni)[0]
                                      for k in range(len(test_labels))])
                diam_test[diam_test < 5] = 5.
            scale_range = 0.5
            core_logger.info('>>>> median diameter set to = %d' % self.diam_mean)
        else:
            scale_range = 1.0

        nchan = train_data[0].shape[0]
        core_logger.info('>>>> training network with %d channel input <<<<' % nchan)
        core_logger.info('>>>> LR: %0.5f, batch_size: %d, weight_decay: %0.5f' % (
        self.learning_rate_const, self.batch_size, weight_decay))

        if test_data is not None:
            core_logger.info(f'>>>> ntrain = {nimg}, ntest = {len(test_data)}')
        else:
            core_logger.info(f'>>>> ntrain = {nimg}')

        tic = time.time()

        lavg, nsum = 0, 0

        if save_path is not None:
            _, file_label = os.path.split(save_path)
            file_path = os.path.join(save_path, 'models/')

            # if not os.path.exists(file_path):
            #     os.makedirs(file_path)
            io.check_dir(file_path)
        else:
            core_logger.warning('WARNING: no save_path given, model not saving')

        ksave = 0
        rsc = 1.0

        # cannot train with mkldnn
        self.net.mkldnn = False

        # get indices for each epoch for training
        np.random.seed(0)
        inds_all = np.zeros((0,), 'int32')
        if nimg_per_epoch is None or nimg > nimg_per_epoch:
            nimg_per_epoch = nimg
        core_logger.info(f'>>>> nimg_per_epoch = {nimg_per_epoch}')
        while len(inds_all) < n_epochs * nimg_per_epoch:
            rperm = np.random.permutation(nimg)
            inds_all = np.hstack((inds_all, rperm))

        if self.autocast:
            self.scaler = GradScaler()

        for iepoch in range(self.n_epochs):
            if SGD:
                self._set_learning_rate(self.learning_rate[iepoch])
            np.random.seed(iepoch)
            rperm = inds_all[iepoch * nimg_per_epoch:(iepoch + 1) * nimg_per_epoch]
            for ibatch in range(0, nimg_per_epoch, batch_size):
                inds = rperm[ibatch:ibatch + batch_size]
                rsc = diam_train[inds] / self.diam_mean if rescale else np.ones(len(inds), np.float32)
                # now passing in the full train array, need the labels for distance field
                st0 = np.random.get_state()


                imgi, lbl, D_ti, S_ti, scale = random_rotate_and_resize([train_data[i] for i in inds],
                                                                              [train_labels[i] for i in inds],
                                                                              [train_D_t[i] for i in inds],
                                                                              [train_S_t[i] for i in inds],
                                                                              links=None if train_links is None else [
                                                                              train_links[i] for i in inds],
                                                                              rescale=rsc,
                                                                              scale_range=scale_range,
                                                                              unet=self.unet,
                                                                              tyx=tyx,
                                                                              inds=inds,
                                                                              omni=self.omni,
                                                                              dim=self.dim,
                                                                              nchan=self.nchan,
                                                                              nclasses=self.nclasses)

                """plt.imshow(imgi[0, 0, :, :]); plt.show()
                plt.imshow(D_ti[0, :]); plt.show()
                plt.imshow(S_ti[0, :]); plt.show()"""


                S_ti = torch.asarray(S_ti).to("cuda")
                D_ti = torch.asarray(D_ti).to("cuda")


                if self.unet and lbl.shape[1] > 1 and rescale:
                    lbl[:, 1] /= diam_batch[:, np.newaxis, np.newaxis] ** 2
                train_loss = self._train_step(imgi, lbl, D_ti, S_ti)
                lavg += train_loss
                nsum += len(imgi)

            if iepoch % 10 == 0 or iepoch == 5:
                lavg = lavg / nsum
                if test_data is not None:
                    lavgt, nsum = 0., 0
                    np.random.seed(42)
                    rperm = np.arange(0, len(test_data), 1, int)
                    for ibatch in range(0, len(test_data), batch_size):
                        inds = rperm[ibatch:ibatch + batch_size]
                        rsc = diam_test[inds] / self.diam_mean if rescale else np.ones(len(inds), np.float32)
                        imgi, lbl, scale = transforms.random_rotate_and_resize([test_data[i] for i in inds],
                                                                               Y=[test_labels[i] for i in inds],
                                                                               links=[test_links[i] for i in inds],
                                                                               rescale=rsc,
                                                                               scale_range=0.,
                                                                               unet=self.unet,
                                                                               tyx=tyx,
                                                                               inds=inds,
                                                                               omni=self.omni,
                                                                               dim=self.dim,
                                                                               nchan=self.nchan,
                                                                               nclasses=self.nclasses)
                        if self.unet and lbl.shape[1] > 1 and rescale:
                            lbl[:, 1] *= scale[0] ** 2

                        test_loss = self._test_eval(imgi, lbl, D_t, S_t)
                        lavgt += test_loss
                        nsum += len(imgi)

                    core_logger.info('Epoch %d, Time %4.1fs, Loss %2.4f, Loss Test %2.4f, LR %2.4f' %
                                     (iepoch, time.time() - tic, lavg, lavgt / nsum, self.learning_rate[iepoch]))
                else:
                    core_logger.info('Epoch %d, Time %4.1fs, Loss %2.4f, LR %2.4f' %
                                     (iepoch, time.time() - tic, lavg, self.learning_rate[iepoch]))

                lavg, nsum = 0, 0

            if save_path is not None:
                if iepoch == self.n_epochs - 1 or iepoch % save_every == 1:
                    # save model at the end
                    if save_each:  # separate files as model progresses
                        if netstr is None:
                            file_name = '{}_{}_{}_{}'.format(self.net_type, file_label,
                                                             d.strftime("%Y_%m_%d_%H_%M_%S.%f"),
                                                             'epoch_' + str(iepoch))
                        else:
                            file_name = '{}_{}'.format(netstr, 'epoch_' + str(iepoch))
                    else:
                        if netstr is None:
                            file_name = '{}_{}_{}'.format(self.net_type, file_label, d.strftime("%Y_%m_%d_%H_%M_%S.%f"))
                        else:
                            file_name = netstr
                    file_name = os.path.join(file_path, file_name)
                    ksave += 1
                    core_logger.info(f'saving network parameters to {file_name}')

                    # self.net.save_model(file_name)
                    # whether or not we are using dataparallel
                    # this logic appears elsewhere in models.py
                    if self.torch and self.gpu:
                        self.net.module.save_model(file_name)
                    else:
                        self.net.save_model(file_name)

            else:
                file_name = save_path

        # reset to mkldnn if available
        self.net.mkldnn = self.mkldnn

        return file_name

