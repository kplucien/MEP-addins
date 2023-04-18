# coding: utf8
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from System.Collections.Generic import List as cList
from pyrevit import forms
from Autodesk.Revit.UI import TaskDialog
"""from pyrevit import script
output = script.get_output()"""

__doc__ = """Select a space by space number"""
__title__ = "SpaceFinder"

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


spaces = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

#space_number = raw_input("Type a space number:")
space_number= forms.ask_for_string(default="R.+xx.xxx", prompt="Space Number", title="SpaceFinder",)


el_ids = []

for i in spaces:
	if i.Number == space_number:
		#print i.Id

		el_ids.append(i.Id)
		ids = cList[ElementId](el_ids)
		uidoc.Selection.SetElementIds(ids)
if len(el_ids) == 0:
    TaskDialog.Show("Error", "Space Number {} not found".format(space_number))
"""output.close()"""






"""from rpw.ui.forms import TextInput
value = TextInput('Title', default="3")
print(value)"""