from qtpy.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication, QLineEdit, QCheckBox, QMessageBox,\
    QDialogButtonBox, QComboBox, QLabel, QHBoxLayout


class TrainingDialog(QDialog):
    def __init__(self, models_list, parent=None, saved_values=None):
        super().__init__(parent)
        self.setWindowTitle("Training options")
        self.setStyleSheet(QApplication.instance().styleSheet())  # Apply Napari style sheet

        # Create the widgets for setting up training
        self.model_field_label = QLabel("Initial model")
        self.model_field = QComboBox()
        self.model_field.addItems(models_list)
        self.model_field.setCurrentIndex(1)

        self.chan1_label = QLabel("Chan to segment")
        self.chan1 = QComboBox()
        self.chan1.addItems(["gray", "red", "green", "blue"])
        self.chan1.setCurrentIndex(0)

        self.chan2_label = QLabel("Chan2 (optional)")
        self.chan2 = QComboBox()
        self.chan2.addItems(["None", "red", "green", "blue"])
        self.chan2.setCurrentIndex(0)

        self.lr_field_label = QLabel("Learning rate")
        self.lr_field = QLineEdit()
        self.lr_field.setText(str(0.1))
        self.w_decay_field_label = QLabel("Weight decay")
        self.w_decay_field = QLineEdit()
        self.w_decay_field.setText("0.0001")
        self.n_epochs_field_label = QLabel("Epochs number")
        self.n_epochs_field = QLineEdit()
        self.n_epochs_field.setText(str(100))

        self.checkbox = QCheckBox("Use SGD (else RAdam)")

        # Create the buttons for actions
        self.button_validate = QPushButton("Validate")
        self.button_cancel = QPushButton("Cancel")
        self.button_reset = QPushButton("Reset values")

        # Layout for the dialog
        layout = QVBoxLayout()
        # Add each pair of label and field to a horizontal layout
        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self.model_field_label)
        fields_layout.addWidget(self.model_field)
        layout.addLayout(fields_layout)

        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self.chan1_label)
        fields_layout.addWidget(self.chan1)
        layout.addLayout(fields_layout)

        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self.chan2_label)
        fields_layout.addWidget(self.chan2)
        layout.addLayout(fields_layout)

        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self.lr_field_label)
        fields_layout.addWidget(self.lr_field)
        layout.addLayout(fields_layout)

        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self.w_decay_field_label)
        fields_layout.addWidget(self.w_decay_field)
        layout.addLayout(fields_layout)

        fields_layout = QHBoxLayout()
        fields_layout.addWidget(self.n_epochs_field_label)
        fields_layout.addWidget(self.n_epochs_field)
        layout.addLayout(fields_layout)

        layout.addWidget(self.checkbox)

        # Create a button box and add the buttons to it
        button_box = QDialogButtonBox()
        button_box.addButton(self.button_validate, QDialogButtonBox.AcceptRole)
        button_box.addButton(self.button_cancel, QDialogButtonBox.RejectRole)
        button_box.addButton(self.button_reset, QDialogButtonBox.ResetRole)
        layout.addWidget(button_box)

        self.setLayout(layout)

        # Connect the button signals to the appropriate slots
        self.button_validate.clicked.connect(self.accept)
        self.button_cancel.clicked.connect(self.reject)
        self.button_reset.clicked.connect(self.load_default_values)

        # If new values never set, then it does not exist so we load default values
        if saved_values is not None:
            self.set_saved_values(saved_values)

    def set_saved_values(self, saved_values):
        self.model_field.setCurrentText(saved_values["initial_model"])
        self.chan1.setCurrentText(saved_values["chan1"])
        self.chan2.setCurrentText(saved_values["chan2"])
        self.lr_field.setText(str(saved_values["LR"]))
        self.w_decay_field.setText(str(saved_values["w_decay"]))
        self.n_epochs_field.setText(str(saved_values["epochs_nb"]))
        self.checkbox.setChecked(saved_values["SGD"])

    def load_default_values(self):
        # Load the default values into the fields
        self.model_field.setCurrentIndex(1)
        self.chan1.setCurrentIndex(0)
        self.chan2.setCurrentIndex(0)
        self.lr_field.setText(str(0.1))
        self.w_decay_field.setText("0.0001")
        self.n_epochs_field.setText(str(100))

    def accept(self):
        if self.validate_values():
            super().accept()
        else:
            QMessageBox.warning(self, "Validation Error", "Invalid values entered.")

    def validate_values(self):
        # Perform validation checks here
        text_value = self.lr_field.text()
        if not text_value:
            return False

        # Additional validation checks...

        return True
