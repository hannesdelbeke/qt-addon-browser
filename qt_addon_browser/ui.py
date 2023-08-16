import logging

import bpy
from PySide2 import QtWidgets, QtGui, QtCore
import addon_utils
import os
import webbrowser
import contextlib


def open_addons_preferences():
    window = bpy.context.window_manager.windows[0]
    with bpy.context.temp_override(window=window):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.context.preferences.active_section = 'ADDONS'
    # todo pass the search box value to the addons preferences search box


def enable_addon(addon_module_name: str):
    """Enable an addon by its module name."""
    _, loaded_state = addon_utils.check(addon_module_name)

    if not loaded_state:
        with contextlib.suppress(ModuleNotFoundError):
            addon_utils.enable(
                addon_module_name,
                default_set=True,
                persistent=True,
                handle_error=lambda x: print("Error enabling addon:", x),
            )


def disable_addon(addon_module_name: str):
    """Enable an addon by its module name."""
    _, loaded_state = addon_utils.check(addon_module_name)

    if loaded_state:
        with contextlib.suppress(ModuleNotFoundError):
            addon_utils.disable(
                addon_module_name,
                default_set=True,
                handle_error=lambda x: print("Error disabling addon:", x),
            )


def addon_is_enabled(addon_module_name):
    return addon_module_name in bpy.context.preferences.addons.keys()


def get_all_addons():
    all_addons = []

    for addon_module in addon_utils.modules():
        if hasattr(addon_module, "bl_info"):
            addon_name = addon_module.bl_info["name"]
            addon_enabled = addon_name in bpy.context.preferences.addons.keys()
            all_addons.append(
                {"module": addon_module,
                 "name": addon_name,
                 })

    return all_addons


def open_install_folder(addon):
    addon_module = addon["module"]
    if addon_module:
        addon_folder = os.path.dirname(addon_module.__file__)
        os.startfile(addon_folder)  # Opens the folder in the default file explorer


def open_documentation(self, addon, parent):
    addon_module = addon["module"]
    if "doc_url" in addon_module.bl_info:
        documentation_url = addon_module.bl_info["doc_url"]
        webbrowser.open_new_tab(documentation_url)
    else:
        QtWidgets.QMessageBox.warning(self, "Documentation Not Available",
                                      "No documentation URL provided for this addon.")


class AddonUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(objectName="addon_manager_main_widget")
        self.setWindowTitle("Blender Addon Manager")
        self.setMinimumWidth(400)

        self.open_addons_preferences_button = QtWidgets.QPushButton("Open Preferences Add-ons")
        self.search_box = QtWidgets.QLineEdit()
        self.addons_layout = QtWidgets.QVBoxLayout()

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        self.populate_addons()

        self.open_addons_preferences_button.clicked.connect(open_addons_preferences)
        self.search_box.textChanged.connect(self.filter_addons)  # Connect the textChanged signal

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.open_addons_preferences_button)
        main_layout.addWidget(self.search_box)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def populate_addons(self):
        self.addons = get_all_addons()

        for addon in self.addons:
            addon_widget = self.create_addon_widget(addon)
            self.scroll_layout.addWidget(addon_widget)
        self.scroll_layout.addStretch(1)  # Add a stretch factor to keep buttons at the top

    def create_addon_widget(self, addon):
        addon_module = addon["module"]
        addon_enabled = addon_is_enabled(addon_module.__name__)

        addon_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(addon["name"])
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)  # Label expands horizontally

        checkbox = QtWidgets.QCheckBox()
        checkbox.setChecked(addon_enabled)
        # connect stateChanged after setting the initial state, otherwise it triggers the callback
        checkbox.stateChanged.connect(lambda: self.toggle_addon_enabled(addon=addon, checkbox=checkbox))
        
        doc_button = QtWidgets.QPushButton("📄")
        doc_button.setFixedSize(QtCore.QSize(24, 24))  # Adjust the size as needed
        doc_button.clicked.connect(lambda: open_documentation(addon=addon, parent=self))

        folder_button = QtWidgets.QPushButton("📂")
        folder_button.setFixedSize(QtCore.QSize(24, 24))  # Adjust the size as needed
        folder_button.clicked.connect(lambda: open_install_folder(addon=addon))

        layout.addWidget(checkbox)
        layout.addWidget(label)
        layout.addWidget(doc_button)
        layout.addWidget(folder_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        addon_widget.setLayout(layout)

        return addon_widget
    
    def toggle_addon_enabled(self, addon, checkbox):
        # TODO add timer to check if addon is disabled outside of this ui

        # print(f"Checkbox enabled: {checkbox.isEnabled()}")
        # checkbnox isEnabled always returns true atm.

        addon_module = addon["module"]
        addon_module_name = addon_module.__name__
        addon_enabled = addon_is_enabled(addon_module_name)

        # if checkbox.isEnabled() and not addon_enabled:
        if not addon_enabled:  # todo this is a naive toggle and ignores the checkbox state atm. fix this
            print(f"Enabling addon {addon_module_name}")
            enable_addon(addon_module_name)
        # elif (not checkbox.isEnabled()) and addon_enabled:
        elif addon_enabled:
            print(f"Disabling addon {addon_module_name}")
            disable_addon(addon_module_name)

    def filter_addons(self):
        search_text = self.search_box.text().lower()
        for index in range(self.scroll_layout.count() - 1):  # -1 to ignore the stretch factor
            widget = self.scroll_layout.itemAt(index).widget()

            # this shouldn't happen, but just in case.
            # if it happens likely UI code was updated, see -1 above
            if not widget:
                logging.warning(f"Widget not found at index {index}/{self.scroll_layout.count()}")
                continue

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
