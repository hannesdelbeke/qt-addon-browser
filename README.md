# qt-addon-browser
A add-on browser widget, to quickly open blender addon folders in explorer

## Goals

main goal:
- [x] no option to right click, open addon install directory

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

### copy default blender addon manager features
- [ ] enable disable
- [x] list all addons
- [x] search addons by name
- [x] show explorer path (but no copy)
- [x] docs button
- [ ] bug report button
- [ ] preferences
- [ ] addon install
