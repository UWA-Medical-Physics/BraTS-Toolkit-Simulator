import os
import unittest
import logging
import vtk, qt, ctk, slicer
import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# Brain tumor Segmentation
#

class BrainTumorSegmentation(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "BrainTumorSegmentation"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Slicer-BratsToolkit"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["Saima Safdar (The University of Western Australia)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """This extension is for automatically segmenting the brain tumor (glioblastoma) for a number of patients using brats toolkit.
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#BrainTumorSegmentation">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """

"""

    # Additional initialization step after application startup is complete
    slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#

def registerSampleData():
  """
  Add data sets to Sample Data module.
  """
  # It is always recommended to provide sample data for users to make it easy to try the module,
  # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  import SampleData
  iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # it is recommended to store data sets that are larger than a few MB in a Github release.

  # BrainTumorSegmentation1
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='BrainTumorSegmentation',
    sampleName='BrainTumorSegmentation1',
    # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
    # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
    thumbnailFileName=os.path.join(iconsPath, 'BrainTumorSegmentation.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
    fileNames='BrainTumorSegmentation.nrrd',
    # Checksum to ensure file integrity. Can be computed by this command:
    #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    checksums = 'SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
    # This node name will be used when the data set is loaded
    nodeNames='BrainTumorSegmentation'
  )

  # BrainTumorSegmentation2
  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='BrainTumorSegmentation',
    sampleName='BrainTumorSegmentation',
    thumbnailFileName=os.path.join(iconsPath, 'BrainTumorSegmentation.png'),
    # Download URL and target file name
    uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
    fileNames='BrainTumorSegmentation.nrrd',
    checksums = 'SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
    # This node name will be used when the data set is loaded
    nodeNames='BrainTumorSegmentation'
  )

#
# BrainTumorSegmentationWidget
#

class BrainTumorSegmentationWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False
    self.logCallback = None

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/BrainTumorSegmentation.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = BrainTumorSegmentationLogic()
    self.logic.logCallback = self.addLog
    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    #self.ui.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    #self.ui.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    
    
   
    
    
    # self.layout = self.parent.layout()
    # self.textbox = qt.QTextEdit()
    # self.layout.addWidget(self.textbox)

    # Buttons
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Make sure parameter node is initialized (needed for module reload)
    self.initializeParameterNode()

  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())

    # Select default input nodes if nothing is selected yet to save a few clicks for the user
    if not self._parameterNode.GetNodeReference("InputVolume"):
      firstVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
      if firstVolumeNode:
        self._parameterNode.SetNodeReferenceID("InputVolume", firstVolumeNode.GetID())

  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True

    # Update node selectors and sliders
    #self.ui.inputSelector.setCurrentNode(self._parameterNode.GetNodeReference("InputVolume"))
    #self.ui.outputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolume"))
    #self.ui.invertedOutputSelector.setCurrentNode(self._parameterNode.GetNodeReference("OutputVolumeInverse"))
    


    # Update buttons states and tooltips
# =============================================================================
#     if self._parameterNode.GetNodeReference("InputVolume") and self._parameterNode.GetNodeReference("OutputVolume"):
#       self.ui.applyButton.toolTip = "Compute output volume"
#       self.ui.applyButton.enabled = True
#     else:
#       self.ui.applyButton.toolTip = "Select input and output volume nodes"
#       self.ui.applyButton.enabled = False
# =============================================================================

    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

    #self._parameterNode.SetNodeReferenceID("InputVolume", self.ui.inputSelector.currentNodeID)
    #self._parameterNode.SetNodeReferenceID("OutputVolume", self.ui.outputSelector.currentNodeID)
   
    #self._parameterNode.SetParameter("Invert", "true" if self.ui.invertOutputCheckBox.checked else "false")
   

    self._parameterNode.EndModify(wasModified)

  def addLog(self, text):
    """Append text to log window
    """
    import re
   
    if re.search("^APT.*[0-9]+$", text,flags = re.IGNORECASE):
        self.ui.cPatient.appendPlainText(text)
        slicer.app.processEvents()
    else:
        self.ui.statusLabel.appendPlainText(text)
        slicer.app.processEvents()  # force update

  
  def onApplyButton(self):
    """
    Run processing when user clicks "Apply" button.
    """
    with slicer.util.tryWithErrorDisplay("Unexpected error.",waitCursor=True):#try:
      # Compute output
      self.ui.statusLabel.plainText = '' #initialise the container to output the progress of your terminal window or python interpreter
      self.ui.cPatient.plainText = '' 
      dataDirectoryPath = self.ui.dataDirectoryPath.directory
      pythonPath = self.ui.pythonPath.currentPath
      patientID= self.ui.patientID.value
      #l = self.ui.listAlgo.currentText
      #print(l)
     
      items = self.ui.listWidget1.selectedItems()
      nnModels= []
      for i in range(len(items)):
          nnModels.append(str(self.ui.listWidget1.selectedItems()[i].text()))
      print (nnModels)
      
      
      
      self.logic.process(nnModels, dataDirectoryPath, pythonPath, patientID)#,self.ui.imageThresholdSliderWidget.value, self.ui.invertOutputCheckBox.checked)
      self.ui.statusLabel.appendPlainText("\nProcessing finished.")
      # Compute inverted output (if needed)
      #if self.ui.invertedOutputSelector.currentNode():
        # If additional output volume is selected then result with inverted threshold is written there
        #self.logic.process(self.ui.inputSelector.currentNode(), self.ui.invertedOutputSelector.currentNode(),
         # self.ui.imageThresholdSliderWidget.value, not self.ui.invertOutputCheckBox.checked, showResult=False)
     
         
    # except Exception as e:
    #   slicer.util.errorDisplay("Failed to compute results: "+str(e))
    #   import traceback
    #   traceback.print_exc()


#
# BrainTumorSegmentationLogic
#

class BrainTumorSegmentationLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
 
            
  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)
    self.logCallback = None

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("Threshold"):
      parameterNode.SetParameter("Threshold", "100.0")
    if not parameterNode.GetParameter("Invert"):
      parameterNode.SetParameter("Invert", "false")
      
  def log(self, text):
    logging.info(text)
    if self.logCallback:
      self.logCallback(text)
      
  def logProcessOutput(self, proc):
        # Wait for the process to end and forward output to the log
        from subprocess import CalledProcessError
        while True:
            try:
                line = proc.stdout.readline()
            except UnicodeDecodeError as e:
                # Code page conversion happens because `universal_newlines=True` sets process output to text mode,
                # and it fails because probably system locale is not UTF8. We just ignore the error and discard the string,
                # as we only guarantee correct behavior if an UTF8 locale is used.
                pass
            if not line:
                break
            self.log(line.rstrip())
        proc.wait()
        retcode = proc.returncode
        if retcode != 0:
            raise CalledProcessError(retcode, proc.args, output=proc.stdout, stderr=proc.stderr)

  def process(self, nnModels, directoryPath, pythonPath, patientID): 
    """
    #, imageThreshold, invert=False, showResult=True):
    Run the processing algorithm.
    Can be used without GUI widget.
    :param nnModels: list of neural network models used for segmentation
    :param directoryPath: the path to the directory containing the patient data
    :param pythonPath: the path to the Python interpreter to be used with installed brattoolkit librariries
    :param patientID: an integer indicating the patient ID to start processing from
    
    """

  

    import time
    import os
    import re
    import csv
    import pandas as pd
    startTime = time.time()
    self.log('Processing started............\n')
    mDirName = os.path.basename(directoryPath)
    print(mDirName)
    #creating a dataframe that contains the patinet ID and dir anme and the directory path
    #search for the patient to get dir name and dir path to start working on that directory
    print(nnModels)
    dirPaths = []
    dirNames = []
    for root, dirs, files in os.walk(directoryPath, topdown=False):
            for dir in [os.path.join(root,d) for d in dirs]:
                #print(dir)
                rx = re.compile(r"^.*/"+re.escape(mDirName)+r"/.*APT.*\d+$", re.I)
                print(rx)
                if rx.match(dir):
                    dirPaths.append(dir)#name of the currently working directory path of the patient
                    dirNames.append(os.path.basename(dir))#name of the study
                    #keep the name of the patient in ascending order in a file to keep track of the patient working on
                
    
    from pathlib import Path
    print(directoryPath)
    filepath = directoryPath+"/patients_id.csv"
    print(filepath)
    #filepath.parent.mkdir(parents=True, exist_ok=True)
              
    df = pd.DataFrame(list(zip(dirPaths, dirNames)), columns =['DirPaths', 'DirNames'])
   
    df.to_csv(filepath, index=True)
    #save patient id in the file at the end of the for loop to keep track of the patient id and start the loop from onward
    
    
    for patientID in range(patientID,len(df)):
    
        print(df.iloc[patientID].DirNames)
        print(df.index.get_loc(patientID))
        patID = df.index.get_loc(patientID)
        startPatientDirName = df.iloc[patientID].DirNames
        startPatientDirPath = df.iloc[patientID].DirPaths
        self.log(startPatientDirName)
        self.log(startPatientDirPath)
        
    
        
        
        #checking the files for each patient if all the original files to run the preprocessor exist or not flair, t1, t2 and t1c
        import re
        path = startPatientDirPath
        patterns = [".*fla.*.nii.gz", ".*t1.nii.gz", ".*t1c.nii.gz", ".*t2.nii.gz"]
        files = []
        
        try:
            for pattern in patterns:
                for file in os.listdir(path):
                    if re.search(pattern, file, flags = re.IGNORECASE):
                        print(os.path.join(path,file))
                        files.append(os.path.join(path,file))
            print(len(patterns), len(files))      
        
            if len(files) != len(patterns):
                self.log("Not all required files found in directory.........."+startPatientDirName)
                with open(directoryPath+"/failed_patient.txt", "a") as f:
                    f.write(str(patID))
                    f.write("\n")
                raise Exception("Not all required files found in directory")
        except FileNotFoundError as e:
            self.log(str(e))
            return


        self.log(f"All required patient files found for patient with id = {patID} and patient directory = {startPatientDirName}\n")
        self.log(f"Starting preprocessor of the brats toolkit for patient id {patID}\n")
        command_line = [r"/home/useradmin/anaconda3/bin/python3.8", "/media/useradmin/Disk2/Python_scripts_saima/bratsPreprocessor.py",startPatientDirPath, startPatientDirName, files[0], files[1], files[2], files[3]]
        import subprocess
        from subprocess import check_output
        import sys,os
        
        try:
          #command_results = subprocess.run(command_line, env=slicer.util.startupEnvironment())
          print("inside pre-processor")
          proc = slicer.util.launchConsoleProcess(command_line, useStartupEnvironment=True)
          self.logProcessOutput(proc)
          #command_result = check_output(command_line, env=slicer.util.startupEnvironment(), shell = True, stderr=subprocess.STDOUT)
          #You can write both stderr and stdout to two separate files: 
          #self.logProcessOutput(check_output(command_line, env=slicer.util.startupEnvironment(), shell = True, stderr=subprocess.STDOUT))                 
          #print(command_result)
        except subprocess.CalledProcessError as e:
            self.log(str(e))
            with open(directoryPath+"/failed_patient.txt", "a") as f:
                  f.write(str(patID))
                  f.write("\n")
                
            return
             
 
# =============================================================================
        # checking of the availability of the files for a current patient then enter to do segmentation
        # code for the checking of the files for the current patient
        # search the preprocessed brat files using the regular expression in a directory if all files exist proceed with segmentation 
        self.log(f"Starting checking the preprocessed brats files (fla, t1, t2, t1c) in path {startPatientDirPath}/output/hdbet_brats-space/\n")
        import re
        path = startPatientDirPath+"/output/hdbet_brats-space/"
        
        patterns = [".*fla.nii.gz", ".*t1.nii.gz", ".*t2.nii.gz", ".*t1c.nii.gz"]
        
        files = []
        try:
            for file in os.listdir(path):
                print(file)
                for pattern in patterns:
                    if re.search(pattern, file, flags=re.IGNORECASE):
                        print(os.path.join(path,file))
                        files.append(os.path.join(path,file))
            print(len(patterns), len(files))           
            if len(files) != len(patterns):
                self.log("Not all required files found in directory..........")
                with open(directoryPath+"/failed_patient.txt", "a") as f:
                    f.write(str(patID))
                    f.write("\n")
                raise Exception("Not all required files found in directory")
        except FileNotFoundError as e:
            self.log(str(e))
            return
        
        self.log(f"All required patient files found for starting segmentator for patient with id = {patID} and patient directory = {startPatientDirName}\n")
        self.log(f"Starting segmentator of the brats toolkit for patient id {patID}")
        command_line = [r"/home/useradmin/anaconda3/bin/python3.8", "/media/useradmin/Disk2/Python_scripts_saima/bratsSegmentor.py", startPatientDirPath, startPatientDirName, str(nnModels)]
        try:
            print("inside segmentator")
            proc = slicer.util.launchConsoleProcess(command_line, useStartupEnvironment=True)
            self.logProcessOutput(proc)
            
        except subprocess.CalledProcessError as e:
            print("exception")
            self.log(str(e))
            with open(directoryPath+"/failed_patient.txt", "a") as f:
                f.write(str(patID))
                f.write("\n")
            return
            
        self.log(f"Segmentator of the brats toolkit finished successfully for patient id {patID}\n")    


        #checking of the files existence for fusion
        self.log("Starting checking the segmentation files for fusion in path "+startPatientDirPath+"/outputSegmentator/ \n")
        cids = nnModels#['isen-20','hnfnetv1-20','sanet0-20','scan-20']
        segFiles = [startPatientDirPath+"/outputSegmentator/"+ cid+".nii.gz" for cid in cids]
        
        try:
            for file in segFiles:
                if not os.path.exists(file):
                    raise FileNotFoundError(f"File {file} not found!")
            print("All files for fusion exist")
        except FileNotFoundError as e:
              print(e, file=sys.stderr)
              self.log(str(e))
              with open(directoryPath+"/failed_patient.txt", "a") as f:
                f.write(str(patID))
                f.write("\n")
              return

            
        self.log(f"All required patient files found to proceed with fusionator for patient with id = {patID} and patient directory = {startPatientDirName}\n")    
        self.log("Starting fusionator of the brats toolkit.............")    
        command_line = [r"/home/useradmin/anaconda3/bin/python3.8", "/media/useradmin/Disk2/Python_scripts_saima/bratsFusionator.py",  startPatientDirPath, startPatientDirName, str(nnModels)]
        try:
            print("inside fusionator", startPatientDirPath, startPatientDirName)
            proc = slicer.util.launchConsoleProcess(command_line, useStartupEnvironment=True)
            self.logProcessOutput(proc)
            self.log("Fusionator of the brats toolkit finished successfully.................") 
            
        except subprocess.CalledProcessError as e:
            print("exception")
            with open(directoryPath+"/failed_patient.txt", "a") as f:
                f.write(str(patID))
                f.write("\n")
        
        #after performing the fusionator do the inverse transform and apply it to the segmentation and save the segmentation in a seperate output folder   
        
        
        stopTime = time.time()
        self.log('Processing completed in {0:.2f} seconds\n'.format(stopTime-startTime))

#
# BrainTumorSegmentationTest
#

class BrainTumorSegmentationTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_BrainTumorSegmentation1()

  def test_BrainTumorSegmentation1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    registerSampleData()
    inputVolume = SampleData.downloadSample('BrainTumorSegmentation1')
    self.delayDisplay('Loaded test data set')

    inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    self.assertEqual(inputScalarRange[0], 0)
    self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    logic = BrainTumorSegmentationLogic()

    # Test algorithm with non-inverted threshold
    logic.process(inputVolume, outputVolume, threshold, True)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    logic.process(inputVolume, outputVolume, threshold, False)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], inputScalarRange[1])

    self.delayDisplay('Test passed')
