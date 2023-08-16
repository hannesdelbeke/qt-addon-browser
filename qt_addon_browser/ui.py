import bpy
from PySide2 import QtWidgets, QtGui, QtCore
import addon_utils
import os
import webbrowser


class AddonUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blender Addon Manager")
        self.setMinimumWidth(400)

        self.search_box = QtWidgets.QLineEdit()
        self.addons_layout = QtWidgets.QVBoxLayout()

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.populate_addons()

        self.search_box.textChanged.connect(self.filter_addons)  # Connect the textChanged signal

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.search_box)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def populate_addons(self):
        self.addons = self.get_all_addons()

        for addon in self.addons:
            addon_widget = self.create_addon_widget(addon)
            self.scroll_layout.addWidget(addon_widget)
        self.scroll_layout.addStretch(1)  # Add a stretch factor to keep buttons at the top

    def get_all_addons(self):
        all_addons = []

        for addon_module in addon_utils.modules():
            if hasattr(addon_module, "bl_info"):
                addon_name = addon_module.bl_info["name"]
                addon_enabled = addon_name in bpy.context.preferences.addons.keys()
                all_addons.append(
                    {"module": addon_module,
                     "name": addon_name,
                     "enabled": addon_enabled,
                     })

        return all_addons

    def create_addon_widget(self, addon):
        addon_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(addon["name"])
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)  # Label expands horizontally

        checkbox = QtWidgets.QCheckBox()
        checkbox.setChecked(addon["enabled"])
        checkbox.stateChanged.connect(self.toggle_addon_enabled)

        doc_button = QtWidgets.QPushButton("📄")
        doc_button.setFixedSize(QtCore.QSize(24, 24))  # Adjust the size as needed
        doc_button.clicked.connect(lambda: self.open_documentation(addon=addon))

        folder_button = QtWidgets.QPushButton("📂")
        folder_button.setFixedSize(QtCore.QSize(24, 24))  # Adjust the size as needed
        folder_button.clicked.connect(lambda: self.open_install_folder(addon=addon))

        layout.addWidget(checkbox)
        layout.addWidget(label)
        layout.addWidget(doc_button)
        layout.addWidget(folder_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        addon_widget.setLayout(layout)

        return addon_widget

    def toggle_addon_enabled(self, state):
        sender = self.sender()
        index = self.addons_layout.indexOf(sender.parentWidget())
        self.addons[index]["enabled"] = state == QtCore.Qt.Checked

    def open_documentation(self, addon):
        addon_module = addon["module"]
        if "doc_url" in addon_module.bl_info:
            documentation_url = addon_module.bl_info["doc_url"]
            webbrowser.open_new_tab(documentation_url)
        else:
            QtWidgets.QMessageBox.warning(self, "Documentation Not Available",
                                          "No documentation URL provided for this addon.")

    def open_install_folder(self, addon):
        addon_module = addon["module"]
        if addon_module:
            addon_folder = os.path.dirname(addon_module.__file__)
            os.startfile(addon_folder)  # Opens the folder in the default file explorer

    def filter_addons(self):
        search_text = self.search_box.text().lower()
        for index in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(index).widget()
            if search_text in widget.layout().itemAt(1).widget().text().lower():
                widget.show()
            else:
                widget.hide()


def show_ui():
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)
    widget = AddonUI()
    widget.show()
    return widget


if __name__ == "__main__":
    widget = show_ui()
