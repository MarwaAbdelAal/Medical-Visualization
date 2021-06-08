# Volume rendering app with VTK & Qt

## GUI was built using pyqt5 

You can load DICOM images by clicking load file or one of the two buttons "_Surface renderning, Ray casting rendering_":

![gui](images/1.jpeg)

- File Upload Function `loadDir`

## Surface rendering Function `surface_rendering`

Here the isovalue = 500

![surface rendering, isovalue=500](images/2.jpeg)

- Sliders are used to adjust ISO values of surface Rendering Using the Function `isovalue_slider`

![surface rendering, isovalue=0](images/3.jpeg)

## Ray Casting has been done by the Function `rayCasting_rendering`

![head raycasting](images/4.jpeg)

![ankle raycasting](images/5.jpeg)

- Adjusting the Opacity and the RGB color of the Casting Ray by Using the Function `transferFunc_slider`

- Controlling the Opacity slider: 
![alt text](images/6.jpeg)

- Controlling the RGB color sliders:
  
  ![alt text](images/7.jpeg)
  
  ![alt text](images/8.jpeg)
  
  ![alt text](images/9.jpeg)

***

# Run the app

```bash
python app.y
```