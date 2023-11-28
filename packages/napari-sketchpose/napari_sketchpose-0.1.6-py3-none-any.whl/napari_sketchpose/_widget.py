"""
Dessin dock widget module
"""
import platform
import subprocess
from datetime import datetime

import matplotlib.pyplot as plt

# We call a bash function to install torch for windows as we cannot install the Cuda version from the setup.cfg file

import torch

# On Windows computers, CUDA version of pytorch is often not well installed.
if torch.cuda.is_available() is False:
    print("Please wait while CUDA PyTorch dependencies are being installed before trying to use the plugin. This can"
          " take a while.")
    p1 = subprocess.Popen("ltt install torch torchvision --upgrade", shell=True)
    p1.wait()


import os
import pandas as pd
import requests
from typing import Any

from napari_plugin_engine import napari_hook_implementation
from napari.utils.notifications import show_info, notification_manager
from .TrainingDialog import TrainingDialog
from qtpy.QtWidgets import QDialog, QProgressBar

import time
import numpy as np
import pyqtgraph as pg

from napari import Viewer
from magicgui import magicgui

from skimage.io import imread, imsave

from superqt import ensure_main_thread
from qtpy.QtWidgets import QFileDialog
from .Custom_cellpose_omni import CustomCellposeModel
from omnipose.core import compute_masks
from omnipose.core import masks_to_flows
from edt import edt
from qtpy.QtCore import QThread, Signal
from napari.qt.threading import thread_worker
from skimage.morphology import dilation, disk, erosion, skeletonize
from skimage.measure import label, regionprops
from cellpose_omni.transforms import normalize_img
from copy import deepcopy


@ensure_main_thread
def show_info(message: str):
    notification_manager.receive_info(message)


# @thread_worker
def read_logging(log_file, logwindow):
    with open(log_file, 'r') as thefile:
        # thefile.seek(0,2) # Go to the end of the file
        while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.01)  # Sleep briefly
                continue
            else:
                logwindow.cursor.movePosition(logwindow.cursor.End)
                logwindow.cursor.insertText(line)
                yield line


def grad_omni(*args, **kargs):
    return masks_to_flows(*args, **kargs)[-1]


models_list = ["None", "cyto2", "bact_phase", "bact_fluor", "plant", "worm", "worm_bact", "worm_high_res",
               "custom model"]
models_url = "https://www.cellpose.org/models/"
model = "None"
custom_model_name = "None"
OMNI = True
nchannels = 2

border_thickness = 3

# DEFAULT PARAMETERS FOR TRAINING

initial_model = "cyto2"
chan1 = "gray"
chan2 = "None"
LR = 0.1
w_decay = 10**-4
epochs_nb = 100
SGD = False

double_click = False
saved_values = None

# Store all processes to make sure to kill them all when clicking stop training
training_threads_list = []
torch.autograd.set_detect_anomaly(True)

