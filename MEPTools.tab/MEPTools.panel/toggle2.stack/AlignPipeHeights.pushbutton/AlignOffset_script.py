from Autodesk.Revit.DB import FilteredElementCollector, Transaction
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit import Exceptions
from Autodesk.Revit import Exceptions

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

__doc__ = """Align pipes offset.
Select first object to be moved.
Select second object which is on desired offset"""
__title__ = "Align pipe heights"


tx = Transaction(doc, 'AlignOffset')
tx.Start()
try:
    var1 = uidoc.Selection.PickObject(ObjectType.Element, "Pick first object")
    var2 = uidoc.Selection.PickObject(ObjectType.Element, "Pick second object")
    element1 = doc.GetElement(var1)
    element2 = doc.GetElement(var2)


    element2.ReferenceLevel = element1.ReferenceLevel
    element2.LevelOffset = element1.LevelOffset

except:
    pass

tx.Commit()

