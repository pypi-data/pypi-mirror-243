import subprocess

import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='cellpose parameters')
parser.add_argument("--init_lr", type=float, default=0.1, help="Initial learning rate.")
parser.add_argument("--batch_size", type=int, default=8, help="Batch size.")
parser.add_argument("--training_dir", type=str, help="Training directory.")
parser.add_argument("--test_dir", type=str, help="Test directory.")
parser.add_argument("--max_epochs", type=int, default=500, help="Maximum number of epochs.")

args = parser.parse_args()


def get_last_weights(path):

    # Filtrer la liste pour ne conserver que les fichiers se terminant par "epoch_numero epoch"
    epoch_files = [file for file in os.listdir(path) if file.endswith(".npy") is False]

    # Vérifier si le dossier 'models' est vide ou s'il y a des fichiers 'epoch_numero epoch'
    if len(epoch_files) > 0:

        def extract_epoch_number(filename):
            return int(filename.split('_')[-1])

        # Trier les fichiers en utilisant la fonction d'extraction comme clé
        sorted_epoch_files = sorted(epoch_files, key=extract_epoch_number)

        # Obtenir le chemin complet du fichier du dernier entraînement
        last_training_file = sorted_epoch_files[-1]
        last_training_path = os.path.join(path, last_training_file)

        print("Le dossier n'est pas vide. Le chemin du dernier entraînement est :", last_training_path)
    else:
        last_training_path = "None"
        print("Le dossier est vide.")
    return last_training_path

init_lr = args.init_lr
batch_size = args.batch_size
training_dir = args.training_dir
test_dir = args.test_dir
max_epochs = args.max_epochs

if os.path.isdir(os.path.join(training_dir, "models")) is False:
    os.mkdir(os.path.join(training_dir, "models"))

pretrained_model = get_last_weights(os.path.join(training_dir, "models"))

"""from napari_sketchpose.evaluation_training.Custom_cellpose_omni_for_training import CustomCellposeModel
model = CustomCellposeModel(gpu=True, pretrained_model=pretrained_model, nchan=2, omni=True)
from skimage.io import imread
model.train(train_data=[imread("/home/cazorla/Images/Cellpose_dataset/train/000_img.png")],
            train_labels=[imread("/home/cazorla/Images/Cellpose_dataset/train/000_masks.png")], train_D_t=[np.random.random((100, 100))],
            train_S_t=[np.random.random((100, 100))], save_every=1, save_each=True, save_path="/home/cazorla/Images/Cellpose_dataset0.6_tiny/train")
"""

# Liste des ensembles de paramètres que vous voulez utiliser
params = ["--train", "--train_size", "--use_gpu", "--omni", "--batch_size",  str(batch_size), "--dir",
          training_dir, "--test_dir", test_dir, "--img_filter", "_img", "--pretrained_model", pretrained_model, "--chan", "2", "--chan2", "1",
          "--save_each", "--save_every", "1", "--channel_axis", "2", "--n_epochs", str(max_epochs), "--verbose"]

command = ["python", "-m", "napari_sketchpose"] + params
subprocess.run(command)