def Dessin():
    """
    Dessin plugin code
    @return:
    """

    @magicgui(
        auto_call=False,
        call_button=False,
        layout='vertical',
        load_images_button=dict(widget_type='PushButton', text='LOAD IMAGES',
                                tooltip='Load images'),
        nn_choice=dict(widget_type='Label', label='MODEL ZOO'),
        nn=dict(widget_type='ComboBox', label='Network architecture', choices=models_list.copy(), value="cyto2",
                tooltip='All the available network architectures'),
        or_txt=dict(widget_type='Label', label='OR'),
        load_custom_button=dict(widget_type='PushButton', text='Load custom model', tooltip='Load a model trained '
                                                                                            'by yourself'),
        chan=dict(widget_type='ComboBox', label='Channel to segment', choices=["gray", "red", "green", "blue"],
                  value="gray", tooltip='First channel to segment'),
        chan2=dict(widget_type='ComboBox', label='Channel 2 (optional)', choices=["None", "red", "green", "blue"],
                  value="None", tooltip='Second channel to segment'),
        flow_th_field=dict(widget_type='LineEdit', label='Flow threshold', value=0.4, tooltip='Flow threshold'),
        cell_th_field=dict(widget_type='LineEdit', label='Cell threshold', value=0.0, tooltip='Cell threshold'),
        bg_button=dict(widget_type='PushButton', text='Background', tooltip='Click to draw background'),
        cells_button=dict(widget_type='PushButton', text='Cells', tooltip='Click to draw background'),
        bd_button=dict(widget_type='PushButton', text='Boundaries', tooltip='Click to draw background'),
        drawing_options=dict(widget_type='Label', label='LABELING'),
        run_button=dict(widget_type='PushButton', text='RUN', tooltip='Load images'),
        diameter_field=dict(widget_type='LineEdit', label='Diameter', value=30, tooltip='Diameter'),
        draw_button=dict(widget_type='PushButton', text='DRAW!', tooltip='Draw!'),
        add_cells_button=dict(widget_type='CheckBox', text='Add cells to labels double-clicking',
                              tooltip='Add cells to the labels', enabled=False),
        draw_bbox_button=dict(widget_type='CheckBox', text='Draw bboxes of training ROI',
                              tooltip='Draw bboxes where to train the model', enabled=False),
        train_part=dict(widget_type='Label', label='TRAINING'),
        inference_part=dict(widget_type='Label', label='INFERENCE'),
        train_button=dict(widget_type='PushButton', text='RETRAIN MODEL', tooltip='Retrain the model from the labels'),
        train_options_button=dict(widget_type='PushButton', text='Training options', tooltip='Set the training options'),
        show_res_each_button=dict(widget_type='LineEdit', label='Show result each', value=20, tooltip='Show result'
                                  ' each n epochs during training'),
        reset_button=dict(widget_type='PushButton', text='Reset network', tooltip='Reset network to None object'),
        little_res_window_button=dict(widget_type='CheckBox', text='Show result in little window',
                                      tooltip='Move a bbox on the image in which you show training progress'),
        doc_button=dict(widget_type='PushButton', text="", tooltip="Documentation"),

    )
    def dessin_widget(  # label_logo,
            viewer: Viewer,
            load_images_button,
            Index: int,
            nn_choice,
            nn,
            or_txt,
            load_custom_button,
            inference_part,
            chan,
            chan2,
            flow_th_field,
            cell_th_field,
            diameter_field,
            run_button,
            drawing_options,
            draw_button,
            bg_button,
            cells_button,
            bd_button,
            add_cells_button,
            draw_bbox_button,
            train_part,
            train_button,
            reset_button,
            train_options_button,
            show_res_each_button,
            little_res_window_button,
            doc_button,



    ) -> None:
        # Create a black image just so layer variable exists
        # This global instance of the viewer is created to be able to display images from the prediction plugin when
        # it's being opened
        global V
        V = viewer

    # Initialization of buttons state when launching the plugin
    dessin_widget.draw_button.root_native_widget.setCheckable(True)
    dessin_widget.train_button.root_native_widget.setCheckable(True)
    dessin_widget.bg_button.enabled = False
    dessin_widget.cells_button.enabled = False
    dessin_widget.bd_button.enabled = False
    dessin_widget.Index.value = 1
    dessin_widget.Index.range = (1, 999)
    dessin_widget.Index.label = "Image index"

    from qtpy.QtGui import QIcon, QPixmap
    import requests

    url = "https://bitbucket.org/koopa31/napari_svetlana/raw/c7438ec591fa5e23f03cfb17f4984e9f52571649/src/doc.png"
    response = requests.get(url)
    pixmap = QPixmap()
    pixmap.loadFromData(response.content)
    icon = QIcon(pixmap)
    dessin_widget.doc_button.native.setIcon(icon)
    dessin_widget.doc_button.native.setStyleSheet("QPushButton { border: none; }")
    dessin_widget.doc_button.native.setText("DOCUMENTATION")

    dessin_widget.show()

    @dessin_widget.doc_button.changed.connect
    def launch_doc(e: Any):
        import webbrowser
        webbrowser.open("https://sketchpose-doc.readthedocs.io/en/latest/")

    def draw_red_ball(x, y, diam):
        coords = np.array([[x - diam - 1, y - diam - 1], [x - diam - 1, y - 1],
                           [x - 1, y - 1], [x - 1, y - diam - 1]])
        dessin_widget.viewer.value.add_shapes(data=coords, shape_type="ellipse", edge_color='red', face_color='red',
                                              name="Cells diameter")
        # Make it quite transparent so it does not bother visualization
        dessin_widget.viewer.value.layers["Cells diameter"].opacity = 0.2
        dessin_widget.viewer.value.layers.selection.active = dessin_widget.viewer.value.layers["image"]

    @dessin_widget.viewer.value.mouse_double_click_callbacks.append
    def display_coordinates(viewer, event):
        if event.button == 1:
            if "CP result" in viewer.layers and viewer.layers.selection.active.name == "CP result"\
                    and double_click is True:
                x = int(event.position[0])
                y = int(event.position[1])
                print(f"Coordonnées : x={x}, y={y}")
                add_cell_to_labels(x, y, dessin_widget.viewer.value.layers["CP result"],
                                   dessin_widget.viewer.value.layers["labels"],
                                   dessin_widget.viewer.value.layers["boundaries"])
        elif event.button == 2:
            # Draw the edges of a fully annotated cell right-clicking on it
            im = dessin_widget.viewer.value.layers["labels"].data
            labs = label(im)
            x = int(event.position[0])
            y = int(event.position[1])
            mask = np.where((labs == labs[x, y]), 1, 0)

            dilated_mask = dilation(mask, disk(1))
            eroded_mask = erosion(mask, disk(border_thickness // 2))
            contours = dilated_mask - mask
            dessin_widget.viewer.value.layers["labels"].data[contours != 0] = 0
            dessin_widget.viewer.value.layers["boundaries"].data[contours != 0] = 10
            dessin_widget.viewer.value.layers["labels"].refresh()
            dessin_widget.viewer.value.layers["boundaries"].refresh()

    @dessin_widget.viewer.value.mouse_drag_callbacks.append
    def delete_cell(viewer, event):
        """
        This function enables to delete some cells in a bbox to redraw it
        Parameters
        ----------
        viewer :
        event :

        Returns
        -------

        """
        # if mouse wheel clicked
        if event.button == 3:
            x = int(event.position[0])
            y = int(event.position[1])
            dessin_widget.viewer.value.layers["CP result"].data[dessin_widget.viewer.value.layers["CP result"].data
                                                                == dessin_widget.viewer.value.layers["CP result"].data[x , y]] = 0
            dessin_widget.viewer.value.layers["CP result"].refresh()

    @dessin_widget.add_cells_button.changed.connect
    def click_to_annotate(e: Any):
        """
        Activates click to annotate option
        @param e: boolean value of the checkbox
        @return:
        """
        global double_click, enable_labeling
        if e is True:
            if ("labels" in dessin_widget.viewer.value.layers) is False:
                dessin_widget.viewer.value.add_labels(
                    np.zeros(dessin_widget.viewer.value.layers[0].data.shape[:2]).astype("uint8"),
                    name="labels")
            if ("boundaries" in dessin_widget.viewer.value.layers) is False:
                dessin_widget.viewer.value.add_labels(
                    np.zeros(dessin_widget.viewer.value.layers[0].data.shape[:2]).astype("uint8"),
                    name="boundaries")
            double_click = True
            # select the image so the user can click on it
            dessin_widget.viewer.value.layers.selection.active = dessin_widget.viewer.value.layers[
                "CP result"]
            dessin_widget.draw_button.enabled = False
            dessin_widget.draw_bbox_button.enabled = False
        else:
            dessin_widget.draw_button.enabled = True
            dessin_widget.draw_bbox_button.enabled = True

    def add_cell_to_labels(x, y, cp_res_layer, labels_layer, bd_layer):
        """
        Add cell To the labels clicking on it to make labels denser.
        @param x: coordinate of clicked cell
        @param y: coordinate of clicked cell
        @return:
        """

        if isinstance(cp_res_layer, np.ndarray):
            labs = cp_res_layer
        else:
            labs = cp_res_layer.data
        labs = label(labs)
        props = regionprops(labs)
        ind = labs[x, y] - 1

        temp_mask = np.zeros_like(labs)
        temp_mask[props[ind].coords[:, 0], props[ind].coords[:, 1]] = 1

        eroded_temp_mask = temp_mask.copy()
        dilated_temp_mask = temp_mask.copy()
        eroded_temp_mask = erosion(eroded_temp_mask, disk(border_thickness // 2 + 1))
        dilated_temp_mask = dilation(dilated_temp_mask, disk(1))

        contours = dilated_temp_mask - temp_mask

        if isinstance(cp_res_layer, np.ndarray):
            labels_layer[temp_mask != 0] = 2
            bd_layer[contours != 0] = 10
        else:
            labels_layer.data[temp_mask != 0] = 2
            labels_layer.refresh()
            bd_layer.data[contours != 0] = 10
            bd_layer.refresh()

    @dessin_widget.viewer.value.bind_key("Up", overwrite=True)
    def increase_brush_size(viewer):
        """
        Change brush size using arrows.
        Parameters
        ----------
        viewer :

        Returns
        -------

        """
        if dessin_widget.draw_button.root_native_widget.isChecked():
            dessin_widget.viewer.value.layers.selection.active.brush_size += 1

    @dessin_widget.viewer.value.bind_key("Down", overwrite=True)
    def increase_brush_size(viewer):
        """
        Change brush size using arrows.
        Parameters
        ----------
        viewer :

        Returns
        -------

        """
        if dessin_widget.draw_button.root_native_widget.isChecked():
            dessin_widget.viewer.value.layers.selection.active.brush_size -= 1

    @dessin_widget.viewer.value.bind_key("x", overwrite=True)
    def show_boundaries(viewer):
        if "CP result" in viewer.layers:
            if dessin_widget.viewer.value.layers["CP result"].contour == 0:
                dessin_widget.viewer.value.layers["CP result"].contour = 1
            else:
                dessin_widget.viewer.value.layers["CP result"].contour = 0

    @dessin_widget.diameter_field.changed.connect
    def change_diameter(e: int):
        """
        Change the diameter of the red ball showing the size of the cells to segment
        :param e:
        :return:
        """
        global model
        diam = int(e)
        x = dessin_widget.viewer.value.layers[0].data.shape[0]
        y = dessin_widget.viewer.value.layers[0].data.shape[1]
        dessin_widget.viewer.value.layers["Cells diameter"].data = \
            np.array([[x - diam - 1, y - diam - 1], [x - diam - 1, y - 1], [x - 1, y - 1], [x - 1, y - diam - 1]])

    @dessin_widget.load_images_button.changed.connect
    def load_images(e: Any):
        """
        Loads the folder containing the images to annotates and displays the first one
        @param e:
        @return:
        """
        global parent_path, mask_folder, previous_index_value

        dessin_widget.viewer.value.layers.clear()
        previous_index_value = 1

        # Choice of the batch folder
        parent_path = QFileDialog.getExistingDirectory(None, 'Choose the parent folder which contains your images',
                                                       options=QFileDialog.DontUseNativeDialog)

        mask_folder = os.path.join(parent_path, "Masks")
        if os.path.isdir(mask_folder) is False:
            os.mkdir(mask_folder)

        # Check if the selected folder is correct
        if os.path.isdir(parent_path) is True:

            # Gets the list of images and masks
            global image_path_list, mask_path_list, global_im_path_list, global_lab_path_list, global_labels_list, \
                global_mini_props_list, mini_props_list, Image, mask

            image_path_list = sorted([os.path.join(parent_path, f) for f in os.listdir(parent_path) if
                                      os.path.isfile(os.path.join(parent_path, f))])

            # For now we only read the first image

            image = imread(image_path_list[dessin_widget.Index.value - 1])
            dessin_widget.viewer.value.add_image(image, name="image")
            draw_red_ball(image.shape[0], image.shape[1], int(dessin_widget.diameter_field.value))

            # If labels and boundaries have already been drawn, reload them to keep drawing
            name, ext = os.path.splitext(os.path.split(image_path_list[dessin_widget.Index.value - 1])[1])
            lab_path = os.path.join(mask_folder, name + "_labels.png")
            bd_path = os.path.join(mask_folder, name + "_boundaries.png")
            bbox_path = os.path.join(mask_folder, name + "_bbox.csv")
            if os.path.isfile(lab_path) is True:
                dessin_widget.viewer.value.add_labels(imread(lab_path), name="labels")
            if os.path.isfile(bd_path) is True:
                dessin_widget.viewer.value.add_labels(imread(bd_path), name="boundaries")
            if os.path.isfile(bbox_path) is True:
                load_bbox(bbox_path)
            if len(image.shape) == 3:
                dessin_widget.viewer.value.add_labels(np.zeros_like(image[:, :, 0]), name="CP result")
            else:
                dessin_widget.viewer.value.add_labels(np.zeros_like(image), name="CP result")

            show_info("Image imported successfully")

        else:
            show_info("ERROR: Please select a folder")

    @dessin_widget.Index.changed.connect
    def switch_image(e: Any):
        """
        Loads next or previous image and its labels
        :param e: boolean to know if function has been triggered
        :return:
        """
        global previous_index_value
        if dessin_widget.Index.value <= len(image_path_list):

            if dessin_widget.Index.value > previous_index_value:
                save_labels(dessin_widget.Index.value - 2)
            elif dessin_widget.Index.value < previous_index_value:
                save_labels(dessin_widget.Index.value)

            previous_index_value = dessin_widget.Index.value

            # Clear the previous images
            dessin_widget.viewer.value.layers.clear()

            # Load the next image and draw the red circle
            image = imread(image_path_list[dessin_widget.Index.value - 1])
            dessin_widget.viewer.value.add_image(image, name="image")
            draw_red_ball(image.shape[0], image.shape[1], int(dessin_widget.diameter_field.value))
            if len(image.shape) == 3:
                dessin_widget.viewer.value.add_labels(np.zeros_like(image[:, :, 0]), name="CP result")
            else:
                dessin_widget.viewer.value.add_labels(np.zeros_like(image), name="CP result")
            if dessin_widget.little_res_window_button.value is True:
                little_res_window(True)

            # If labels and boundaries have already been drawn, reload them to keep drawing
            name, ext = os.path.splitext(os.path.split(image_path_list[dessin_widget.Index.value - 1])[1])
            lab_path = os.path.join(mask_folder, name + "_labels.png")
            bd_path = os.path.join(mask_folder, name + "_boundaries.png")
            bbox_path = os.path.join(mask_folder, name + "_bbox.csv")
            if os.path.isfile(lab_path) is True:
                dessin_widget.viewer.value.add_labels(imread(lab_path), name="labels")
            if os.path.isfile(bd_path) is True:
                dessin_widget.viewer.value.add_labels(imread(bd_path), name="boundaries")
            if os.path.isfile(bbox_path) is True:
                load_bbox(bbox_path)
        else:
            dessin_widget.Index.value -= 1
            show_info("No more images in the folder")

    @dessin_widget.viewer.value.bind_key("Right", overwrite=True)
    def next_image(e: Any):
        # Increase the image index by 1
        dessin_widget.Index.value += 1

    @dessin_widget.viewer.value.bind_key("Left", overwrite=True)
    def previous_image(e: Any):
        if dessin_widget.Index.value > 1:
            # Decrease the image index by 1
            dessin_widget.Index.value -= 1

    def load_bbox(bbox_path):
        """
        Loads existing bbox which has already been drawn on images
        :param bbox_path: path to file containing the bboxes coordinates
        :return:
        """
        df = pd.read_csv(bbox_path)

        # Regroupez les coordonnées de toutes les bounding boxes
        all_shape_data = []
        # Itérez sur les groupes de lignes (index) dans le DataFrame
        for index, group in df.groupby('index'):
            # Ajoutez les coordonnées des quatre coins à la liste globale
            all_shape_data.append(group[['axis-0', 'axis-1']].to_numpy())

        # Ajoutez un shape layer au viewer en utilisant les données de la bounding box
        shapes = dessin_widget.viewer.value.add_shapes(name="bbox", data=all_shape_data, shape_type='rectangle',
                                                       blending="additive", edge_width=2, edge_color="#00aa00ff",
                                                       face_color=[0, 0, 0, 0])

    def save_labels(ind):
        """
        Save labels for each annotated image
        :param ind: index of the image in the folder
        :return:
        """

        # If bbox exists, must be saved first to update labels and boundaries with what have been drawn
        # and/or predicted inside bboxes
        if "bbox" in dessin_widget.viewer.value.layers:
            name, ext = os.path.splitext(os.path.split(image_path_list[ind])[1])
            shape_data = dessin_widget.viewer.value.layers["bbox"].data

            bbox_list = []

            # append in a list each bbox contained in the bbox layer as a dict
            for index, bbox in enumerate(shape_data):
                for vertex_index in range(4):
                    bbox_dict = {
                        'index': index,
                        'shape-type': 'rectangle',
                        'vertex-index': vertex_index,
                        'axis-0': tuple(bbox)[vertex_index][0],
                        'axis-1': tuple(bbox)[vertex_index][1],
                    }
                    bbox_list.append(bbox_dict)

            # Convert dictionary list into DataFrame pandas
            df = pd.DataFrame(bbox_list)

            # Set the backup path for the CSV file
            file_path = os.path.join(mask_folder, name + "_bbox.csv")

            # Save the pandas DataFrame as a CSV file
            df.to_csv(file_path, index=False)

            # Then convert remaining labels in CP result to labels layer
            CP_result_patches = get_im_from_bbox(dessin_widget.viewer.value.layers["CP result"].data,
                                                 shape_data)
            labels_patches = get_im_from_bbox(dessin_widget.viewer.value.layers["labels"].data, shape_data)
            boundaries_patches = get_im_from_bbox(dessin_widget.viewer.value.layers["boundaries"].data, shape_data)

            for i, CP_patch in enumerate(CP_result_patches):
                props = regionprops(CP_patch)
                for prop in props:
                    add_cell_to_labels(int(prop.centroid[0]), int(prop.centroid[1]), CP_patch,
                                       labels_patches[i], boundaries_patches[i])

                # Set everything which is not cells or boundaries to background
                labels_patches[i][np.logical_and(labels_patches[i] == 0,
                                                 boundaries_patches[i] == 0)] = 1

                xmin, ymin, xmax, ymax = shape_data[i]
                xmin = np.maximum(0, xmin).astype("int")
                xmax = np.minimum(xmax, dessin_widget.viewer.value.layers["labels"].data.shape[:2]).astype("int")
                dessin_widget.viewer.value.layers["labels"].data[xmin[0]:xmax[0], xmin[1]:xmax[1]] = labels_patches[i]
                dessin_widget.viewer.value.layers["boundaries"].data[xmin[0]:xmax[0], xmin[1]:xmax[1]] = \
                    boundaries_patches[i]

        if "labels" in dessin_widget.viewer.value.layers:
            name, ext = os.path.splitext(os.path.split(image_path_list[ind])[1])
            imsave(os.path.join(mask_folder, name + "_labels.png"),
                   dessin_widget.viewer.value.layers["labels"].data)

        if "boundaries" in dessin_widget.viewer.value.layers:
            name, ext = os.path.splitext(os.path.split(image_path_list[ind])[1])
            imsave(os.path.join(mask_folder, name + "_boundaries.png"),
                   dessin_widget.viewer.value.layers["boundaries"].data)

    @dessin_widget.load_custom_button.changed.connect
    def load_custom_model():
        """
        Load a model which has been trained previously by the user
        Returns
        -------

        """
        global custom_model_name
        # Choice of the binary file containing the weights
        custom_model_name = QFileDialog.getOpenFileName(None, 'Choose the parent folder which contains your images',
                                                        options=QFileDialog.DontUseNativeDialog)[0]
        dessin_widget.nn.value = "custom model"
        show_info("Model loaded: %s" %os.path.split(custom_model_name)[-1])

    def load_model():
        """
        Load the desired model, from scratch or a downloaded weights binary file.
        :return:
        """
        global model

        model_name = dessin_widget.nn.value
        if model_name == "None":
            model = CustomCellposeModel(gpu=True, pretrained_model=False, nchan=nchannels, omni=OMNI)

        elif model_name == "custom model":
            if custom_model_name is "None":
                show_info("Load a custom model first")
            else:
                model = CustomCellposeModel(gpu=True, pretrained_model=custom_model_name, nchan=nchannels, omni=OMNI)

        else:
            model_name = model_name + "_omnitorch" + "_0"
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", model_name)
            if os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")) is False:
                os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models"))
            if os.path.isfile(model_path) is False:
                # request model from the web
                show_info("Wait while weights are being downloaded...")
                r = requests.get(os.path.join(models_url, model_name), allow_redirects=True)
                open(model_path, 'wb').write(r.content)
                show_info("Weights downloaded successfully!")
            model = CustomCellposeModel(gpu=True, pretrained_model=model_path, nchan=nchannels, omni=OMNI)

    @dessin_widget.draw_bbox_button.changed.connect
    def add_bbox_layer(e: Any):
        """
        Layer to draw bounding boxes
        Returns
        -------

        """
        if e is True:
            dessin_widget.draw_button.enabled = False
            dessin_widget.add_cells_button.enabled = False

            if "bbox" not in dessin_widget.viewer.value.layers:
                shapes = dessin_widget.viewer.value.add_shapes(name="bbox")
            else:
                shapes = dessin_widget.viewer.value.layers["bbox"]

            # In some cases, labels and bd don't already exist so the need to be created
            if ("labels" in dessin_widget.viewer.value.layers) is False:
                dessin_widget.viewer.value.add_labels(
                    np.zeros(dessin_widget.viewer.value.layers[0].data.shape[:2]).astype("uint8"),
                    name="labels")
            if ("boundaries" in dessin_widget.viewer.value.layers) is False:
                dessin_widget.viewer.value.add_labels(
                    np.zeros(dessin_widget.viewer.value.layers[0].data.shape[:2]).astype("uint8"),
                    name="boundaries")

            dessin_widget.viewer.value.layers.selection.active = shapes
            shapes.blending = "additive"
            shapes.current_edge_width = 2
            shapes.current_edge_color = "#00aa00ff"
            shapes.current_face_color = [0, 0, 0, 0]
            shapes.mode = "add_rectangle"
        else:
            dessin_widget.draw_button.enabled = True
            dessin_widget.add_cells_button.enabled = True
            shapes = dessin_widget.viewer.value.layers["bbox"]
            shapes.mode = "pan_zoom"

    def handle_inference_result(mask_labels):
        # Update the image layer with the segmentation result
        if "CP result" not in dessin_widget.viewer.value.layers:
            dessin_widget.viewer.value.add_labels(mask_labels, name="CP result")
        else:
            dessin_widget.viewer.value.layers["CP result"].data = mask_labels

        cells_nb = mask_labels.max()
        if cells_nb == 0:
            show_info("No cells found")
        else:
            show_info("%s cells found" % (mask_labels.max()))
        # Now CP result exists, enable clicking on cells
        dessin_widget.add_cells_button.enabled = True
        dessin_widget.draw_bbox_button.enabled = True

    def inference(model, image, diameter, cellprob_th, channels, flow_th):
        """
        Inference of the model in a thread_worker
        :param model:
        :param image:
        :param diameter:
        :param cellprob_th:
        :param channels:
        :param flow_th:
        :return:
        """
        # Perform the segmentation using the loaded model
        mask_labels = model.eval(image, diameter=diameter, flow_threshold=flow_th, cellprob_threshold=cellprob_th,
                                 channels=channels, omni=OMNI, channel_axis=2)[0]
        return mask_labels

    @dessin_widget.run_button.changed.connect
    def process():
        """
        Perform the segmentation of the image using the loaded model
        :return:
        """

        load_model()

        image = dessin_widget.viewer.value.layers[0].data

        # Setting the parameters for inference given by the user
        if int(dessin_widget.diameter_field.value) == 0:
            diameter = None
        else:
            diameter = int(dessin_widget.diameter_field.value)
        if float(dessin_widget.cell_th_field.value) == 0:
            cellprob_th = None
        else:
            cellprob_th = float(dessin_widget.cell_th_field.value)

        channels = [dessin_widget.chan.choices.index(dessin_widget.chan.value),
                    dessin_widget.chan2.choices.index(dessin_widget.chan2.value)]

        # Inference
        # Create the inference thread
        inference_thread = thread_worker(inference)(model, image, diameter, cellprob_th, channels,
                                           float(dessin_widget.flow_th_field.value))

        # Connect the inference_complete signal to the slot
        inference_thread.returned.connect(handle_inference_result)

        # Start the inference thread
        inference_thread.start()
        show_info("Please wait during computation")

    @dessin_widget.draw_button.changed.connect
    def draw(e: Any):
        """
        Activate or deactivate the drawing option to label.
        :param e:
        :return:
        """
        if dessin_widget.draw_button.root_native_widget.isChecked():
            if ("labels" in dessin_widget.viewer.value.layers) is False:
                dessin_widget.viewer.value.add_labels(np.zeros(dessin_widget.viewer.value.layers[0].data.shape[:2]).astype("uint8"),
                                                      name="labels")
            if ("boundaries" in dessin_widget.viewer.value.layers) is False:
                dessin_widget.viewer.value.add_labels(np.zeros(dessin_widget.viewer.value.layers[0].data.shape[:2]).astype("uint8"),
                                                      name="boundaries")

            dessin_widget.draw_button.text = "STOP DRAWING"
            dessin_widget.run_button.enabled = False
            dessin_widget.bg_button.enabled = True
            dessin_widget.cells_button.enabled = True
            dessin_widget.bd_button.enabled = True
            dessin_widget.add_cells_button.enabled = False
            dessin_widget.draw_bbox_button.enabled = False
            show_info("Labelling activated")
        else:
            dessin_widget.draw_button.text = "DRAW!"
            dessin_widget.run_button.enabled = True
            dessin_widget.bg_button.enabled = False
            dessin_widget.cells_button.enabled = False
            dessin_widget.bd_button.enabled = False
            dessin_widget.add_cells_button.enabled = True
            dessin_widget.draw_bbox_button.enabled = True
            dessin_widget.viewer.value.layers.selection.active = dessin_widget.viewer.value.layers["image"]
            show_info("Labelling deactivated")

    @dessin_widget.bg_button.changed.connect
    def draw_bg(e: Any):
        # Make labels layer active to draw
        dessin_widget.viewer.value.layers.selection.active = dessin_widget.viewer.value.layers["labels"]
        dessin_widget.viewer.value.layers["labels"].selected_label = 1
        dessin_widget.viewer.value.layers["labels"].brush_size = 20
        dessin_widget.viewer.value.layers["labels"].mode = "paint"
        show_info("Please draw background labels")

    @dessin_widget.cells_button.changed.connect
    def draw_cells(e: Any):
        # Make labels layer active to draw
        dessin_widget.viewer.value.layers.selection.active = dessin_widget.viewer.value.layers["labels"]
        dessin_widget.viewer.value.layers["labels"].selected_label = 2
        dessin_widget.viewer.value.layers["labels"].brush_size = 20
        dessin_widget.viewer.value.layers["labels"].mode = "paint"
        show_info("Please draw cells labels")

    @dessin_widget.bd_button.changed.connect
    def draw_bd(e: Any):
        # Make labels layer active to draw
        dessin_widget.viewer.value.layers.selection.active = dessin_widget.viewer.value.layers["boundaries"]
        dessin_widget.viewer.value.layers["boundaries"].selected_label = 10
        dessin_widget.viewer.value.layers["boundaries"].brush_size = 1
        dessin_widget.viewer.value.layers["boundaries"].mode = "paint"
        show_info("Please draw boundaries labels")

    @dessin_widget.train_options_button.changed.connect
    def set_train_params(e: int):
        global LR, SGD, initial_model, chan1, chan2, w_decay, epochs_nb, saved_values
        # Open the training dialog
        dialog = TrainingDialog(models_list, saved_values=saved_values)
        if dialog.exec_() == QDialog.Accepted:  # Only retrieve parameters if the dialog was accepted
            LR = float(dialog.lr_field.text())
            SGD = dialog.checkbox.isChecked()
            initial_model = dialog.model_field.currentText()
            dessin_widget.nn.value = initial_model
            chan1 = dialog.chan1.currentText()
            dessin_widget.chan.value = chan1
            chan2 = dialog.chan2.currentText()
            dessin_widget.chan2.value = chan2
            w_decay = float(dialog.w_decay_field.text())
            epochs_nb = int(dialog.n_epochs_field.text())
            # Saved values for the training params dialog
            saved_values = {"LR": LR, "SGD": SGD, "initial_model": initial_model, "chan1": chan1, "chan2": chan2,
                            "w_decay": w_decay, "epochs_nb": epochs_nb}

    def display_labels(S1, S2, B):
        im = np.zeros((S1.shape[0], S1.shape[1], 3))
        im[B > 0, 0] = 1
        im[(S1 > 0) & (B == 0), 1] = 1
        im[(S2 > 0) & (B == 0), 2] = 1
        plt.imshow(im)
        plt.title("R=edges, G=S1, B=S2, Black=unknown label")
        plt.show()

    def trusted_region_distance(labels, boundaries):

        partition = labels
        B_manual = boundaries

        dilated_labels = dilation(partition == 2, disk(1))
        B = np.logical_and(dilated_labels == 1, partition == 1).astype("uint8")
        # B = dilation(B, disk(border_thickness // 2))
        B = np.logical_or(B != 0, B_manual != 0).astype("uint8") * 255
        # so we have a 1-pixel width boundary
        # B = skeletonize(B).astype("uint8") * 255

        # indicators of background (S1) and cells (S2)
        S1 = np.where(partition == 1, 255, 0).astype("uint8")
        S2 = np.where(partition == 2, 255, 0).astype("uint8")

        # display_labels(S1, S2, B)

        # Distance to boundaries (complementary to B)
        dist_B = edt((255 - B).copy(), parallel=-1).astype(np.float32)

        # Distance to no labels area
        S = (S1 // 255) | (S2 // 255)
        dist_CB = edt(S, parallel=-1).astype(np.float32)

        # Area where distance is safe to compute
        D = (dist_B <= dist_CB).astype("uint8")

        # Labels from manual annotations for the training
        # B is skeletonized in order to avoid cell erosion
        # B_inv = 255 - (skeletonize(B) * 255)
        B_inv = 255 - (B.astype("bool") * 255)
        labels = label(S2 * B_inv, connectivity=1)

        imsave("labels.png", labels.astype("uint16"))

        """# Cleaning out the tiny outliers from the labels
        eroded_labels = erosion(labels, disk(3))
        keep_list = np.unique(eroded_labels)
        labels_keep = np.zeros_like(labels)
        for keep in keep_list:
            labels_keep += (labels == keep) * keep
        labels = labels_keep"""

        """# Make data consistent with the one of data science bowl removing artificial erosion created by the way
        # boundaries are drawn
        dil = dilation(labels, disk(2))
        labels = np.logical_and(np.where(S2 == 255, 1, 0), np.where(dil != 0, 1, 0)) * dil
        
        plt.imshow(labels);
        plt.title("dilaté");
        plt.show()
        plt.imshow(S1);
        plt.show()
        plt.imshow(S2);
        plt.show()
        plt.imshow(B);
        plt.show()
        plt.imshow(dist_B);
        plt.title("dist B");
        plt.show()
        plt.imshow(dist_CB);
        plt.title("dist CB");
        plt.show()
        plt.imshow(D);
        plt.show()
        plt.imshow(S);
        plt.show()
        plt.imshow(D * partition);
        plt.title("D x labls");
        plt.show()
        plt.imshow(labels);
        plt.title("Labels");
        plt.show()"""

        return labels, D, S

    @dessin_widget.little_res_window_button.changed.connect
    def little_res_window(e: Any):
        """
        Little window in which prediction is made each n iteration of the training
        Parameters
        ----------
        e :

        Returns
        -------

        """
        global little_window
        if e is True:
            if "little window" not in dessin_widget.viewer.value.layers:
                little_window = dessin_widget.viewer.value.add_shapes(np.array([[0, 0], [224, 0], [224, 224], [0, 224]]),
                                                                      edge_color="#ff0000", face_color=[0, 0, 0, 0],
                                                                      edge_width=2, blending="translucent",
                                                                      name="little window")

            # Make this layer active and draw red rectangle of size 200x200
            dessin_widget.viewer.value.layers.selection.active = little_window
            little_window.mode = "select"

    def on_yielded(e):
        global predict_model, epoch
        epoch, loss_list, model = e
        dessin_widget.viewer.value.status = "epoch {}, training loss = {:.4f}".format(epoch, loss_list[-1])
        if epoch != 1:
            if dessin_widget.little_res_window_button.value:
                training_thread.pause()

                # Plot the loss values
                loss_curve = loss_plot.plot(loss_list, pen=(255, 102, 0), clear=True)

                # Refresh the plot
                loss_plot.autoRange()

                channels = [dessin_widget.chan.choices.index(dessin_widget.chan.value),
                            dessin_widget.chan2.choices.index(dessin_widget.chan2.value)]
                square_coords = dessin_widget.viewer.value.layers["little window"].data[0]
                # Récupérer les limites de la région à extraire
                x_min = max(int(np.min(square_coords[:, 0])), 0)
                x_max = int(np.max(square_coords[:, 0]))
                y_min = max(int(np.min(square_coords[:, 1])), 0)
                y_max = int(np.max(square_coords[:, 1]))

                cropped_image = dessin_widget.viewer.value.layers["image"].data[x_min:x_max, y_min:y_max].copy()

                # Brut force solution to  avoid inplace problems during backprop

                mask_labels = model.eval(cropped_image, diameter=int(dessin_widget.diameter_field.value),
                                         flow_threshold=float(dessin_widget.flow_th_field.value),
                                         cellprob_threshold=float(dessin_widget.cell_th_field.value),
                                         channels=channels, omni=OMNI, channel_axis=2)[0]
                dessin_widget.viewer.value.layers["CP result"].data = np.zeros_like(dessin_widget.viewer.value.
                                                                                    layers["CP result"].data)
                dessin_widget.viewer.value.layers["CP result"].data[x_min:x_max, y_min:y_max] = mask_labels
                dessin_widget.viewer.value.layers["CP result"].refresh()
                training_thread.resume()
            else:
                training_thread.pause()
                # Plot the loss values
                loss_curve = loss_plot.plot(loss_list, pen=(255, 102, 0), clear=True)

                # Refresh the plot
                loss_plot.autoRange()

                if (epoch - 1) % int(dessin_widget.show_res_each_button.value) == 0:

                    channels = [dessin_widget.chan.choices.index(dessin_widget.chan.value),
                                dessin_widget.chan2.choices.index(dessin_widget.chan2.value)]

                    # Brut force solution to  avoid inplace problems during backprop
                    mask_labels = model.eval(dessin_widget.viewer.value.layers["image"].data,
                                             diameter=int(dessin_widget.diameter_field.value),
                                             flow_threshold=float(dessin_widget.flow_th_field.value),
                                             cellprob_threshold=float(dessin_widget.cell_th_field.value),
                                             channels=channels, omni=OMNI, channel_axis=2)[0]

                    dessin_widget.viewer.value.layers["CP result"].data = mask_labels
                    dessin_widget.viewer.value.layers["CP result"].refresh()
                training_thread.resume()

    def get_im_from_bbox(layer, bboxes):
        """
        Get image patches from the bbox for the training
        Returns
        -------

        """
        # Create a list to store the subimages
        subimages = []

        # Iterate over each bounding box
        for bbox in bboxes:
            # Extract the coordinates of the bounding box
            xmin, ymin, xmax, ymax = bbox

            # Ensure the coordinates are within the image boundaries
            xmin = np.maximum(0, xmin).astype("int")
            xmax = np.minimum(xmax, layer.shape[:2]).astype("int")

            # Extract the subimage
            subimage = layer[xmin[0]:xmax[0], xmin[1]:xmax[1]]

            # Add the subimage to the list
            subimages.append(subimage)
            plt.imshow(subimage); plt.show()
        return subimages

    def change_training_button_name():
        dessin_widget.train_button.text = "RETRAIN MODEL"
        dessin_widget.train_button.root_native_widget.setChecked(False)

    def plot_loss(res):
        epochs = range(1, len(res[1]) + 1)
        plt.figure()
        plt.plot(epochs, res[1], 'b', label='Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Training loss')
        plt.legend()
        plt.show()

    @dessin_widget.reset_button.changed.connect
    def reset_button():
        global model
        model = "None"

    @dessin_widget.train_button.changed.connect
    def train():
        global training_thread, model, training_threads_list, loss_plot
        if dessin_widget.train_button.root_native_widget.isChecked():

            # Save the labels of current image cause we gonna use them
            save_labels(dessin_widget.Index.value - 1)

            if "loss_plot" not in globals():
                # Create a pyqtgraph GraphicsLayoutWidget to display the loss plot
                pg.setConfigOption('background', (38, 41, 48))  # Set background to white
                pg.setConfigOption('foreground', "w")  # Set foreground (axes, lines, etc.) to black
                loss_plot_widget = pg.GraphicsLayoutWidget()

                # Add the magicgui widget and loss plot widget to the viewer as dock widgets
                dessin_widget.viewer.value.window.add_dock_widget(loss_plot_widget, area='right', name='Loss Plot')

                # Create a PlotItem in the GraphicsLayoutWidget for the loss plot
                loss_plot = loss_plot_widget.addPlot()

                # Set plot labels
                loss_plot.setLabel('left', 'Loss')
                loss_plot.setLabel('bottom', 'Epochs')

            dessin_widget.train_button.text = "STOP TRAINING"
            if "bbox" not in dessin_widget.viewer.value.layers:

                im_list = []
                lab_list = []
                bd_list = []
                D_list = []
                S_list = []

                for p in image_path_list:
                    name, ext = os.path.splitext(os.path.split(p)[1])
                    lab_path = os.path.join(mask_folder, name + "_labels" + ".png")
                    bd_path = os.path.join(mask_folder, name + "_boundaries" + ".png")

                    if os.path.isfile(lab_path) and os.path.isfile(bd_path):
                        lab = imread(lab_path)
                        bd = imread(bd_path)
                        labels, D, S = trusted_region_distance(lab, bd)

                        im_list.append(imread(p))
                        lab_list.append(labels)
                        bd_list.append(bd)
                        D_list.append(D)
                        S_list.append(S)

                if model is "None":
                    load_model()

                channels = [dessin_widget.chan.choices.index(dessin_widget.chan.value),
                            dessin_widget.chan2.choices.index(dessin_widget.chan2.value)]
                if initial_model == "None" and hasattr(model, "optimizer") is False:
                    model = CustomCellposeModel(gpu=True, pretrained_model=False, nchan=2, omni=True)

                model.pretrained_model = "In training"

                # If model is pretrained it's transfer learning, so we freeze the first layers of encoder and
                # decoder

                """if initial_model != "None":
                    from cellpose_omni.resnet_torch import resdown, resup
                    # Freeze the initial layers in the downsample part (encoder)
                    for i, res_down_layer in enumerate(model.net.module.downsample.down.children()):
                        if isinstance(res_down_layer, resdown) in range(3):
                            for param in res_down_layer.parameters():
                                 param.requires_grad = False

                     # Freeze the initial layers in the upsample part (decoder)
                    for i, res_up_layer in enumerate(model.net.module.upsample.up.children()):
                        if isinstance(res_up_layer, resup) and i in range(3):
                            for param in res_up_layer.parameters():
                                param.requires_grad = False

                    show_info("Encoder frozen for transfer learning")"""

                training_thread = thread_worker(model.train, progress={"total": epochs_nb})(im_list, lab_list,
                                                D_list, S_list, n_epochs=epochs_nb, SGD=SGD,
                                                learning_rate=LR, min_train_masks=1, save_path=parent_path,
                                                channels=channels, channel_axis=2)

                # Store all processes to make sure to kill them all when clicking stop training
                training_threads_list.append(training_thread)

                # Version without multi thread
                #model.train([image], [labels], [D], [S], n_epochs=200, SGD=False, learning_rate=0.1, min_train_masks=1)
                training_thread.yielded.connect(on_yielded)
                # if training stops naturally reset button
                training_thread.finished.connect(change_training_button_name)
                training_thread.returned.connect(plot_loss)
                training_thread.start()
            else:

                images_list = []
                labels_list = []
                D_list = []
                S_list = []

                for p in image_path_list:
                        name, ext = os.path.splitext(os.path.split(p)[1])
                        lab_path = os.path.join(mask_folder, name + "_labels.png")
                        bd_path = os.path.join(mask_folder, name + "_boundaries.png")
                        bbox_path = os.path.join(mask_folder, name + "_bbox.csv")

                        if os.path.isfile(lab_path) and os.path.isfile(bd_path) and os.path.isfile(bbox_path):

                            df = pd.read_csv(bbox_path)
                            bbox = []
                            # Itérez sur les groupes de lignes (index) dans le DataFrame
                            for index, group in df.groupby('index'):
                                # Ajoutez les coordonnées des quatre coins à la liste globale
                                bbox.append(group[['axis-0', 'axis-1']].to_numpy())

                            # Store all bbox patches in a list
                            images = get_im_from_bbox(imread(p), bbox)
                            labels_patches = get_im_from_bbox(imread(lab_path), bbox)
                            boundaries_patches = get_im_from_bbox(imread(bd_path), bbox)

                            for i in range(len(labels_patches)):
                                labels, D, S = trusted_region_distance(labels_patches[i], boundaries_patches[i])
                                images_list.append(images[i])
                                labels_list.append(labels)
                                D_list.append(D)
                                S_list.append(S)

                dessin_widget.viewer.value.layers["labels"].refresh()
                dessin_widget.viewer.value.layers["boundaries"].refresh()

                # Training of all bboxes
                channels = [dessin_widget.chan.choices.index(dessin_widget.chan.value),
                            dessin_widget.chan2.choices.index(dessin_widget.chan2.value)]
                if model is "None":
                    load_model()

                if initial_model == "None" and hasattr(model, "optimizer") is False:
                    model = CustomCellposeModel(gpu=True, pretrained_model=False, nchan=2, omni=True)

                model.pretrained_model = "In training"

                training_thread = thread_worker(model.train, progress={"total": epochs_nb})(images_list, labels_list, D_list,
                                                                                            S_list, n_epochs=epochs_nb,
                                                                                            SGD=SGD, learning_rate=LR,
                                                                                            min_train_masks=1,
                                                                                            save_path=parent_path,
                                                                                            channels=channels,
                                                                                            channel_axis=2)
                # Store all processes to make sure to kill them all when clicking stop training
                training_threads_list.append(training_thread)

                training_thread.yielded.connect(on_yielded)
                # if training stops naturally reset button
                training_thread.finished.connect(change_training_button_name)
                training_thread.returned.connect(plot_loss)
                training_thread.start()

        else:
            # this makes sure that if there are several simultaneaous processes remaining that they all get killed
            for thread in training_threads_list:
                thread.quit()
            training_threads_list.clear()
            change_training_button_name()

            # Model saving if training is stopped manually
            d = datetime.now()
            _, file_label = os.path.split(parent_path)
            file_path = os.path.join(parent_path, 'models/')
            file_name = '{}_{}_{}_{}'.format(file_path, model.net_type, file_label,
                                             d.strftime("%Y_%m_%d_%H_%M_%S.%f") + '_epoch_' + str(epoch))
            if model.torch and model.gpu:
                model.net.module.save_model(file_name)
            else:
                model.net.save_model(file_name)

    return dessin_widget


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [Dessin]
