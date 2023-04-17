# -*- coding: utf-8 -*-

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


for view in selection:
	uidoc.ActiveView = view