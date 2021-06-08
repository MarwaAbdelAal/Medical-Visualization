# Volume rendering app with Visualization Toolkit (VTK) & Qt

Objective is to create a 3D object from series of 2D images

## GUI was built using pyqt5 

You can load DICOM images series dynamically by clicking on load file or by clicking one of the two buttons "_Surface renderning, Ray casting rendering_":

![gui](images/gui.jpeg)

- File Upload Function `loadDir`

## Surface rendering

- it's done using the function `surface_rendering`

Here, the isovalue = 500

![surface rendering, isovalue=500](images/surface_rendering_500.jpeg)

- Sliders are used to adjust ISO value of surface Rendering Using the function `isovalue_slider`

Here, the isovalue = 0

![surface rendering, isovalue=0](images/surface_rendering_0.jpeg)

## Ray casting for direct volume rendering

 - it's done by the function `rayCasting_rendering`

Head ray casting:

![head raycasting](images/head_raycasting.jpeg)

Ankle ray casting:

![ankle raycasting](images/ankle_raycasting.jpeg)

- Adjusting the Opacity and the RGB color of the Casting Ray by Using the Function `transferFunc_slider`

- Controlling the Opacity slider: 
 
  ![adjusting opacity slider](images/opacity_slider.jpeg)

- Controlling the RGB color sliders:
  
  ![adjusting redColor slider](images/redColor_slider.jpeg)
  
  ![adjusting greenColor slider](images/greenColor_slider.jpeg)
  
  ![adjusting blueColor slider](images/blueColor_slider.jpeg)

***

# Run the app

```bash
python app.y
```
