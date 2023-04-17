from Autodesk.Revit.DB.Mechanical import Duct, DuctType
from Autodesk.Revit.DB.Plumbing import Pipe, PipeType
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, TransactionGroup
from Autodesk.Revit.DB import Line, InsulationLiningBase
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit import Exceptions

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


def GetPipeType(s0):
	pipeType = []
	try: 
		usedConn = s0.MEPModel.ConnectorManager.Connectors
	except:
		usedConn = s0.ConnectorManager.Connectors

	pipeType = FilteredElementCollector(doc).OfClass(PipeType).WhereElementIsElementType().FirstElement()
	for x in usedConn:
		for y in x.AllRefs:
			try:
				pipeType = y.Owner.PipeType 
			except:
				pass
	pipeTypeId = pipeType.Id
	return pipeTypeId


def GetDuctType(s0):
	ductType = []
	try: 
		usedConn = s0.MEPModel.ConnectorManager.Connectors
	except:
		usedConn = s0.ConnectorManager.Connectors

	ductType = FilteredElementCollector(doc).OfClass(DuctType).WhereElementIsElementType().ToElements()
	rectDuct = filter(lambda x: x.FamilyName.Contains("Rec"), ductType)
	roundDuct = filter(lambda x: x.FamilyName.Contains("Round"), ductType)

	for x in usedConn:
		if x.Shape.ToString() =="Rectangular":
			ductType = rectDuct[0]
			for y in x.AllRefs:
				try:
					ductType = y.Owner.DuctType 
				except:
					pass
		else:
			ductType = roundDuct[0]
			for y in x.AllRefs:
				try:
					ductType = y.Owner.DuctType 
				except:
					pass
		ductTypeId = ductType.Id
	return ductTypeId

transgroup = TransactionGroup(doc, "Bloom: ")
transgroup.Start()

try:    
    while (True):

        split1 = uidoc.Selection.PickObject(ObjectType.Element, "Pick first point")
        sp1 = split1.GlobalPoint
        s0 = doc.GetElement(split1)
        ductTypeId = GetDuctType(s0)
        pipeTypeId = GetPipeType(s0)

        try:
            levelId = s0.ReferenceLevel.Id
        except:
            levelId = s0.LevelId
            
        tx = Transaction(doc, "Bloom")
        tx.Start()

        try: 
            unused = s0.MEPModel.ConnectorManager.UnusedConnectors
        except:
            unused = s0.ConnectorManager.UnusedConnectors
            
        for i in unused:
            startConnector = i
            endpoint = i.Origin + i.CoordinateSystem.BasisZ
            try:	
                Pipe.Create(doc, pipeTypeId, levelId, startConnector, endpoint)
            except:
                Duct.Create(doc, ductTypeId, levelId, startConnector, endpoint)
        tx.Commit()
except Exceptions.OperationCanceledException:
    pass 

transgroup.Assimilate()