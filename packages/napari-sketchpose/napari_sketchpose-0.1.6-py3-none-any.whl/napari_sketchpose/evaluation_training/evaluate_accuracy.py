import matplotlib.pyplot as plt

from napari_sketchpose.Custom_cellpose_omni import CustomCellposeModel
from omnipose.core import diameters
import os
from skimage.io import imread
import numpy as np
from cellpose_omni import utils, metrics
import pandas as pd

"""
This code compute the average precision over a list of test images for
several trained models
"""


def average_precision(masks_true, masks_pred, threshold=[0.5, 0.75, 0.9]):
    """ average precision estimation: AP = TP / (TP + FP + FN)

    This function is based heavily on the *fast* stardist matching functions
    (https://github.com/mpicbg-csbd/stardist/blob/master/stardist/matching.py)

    Parameters
    ------------

    masks_true: list of ND-arrays (int) or ND-array (int)
        where 0=NO masks; 1,2... are mask labels
    masks_pred: list of ND-arrays (int) or ND-array (int)
        ND-array (int) where 0=NO masks; 1,2... are mask labels

    Returns
    ------------

    ap: array [len(masks_true) x len(threshold)]
        average precision at thresholds
    tp: array [len(masks_true) x len(threshold)]
        number of true positives at thresholds
    fp: array [len(masks_true) x len(threshold)]
        number of false positives at thresholds
    fn: array [len(masks_true) x len(threshold)]
        number of false negatives at thresholds

    """
    not_list = False
    if not isinstance(masks_true, list):
        masks_true = [masks_true]
        masks_pred = [masks_pred]
        not_list = True
    if not isinstance(threshold, list) and not isinstance(threshold, np.ndarray):
        threshold = [threshold]
    ap = np.zeros((len(masks_true), len(threshold)), np.float32)
    tp = np.zeros((len(masks_true), len(threshold)), np.float32)
    fp = np.zeros((len(masks_true), len(threshold)), np.float32)
    fn = np.zeros((len(masks_true), len(threshold)), np.float32)
    n_true = np.array([len(np.unique(mask)) - 1 for mask in masks_true])
    n_pred = np.array([len(np.unique(mask)) - 1 for mask in masks_pred])
    #     if len(n_pred) < 1:
    #         n_pred = [0]
    for n in range(len(masks_true)):
        # _,mt = np.reshape(np.unique(masks_true[n], return_index=True), masks_pred[n].shape)
        if n_pred[n] > 0:
            iou = metrics._intersection_over_union(masks_true[n], masks_pred[n])[1:, 1:]
            for k, th in enumerate(threshold):
                tp[n, k] = metrics._true_positive(iou, th)
        fp[n] = n_pred[n] - tp[n]
        fn[n] = n_true[n] - tp[n]
        ap[n] = tp[n] / (tp[n] + fp[n] + fn[n])  # this is the jaccard index, not precision, right?
        # this is tp[n] / (tp[n] + n_pred[n] - tp[n] + n_true[n] - tp[n]) = tp[n] / ( n_pred[n] + n_true[n] - tp[n])

    if not_list:
        ap, tp, fp, fn = ap[0], tp[0], fp[0], fn[0]
    return ap, tp, fp, fn


test_folder = "/home/cazorla/Images/Cellpose_dataset/test"

trainings_list = ["/home/cazorla/Images/Train_nouvelle_methode/Cellpose_dataset1",
                  "/home/cazorla/Images/Train_nouvelle_methode/Cellpose_dataset0.5",
                  "/home/cazorla/Images/Train_nouvelle_methode/Cellpose_dataset0.25",
                  "/home/cazorla/Images/Train_nouvelle_methode/Cellpose_dataset0.1"]

iou_thresholds = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.85, 0.9]

# test dataset images list
image_path_list = sorted([os.path.join(test_folder, f) for f in os.listdir(test_folder) if
                          (os.path.isfile(os.path.join(test_folder, f)) and "img" in f)])

# Groundtruths list
gt_path_list = sorted([os.path.join(test_folder, f) for f in os.listdir(test_folder) if
                       (os.path.isfile(os.path.join(test_folder, f)) and "masks" in f)])

# Initialize an empty list to store the image arrays
image_list = []
gt_list = []

# Loop through the image paths and read images as NumPy arrays
for i, image_path in enumerate(image_path_list):
    image_array = imread(image_path)
    gt_array = imread(gt_path_list[i])
    image_list.append(image_array)
    gt_list.append(gt_array)

# Computation of diameters for rescaling all the images

diam_test = np.array([utils.diameters(gt_list[k], omni=True)[0]
                     for k in range(len(gt_list))])

data = []
ap0 = []
nb = 69
for training in trainings_list:
    gt_cropped_list = []
    masks_cropped_list = []
    ap = []

    models_folder = os.path.join(training, "train", "models")
    models_list = sorted([os.path.join(models_folder, f) for f in os.listdir(models_folder) if
                          (os.path.isfile(os.path.join(models_folder, f)) and ".npy" not in f and ".txt" not in f)])
    # we use the most recent file, i.e. the last epoch
    models_list.sort(key=os.path.getmtime, reverse=True)
    pretrained_model = models_list[0]
    #for pretrained_model in models_list[0]:
    print(pretrained_model)
    model = CustomCellposeModel(gpu=True, pretrained_model=pretrained_model, nchan=2, omni=True)
    masks = model.eval(image_list[:nb], diameter=diam_test[:nb], flow_threshold=0, cellprob_threshold=0,
                       channels=[2, 1], omni=True, channel_axis=2)[0]

    # We remove 10% of the borders in the masks and grountruths
    for gt, mask in zip(gt_list, masks):
        x_0 = int(0.1 * gt.shape[0])
        x_1 = int(0.9 * gt.shape[0])
        y_0 = int(0.1 * gt.shape[1])
        y_1 = int(0.9 * gt.shape[1])
        gt_cropped_list.append(gt[x_0:x_1, y_0:y_1])
        masks_cropped_list.append(mask[x_0:x_1, y_0:y_1])

    # We don't use Omnipose average precision code cause it's not robust when cells are not regularly labelled
    # from 1 to n
    ap = average_precision(gt_cropped_list[:nb], masks_cropped_list, iou_thresholds)[0]

    ap0.append(list(ap.mean(axis=0)))


ap_values = {"100%": ap0[0], "50%": ap0[1], "25%": ap0[2], "10%": ap0[3]}
fig, ax = plt.subplots(figsize=(10, 8))

# Créez un graphique avec trois courbes, une pour chaque seuil d'IOU
for model, ap_scores in ap_values.items():
    plt.plot(iou_thresholds, ap_scores, label=model, linewidth=3)

plt.legend(fontsize=26)

plt.tick_params(axis="both", labelsize=26)
plt.xlabel("IoU matching threshold", fontsize=30)
plt.ylabel("Average Precision", fontsize=30)


print("precision max 100% : ", ap0[0][0])
print("precision max 50% : ", ap0[1][0])
print("precision max 25% : ", ap0[2][0])
print("precision max 10% : ", ap0[3][0])

plt.savefig('/home/cazorla/Documents/Codes/papier-frugalpose/figures/xp_cp_dataset/accuracy.pdf')

# Affichez le graphique
plt.show()
