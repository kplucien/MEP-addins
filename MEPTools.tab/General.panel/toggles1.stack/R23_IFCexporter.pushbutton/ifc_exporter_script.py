#Define Document
__title__ = "Export IFC from selection"
__author__ = 'Kamil Pluciennik'
__context__ = 'Selection'

import random
import os
import datetime
import clr
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *

clr.AddReferenceToFileAndPath('C:\Program Files\Autodesk\Revit 2023\AddIns\IFCExporterUI\Autodesk.IFC.Export.UI.dll')
import BIM.IFC.Export.UI as ifcX

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)
selection = get_selected_elements(doc)
# convenience variable for first element in selection
if len(selection):
    s0 = selection[0]

#Create an Instance of the IFC Export Class

desiredConfigName = "IFC 2x3 Coordination View 2.0" #the name of the export setting we want to use
ifcXConfigMap = ifcX.IFCExportConfigurationsMap() #creates a new (empty) ifc exporter configuraitons map object
ifcXConfigMap.AddSavedConfigurations() #adds the previously saved configurations to the configuratons map, including the default <In-Ssession Setup> configuration
ifcXConfigMap.AddBuiltInConfigurations() #adds the builtin configurations which ship with the add-in to the configurations map
#gets the saved configurations from the mapping
configurations = ifcXConfigMap.Values #gets the configurations as a "value collection" object, because of course this wouldn't be easy
enum = configurations.GetEnumerator() #gets the enumerator for the configuration value collection
selectedConfiguration = [] #sets an empty list for the selected configuration variable
#gets the selected configuration or the names of all available configurations
for i in range(configurations.Count): #for every item in the range of configurations perform the offset actions below
    enum.MoveNext() # move to the next item in the enumerations list; have to do this before we get the first item as the pointer will otherwise point at nothing
    now = enum.Current #gets the current enumeration
    if now.Name == desiredConfigName: #if the name matched the value given perform the offset lines below
        selectedConfiguration.append(now) #set the selected configuraiton to the current item

mycon = selectedConfiguration[0]
mycon.IFCVersion.IFC2x3CV2
mycon.ExchangeRequirement
mycon.ExchangeRequirement.NotDefined
mycon.IFCFileType.Ifc
mycon.SpaceBoundaries = 2
mycon.SplitWallsAndColumns = False
mycon.IncludeSteelElements = True
mycon.ProjectAddress.UpdateProjectInformation = False
mycon.ProjectAddress.AssignAddressToSite = False
mycon.ProjectAddress.AssignAddressToBuilding = False
mycon.Export2DElements = False
mycon.ExportLinkedFiles = False
mycon.VisibleElementsOfCurrentView = True
mycon.ExportRoomsInView = False
mycon.ExportInternalRevitPropertySets = True
mycon.ExportIFCCommonPropertySets = True
mycon.ExportBaseQuantities = True
#mycon.ExportMaterialPsets = False //element not found
mycon.ExportSchedulesAsPsets = True
mycon.ExportSpecificSchedules = True
mycon.ExportUserDefinedPsets = True

#mycon.ExportUserDefinedPsetsFileName = "C:\\Users\\KPlucien\\DC\\ACCDocs\\INVAP\\PALLAS - Production\\Project Files\\01-wip\\s0-hvac\\08. framework\\00. settings\\IFC-settings\\PLLS_ParameterSets.txt"
mycon.ExportUserDefinedPsetsFileName = "C:\\Users\\KPlucien\\DC\\ACCDocs\\INVAP\\PALLAS - Production\\Project Files\\01-wip\\s0-framework\\02-revit\\00-settings\\02-ifc_settings\\PLLS_ParameterSets.txt"

mycon.ExportUserDefinedParameterMapping = False
mycon.ExportUserDefinedParameterMappingFileName = ""
mycon.ClassificationSettings.ClassificationName = None
mycon.ClassificationSettings.ClassificationEdition = None
mycon.ClassificationSettings.ClassificationSource = None
#mycon.ClassificationSettings.ClassificationEditionDate //?? how to define date?
mycon.ClassificationSettings.ClassificationLocation = None
mycon.ClassificationSettings.ClassificationFieldName = None
mycon.TessellationLevelOfDetail = 0.5
mycon.ExportPartsAsBuildingElements = True
mycon.ExportSolidModelRep = False
mycon.UseActiveViewGeometry = True
mycon.UseFamilyAndTypeNameForReference = False
mycon.Use2DRoomBoundaryForVolume = False
mycon.IncludeSiteElevation = False
mycon.StoreIFCGUID = True
mycon.ExportBoundingBox = False
mycon.UseOnlyTriangulation = False

mycon.UseTypeNameOnlyForIfcType = False
mycon.UseVisibleRevitNameAsEntityName = False
mycon.SelectedSite = "IFC Export"
mycon.SitePlacement.Site
mycon.GeoRefCRSName = "Netherlands-RD"
mycon.GeoRefCRSDesc = "Netherlands, Rijksdriehoeksmeting datum, Oblique Stereographic"
mycon.GeoRefEPSGCode = ""
mycon.GeoRefGeodeticDatum = "RD"
mycon.GeoRefMapUnit = "METRE"
mycon.ExcludeFilter = ""
mycon.COBieCompanyInfo = ""
mycon.COBieProjectInfo = ""

options = IFCExportOptions()

default_path = "D:\\_projects exports IFC"

current_time = datetime.datetime.now()
subfolder = current_time.strftime("%y%m%d") + "_" + current_time.strftime("%H%M")
file_path = default_path+"\\"+doc.Title+"\\"+subfolder+"\\"
if os.path.exists(file_path):
    pass
else:
    os.mkdir(file_path)



if os.path.exists(file_path):
    pass
else:
    os.mkdir(file_path)


tx = Transaction(doc, 'default')
tx.Start()

for view in selection:
	mycon.UpdateOptions(options, view.Id)
	name = view.Name+".ifc"
	doc.Export(file_path, name, options)
        

for x in doc.ProjectLocations:
    #if x.Name == "PALLAS Health Centre - B":
    if x.Name.Contains("PALLAS Site"):
        doc.ActiveProjectLocation = x
             

tx.Commit()


path = os.path.realpath(file_path)
os.startfile(path)