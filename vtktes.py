
import vtk

# Read the DICOM images
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName("imgs/")  # folder containing DICOM files
reader.Update()

# Create an image viewer
imageViewer = vtk.vtkImageViewer2()
imageViewer.SetInputConnection(reader.GetOutputPort())

# Setup render window, renderer, and interactor
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
imageViewer.SetupInteractor(renderWindowInteractor)
imageViewer.Render()

# Start interaction
renderWindowInteractor.Start()