bl_info = {
        "name": "Qt Addon Browser",
        "description": "browse add-ons. Enable the addon to show the browser window.",
        "author": "Hannes",
        "version": (1, 0),
        "blender": (2, 80, 0),
        "support": "COMMUNITY",
        "category": "Develop"
        }

#         "location": "",
#         "warning": "",
#         "wiki_url": "http://my.wiki.url",
#         "tracker_url": "http://my.bugtracker.url",




def register():
    from qt_addon_browser import ui
    ui.show_ui()
    pass


def unregister():
    pass


if __name__ == '__main__':
    register()
