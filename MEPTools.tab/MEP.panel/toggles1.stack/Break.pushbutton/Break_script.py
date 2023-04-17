# coding: utf8
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from math import pi

from Autodesk.Revit.DB import Line, InsulationLiningBase
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit import Exceptions
from Autodesk.Revit.DB.Mechanical import *
from Autodesk.Revit.DB.Plumbing import *
from System.Collections.Generic import List as cList

 
#from pyrevitmep.meputils import get_connector_manager, get_connector_closest_to

__doc__ = """BreakCurve"""
__title__ = "BreakCurve"

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
id = []


# Prompt user to select elements and points to connect
transgroup = TransactionGroup(doc, "BreakElement: ")
transgroup.Start()

try:    
    while (True):


        split1 = uidoc.Selection.PickObject(ObjectType.Element, "Pick first point")
        sp1 = split1.GlobalPoint
        element = doc.GetElement(split1)
        tx = Transaction(doc, 'BreakCurve')
        tx.Start()
        try: 
            a = PlumbingUtils.BreakCurve(doc, element.Id, sp1)
        except:
            a = MechanicalUtils.BreakCurve(doc, element.Id, sp1)

        tx.Commit()

except Exceptions.OperationCanceledException:
    pass 

transgroup.Assimilate()