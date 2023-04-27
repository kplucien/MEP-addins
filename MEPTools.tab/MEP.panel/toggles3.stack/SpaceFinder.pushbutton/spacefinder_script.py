import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from System.Collections.Generic import List as cList
from pyrevit import forms
from Autodesk.Revit.UI import TaskDialog

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

####imports for UI
import sys
from pyrevit import forms
from pyrevit import script
#imports for UI
spaces = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()

class AboutWindow(forms.WPFWindow):

    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

    def funkcja(self, sender, args):
        space_number = self.space_nr.Text
        el_ids = []

        for i in spaces:
            if i.Number == space_number:
                #print i.Id

                el_ids.append(i.Id)
                ids = cList[ElementId](el_ids)
                uidoc.Selection.SetElementIds(ids)
        if len(el_ids) == 0:
            TaskDialog.Show("Error", "Space Number {} not found".format(space_number))
        self.Close()

space_number = AboutWindow("ui.xaml").ShowDialog()


