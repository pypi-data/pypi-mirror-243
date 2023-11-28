import subprocess
import os
from skimage.io import imread, imsave
from napari_sketchpose.Custom_cellpose_omni import CustomCellposeModel
from cellpose_omni import utils, metrics
import numpy as np
import pandas as pd


# Liste des ensembles de paramètres que vous voulez utiliser
param_sets = [
    ["--train", "--train_size", "--use_gpu", "--omni",
     "--dir", "/home/cazorla/Images/Cellpose_dataset0.6_tiny/train", "--n_epochs", "40",
     "--img_filter", "_img", "--pretrained_model", "None",
     "--chan", "2", "--chan2", "1", "--save_each", "--save_every", "20", "--channel_axis", "2"],
    """["--train", "--train_size", "--use_gpu", "--omni",
         "--dir", "/home/cazorla/Images/Train_leur_LR/Cellpose_dataset0.5/train",
         "--img_filter", "_img", "--pretrained_model", "None",
         "--chan", "2", "--chan2", "1", "--save_each", "--save_every", "20", "--channel_axis", "2"],
    ["--train", "--train_size", "--use_gpu", "--omni",
             "--dir", "/home/cazorla/Images/Train_leur_LR/Cellpose_dataset0.25/train",
             "--img_filter", "_img", "--pretrained_model", "None",
             "--chan", "2", "--chan2", "1", "--save_each", "--save_every", "20", "--channel_axis", "2"],
    ["--train", "--train_size", "--use_gpu", "--omni",
    "--dir", "/home/cazorla/Images/Train_leur_LR/Cellpose_dataset0.1/train",
    "--img_filter", "_img", "--pretrained_model", "None",
    "--chan", "2", "--chan2", "1", "--save_each", "--save_every", "20", "--channel_axis", "2"]"""
]

# Parcourir chaque ensemble de paramètres et exécuter le script
for params in param_sets:
    command = ["python", "-m", "napari_sketchpose"] + params
    subprocess.run(command)

test_folder = "/home/cazorla/Images/Cellpose_dataset/test"

trainings_list = ["/home/cazorla/Images/Train_mon_LR/Cellpose_dataset1",
                  "/home/cazorla/Images/Train_mon_LR/Cellpose_dataset0.5",
                  "/home/cazorla/Images/Train_mon_LR/Cellpose_dataset0.25",
                  "/home/cazorla/Images/Train_mon_LR/Cellpose_dataset0.1"]

image_path_list = sorted([os.path.join(test_folder, f) for f in os.listdir(test_folder) if
                          (os.path.isfile(os.path.join(test_folder, f)) and "img" in f)])

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

# Computation of diameters for rescaling

diam_test = np.array([utils.diameters(gt_list[k], omni=True)[0]
                     for k in range(len(gt_list))])

data = []

for training in trainings_list:
    models_folder = os.path.join(training, "train", "../models")
    models_list = sorted([os.path.join(models_folder, f) for f in os.listdir(models_folder) if
                          (os.path.isfile(os.path.join(models_folder, f)) and ".npy" not in f and ".txt" not in f)])
    for pretrained_model in models_list:
        print(pretrained_model)
        model = CustomCellposeModel(gpu=True, pretrained_model=pretrained_model, nchan=2, omni=True)
        masks = model.eval(image_list, diameter=diam_test, flow_threshold=0, cellprob_threshold=None,
                           channels=[2, 1], omni=True, channel_axis=2)[0]
        ap = metrics.average_precision(gt_list, masks, [0.5])[0]
        ap0 = ap.mean(axis=0)[0]
        metrics._intersection_over_union(gt_list, masks)
        metrics.boundary_scores(gt_list, masks, [1])

        print(ap0)
        data.append([100 * int(training[-1]), int(pretrained_model[-3:]) - 1, ap0])

columns = ["Labels percentage", "epochs_nb", "ap0"]
df = pd.DataFrame(data, columns=columns)
df.to_excel("/home/cazorla/Images/Train_mon_LR/perf05.xlsx", index=False, engine="xlsxwriter")
