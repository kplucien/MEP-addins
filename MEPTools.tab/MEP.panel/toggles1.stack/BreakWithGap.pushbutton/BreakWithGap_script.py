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

__doc__ = """Split pipe/duct with gap"""
__title__ = "SplitWithGap"

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
id = []
transgroup = TransactionGroup(doc, "BreakElement: ")
transgroup.Start()
elements= []
n=0

pt = []
try:    
    while n<2:


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
        pt.append(sp1)
        elements.append(doc.GetElement(a))
        elements.append(element)

        n += 1
except Exceptions.OperationCanceledException:
    pass 


transgroup.Assimilate()
el_bb = []
el_outline = []

for el in elements:
     
    el_bb.append(el.get_BoundingBox(doc.ActiveView))
    el_bb_min = el.get_BoundingBox(doc.ActiveView).Min
    el_bb_max = el.get_BoundingBox(doc.ActiveView).Max
    el_outline.append(Outline(el_bb_min, el_bb_max))

for x in range(len(el_outline)):   
    if el_outline[x].Contains(pt[0], 1) and el_outline[x].Contains(pt[1], 1):
        rollingpipe = elements[x]
    else:
        pass

to_delete = []
to_delete.append(rollingpipe)

tx = Transaction(doc, 'RemoveRollingPipe')
tx.Start()
el_ids = []
for e in to_delete:
	el_ids.append(e.Id)
ids = cList[ElementId](el_ids)


doc.Delete(ids)

tx.Commit()
