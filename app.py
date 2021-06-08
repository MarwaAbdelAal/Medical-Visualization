import sys
from PyQt5 import QtWidgets
import myGui
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
import os

surfaceExtractor = vtk.vtkContourFilter()

class MainWindow(QtWidgets.QMainWindow , myGui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.Menubar()
        self.dataDir = None
        self.val = self.isoValueSlider.value()
        self.transferFunc = [self.redSlider.value()/100.0 , self.greenSlider.value()/100.0 , self.blueSlider.value()/100.0 , self.opacitySlider.value()/100.0]

        self.pushButton.clicked.connect(lambda: self.loadDir(0))
        self.pushButton_2.clicked.connect(lambda: self.loadDir(1))

        self.isoValueSlider.valueChanged.connect(self.isovalue_slider)
        self.redSlider.valueChanged.connect(self.transferFunc_slider)
        self.greenSlider.valueChanged.connect(self.transferFunc_slider)
        self.blueSlider.valueChanged.connect(self.transferFunc_slider)
        self.opacitySlider.valueChanged.connect(self.transferFunc_slider)

    def isovalue_slider(self):
        self.val = self.isoValueSlider.value()
        surfaceExtractor.SetValue(0, self.val)
        iren_surface.update()
    
    def transferFunc_slider(self):
        self.transferFunc = [self.redSlider.value()/100.0 , self.greenSlider.value()/100.0 , self.blueSlider.value()/100.0 , self.opacitySlider.value()/100.0]
        if self.dataDir:
            rayCasting_rendering(self.dataDir , self.transferFunc)

    #connecting menubar buttons to their functions
    def Menubar(self):
        self.actionSurface_rendering.triggered.connect(lambda: self.loadDir(0))
        self.actionRay_casting_rendering.triggered.connect(lambda: self.loadDir(1))
 
    def loadDir(self , state):
        self.dataDir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if self.dataDir:
            if state:
                rayCasting_rendering(self.dataDir, self.transferFunc)
            else:
                surface_rendering(self.dataDir, self.val)


def surface_rendering(dataDir, val):
    aRenderer = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(aRenderer)
    iren_surface = vtk.vtkRenderWindowInteractor()
    iren_surface.SetRenderWindow(renWin)

    # Read Dataset using vtkDICOMImageReader 
    v = vtk.vtkDICOMImageReader()
    v.SetDataByteOrderToLittleEndian()
    v.SetDirectoryName(dataDir)
    v.SetDataSpacing(3.2, 3.2, 1.5)
    
    # An isosurface, or contour value of 500 is known to correspond to the
    surfaceExtractor = vtk.vtkContourFilter()
    surfaceExtractor.SetInputConnection(v.GetOutputPort())
    surfaceExtractor.SetValue(0, val)
    surfaceNormals = vtk.vtkPolyDataNormals()
    surfaceNormals.SetInputConnection(surfaceExtractor.GetOutputPort())
    surfaceNormals.SetFeatureAngle(60.0)
    surfaceMapper = vtk.vtkPolyDataMapper()
    surfaceMapper.SetInputConnection(surfaceNormals.GetOutputPort())
    surfaceMapper.ScalarVisibilityOff()
    surface = vtk.vtkActor()
    surface.SetMapper(surfaceMapper)
    
    aCamera = vtk.vtkCamera()
    aCamera.SetViewUp(0, 0, -1)
    aCamera.SetPosition(0, 1, 0)
    aCamera.SetFocalPoint(0, 0, 0)
    aCamera.ComputeViewPlaneNormal()
    
    aRenderer.AddActor(surface)
    aRenderer.SetActiveCamera(aCamera)
    aRenderer.ResetCamera()
    aCamera.Dolly(1)
    
    aRenderer.SetBackground(0, 0, 0)
    renWin.SetSize(640, 480)
    
    aRenderer.ResetCameraClippingRange()
    
    # Interact with the data.
    iren_surface.Initialize()
    renWin.Render()
    iren_surface.Start()
    # iren_surface.show()


def rayCasting_rendering(dataDir, transferFunc):
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren_rayCasting = vtk.vtkRenderWindowInteractor()
    iren_rayCasting.SetRenderWindow(renWin)
    
    # Read Dataset using vtkDICOMImageReader 
    v = vtk.vtkDICOMImageReader()
    v.SetDataByteOrderToLittleEndian()
    v.SetDirectoryName(dataDir)
    v.SetDataSpacing(3.2, 3.2, 1.5)

    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(v.GetOutputPort())
    volumeMapper.SetBlendModeToComposite()
    
    # The color transfer function maps voxel intensities to colors.
    volumeColor = vtk.vtkColorTransferFunction()
    volumeColor.AddRGBPoint(0,    0.0, 0.0, 0.0)
    # volumeColor.AddRGBPoint(500,  1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(500,  transferFunc[0], transferFunc[1], transferFunc[2])
    volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)
    
    # The opacity transfer function is used to control the opacity of different tissue types.
    volumeScalarOpacity = vtk.vtkPiecewiseFunction()
    volumeScalarOpacity.AddPoint(0,    0.00)
    # volumeScalarOpacity.AddPoint(500,  0.15)
    volumeScalarOpacity.AddPoint(500,  transferFunc[3])
    volumeScalarOpacity.AddPoint(1000, 0.15)
    volumeScalarOpacity.AddPoint(1150, 0.85)
    
    # The gradient opacity function is used to decrease the opacity
    volumeGradientOpacity = vtk.vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(0,   0.0)
    volumeGradientOpacity.AddPoint(90,  0.5)
    volumeGradientOpacity.AddPoint(100, 1.0)
    
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(volumeColor)
    volumeProperty.SetScalarOpacity(volumeScalarOpacity)
    volumeProperty.SetGradientOpacity(volumeGradientOpacity)
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    
    # Finally, add the volume to the renderer
    ren.AddViewProp(volume)

    camera =  ren.GetActiveCamera()
    c = volume.GetCenter()
    camera.SetFocalPoint(c[0], c[1], c[2])
    camera.SetPosition(c[0] + 400, c[1], c[2])
    camera.SetViewUp(0, 0, -1)
    
    # Increase the size of the render window
    renWin.SetSize(640, 480)
    
    # Interact with the data.
    iren_rayCasting.Initialize()
    renWin.Render()
    iren_rayCasting.Start()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # The class that connect Qt with VTK
    iren_surface = QVTKRenderWindowInteractor()
    iren_rayCasting = vtk.vtkRenderWindowInteractor()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




