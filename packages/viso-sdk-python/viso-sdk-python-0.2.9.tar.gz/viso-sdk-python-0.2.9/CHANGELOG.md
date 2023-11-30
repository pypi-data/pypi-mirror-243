# Changelog

<!--next-version-placeholder-->

## v0.1.3

### Enhancements
- Update visualization for dynamic fonts  

### Features

### Fix
- init_font() - the case of not existing font_name


## v0.2.2

### Enhancements
### Features
- new declaration of modules 
### Fix
- VizObj, VizRoi - missed arguments (text_color)
- update default shadow_color with pillow RGBA format(255, 0, 0, 255) = RED
 
## v0.2.3

### Enhancements
### Features
- added drawer function for (line-type) roi objects  
### Fix
- visualize.utils.put_text() - correct padding calculation
- visualize.utils.put_text() - treat multi-line text too
- visualize.utils.put_text() - added option for center align


## v0.2.4

### Enhancements
### Features
- sphinx autodoc  
### Fix


## v0.2.5

### Enhancements
### Features
### Fix
- update function to calculate padding in the case of multi-line text
- add new framework TensorRT
- update utils.put_text() parameter names


## v0.2.6

### Enhancements
### Features
### Fix
- update other viz functions (vis_obj, vis_roi) using updated utils.put_text()


## v0.2.7(v0.2.8)
### Enhancements
- constants - add common keys for object tracking/recognition
- visualization:
  - add draw_tracking_objects
  - ignore empty object lists on visualization function 
### Features


## v0.2.9
### Enhancements
- more detailed visualization parameters 
### Features
