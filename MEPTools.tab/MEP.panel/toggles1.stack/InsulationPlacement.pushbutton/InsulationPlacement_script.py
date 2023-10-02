
from Autodesk.Revit.DB.Mechanical import DuctInsulation, DuctInsulationType
from Autodesk.Revit.DB.Plumbing import PipeInsulation, PipeInsulationType
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, Document, BuiltInCategory, ElementId
from System.Collections.Generic import List as cList


__title__ = "InsulationPlacement"
__author__ = 'Kamil Pluciennik'


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
to_delete = []

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


duct_segment = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_DuctCurves).WhereElementIsNotElementType().ToElements()
duct_fittings = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_DuctFitting).WhereElementIsNotElementType().ToElements()
duct_all_insulations = FilteredElementCollector(doc).OfClass(DuctInsulationType).WhereElementIsElementType().ToElements()

pipe_segment = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_PipeCurves).WhereElementIsNotElementType().ToElements()
pipe_fittings = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_PipeFitting).WhereElementIsNotElementType().ToElements()
pipe_all_insulations = FilteredElementCollector(doc).OfClass(PipeInsulationType).WhereElementIsElementType().ToElements()


duct_all = list(duct_segment) + list(duct_fittings)
duct_insulation_missing = []
duct_insulated = []

for x in duct_all:
	if x.LookupParameter("Insulation Type").AsString() == None and x.LookupParameter("System Type").AsValueString().Contains("Supply"):
		duct_insulation_missing.append(x)
	elif x.LookupParameter("Insulation Type").AsString() != None and x.LookupParameter("System Type").AsValueString().Contains("Supply"):
		duct_insulated.append(x)

################################

pipe_all = list(pipe_segment) + list(pipe_fittings)
pipe_insulation_missing = []
pipe_insulated = []
for x in pipe_all:
	if x.LookupParameter("Insulation Type").AsString() == None:
		pipe_insulation_missing.append(x)
	elif x.LookupParameter("Insulation Type").AsString() != None:
		pipe_insulated.append(x)


tx = Transaction(doc, 'InsulationPlacement')
tx.Start()

#get first item from list or get by name
#duct_ins = duct_insulated[0].LookupParameter("Insulation Type").AsString()
duct_ins = "NLRS_57_DUI_UN_uitwendige isolatie_generiek"
thickness_duct = duct_insulated[0].LookupParameter("Insulation Thickness").AsDouble()

pipe_ins = pipe_insulated[0].LookupParameter("Insulation Type").AsString()
thickness_pipe = pipe_insulated[0].LookupParameter("Insulation Thickness").AsDouble()

try:
    duct_get_insulation = filter(lambda x: duct_ins in x.LookupParameter("Type Name").AsString(), duct_all_insulations)
    duct_insulation = duct_get_insulation[0]

    for el in duct_insulation_missing:
        DuctInsulation.Create(doc, el.Id, duct_insulation.Id, thickness_duct)
        #print("Duct Id {} insualtion was filled".format(el.Id))


    pipe_get_insulation = filter(lambda x: pipe_ins in x.LookupParameter("Type Name").AsString(), pipe_all_insulations)
    pipe_insulation = pipe_get_insulation[0]

    for el in pipe_insulation_missing:
        PipeInsulation.Create(doc, el.Id, pipe_insulation.Id, thickness_pipe)
        #print("Pipe Id {} insualtion was filled".format(el.Id))


except:
      pass

all = list(duct_insulation_missing) + list(pipe_insulation_missing)

##add element to selection in UI

tx.Commit()

el_ids = []

for i in all:
    el_ids.append(i.Id)    
    ids = cList[ElementId](el_ids)
    uidoc.Selection.SetElementIds(ids)
