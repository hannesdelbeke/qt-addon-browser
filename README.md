# qt-addon-browser
A add-on browser widget, to quickly open blender add-on folders in explorer.
To help speed up add-on development.

| ![image](https://github.com/hannesdelbeke/qt-addon-browser/assets/3758308/6406ff21-28eb-47fc-a9c5-e530c98789c1) | ![image](https://github.com/hannesdelbeke/qt-addon-browser/assets/3758308/9ce48dba-dc13-497e-9b16-9d380966bbd8) |
| -- | -- |
| qt-addon-browser  | default add-on browser in Preferences  | 

## Requirements
- [bqt](https://github.com/techartorg/bqt)

## Feature planned

### Main prio:
- [x] no option to right click, open addon install directory

### copy default blender addon manager features
- [ ] enable disable
- [x] list all addons
- [x] search addons by name
- [x] show explorer path (but no copy)
- [x] docs button
- [ ] bug report button
- [ ] preferences
- [ ] addon install

### Stretch goals
fix minor issues with the default addon browser 
- [ ] shows all addons, no option to filter out default addons
- [ ] no option to filter by directory
- [ ] no easy option to customize.
- [x] search bar doesn't stay at top when scrolling down

Wishlist
- [ ] can we have some kind of view mode to see what data is saved to blender cloud?
  unsure how this works atm
- [ ] support display (e.g. as red) even if addon not correctly installed. (e.g. when a folder with files is in the addon folder without a correct python script setup)
- [ ] show dependencies
	- [ ] python libs based on requirements?
	- [ ] other dependencies, e.g. blend files?
- [ ] editable install (point to local addon working repo or project)

## Community
- https://blenderartists.org/t/free-addon-browser/1478372
