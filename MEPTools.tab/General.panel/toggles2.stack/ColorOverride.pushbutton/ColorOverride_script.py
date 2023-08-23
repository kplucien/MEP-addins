__title__ = "ColorOverride"
__author__ = 'Kamil Pluciennik'
__context__ = ['Selection']

import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from System.Collections.Generic import List as cList
from Autodesk.Revit.DB import Transaction, Document

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

view = doc.ActiveView
my = []
color = Color(255,0,0)
line_weight = 9
graphic = OverrideGraphicSettings()
graphic.SetProjectionLineColor(color)
graphic.SetProjectionLineWeight(line_weight)


tx = Transaction(doc, 'default')
tx.Start()

for element in selection:
	view.SetElementOverrides(element.Id, graphic)
		


tx.Commit()
