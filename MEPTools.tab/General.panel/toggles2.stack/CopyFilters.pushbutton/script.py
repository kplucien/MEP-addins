# dependencies
import clr

from operator import truediv
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.Creation import *
from Autodesk.Revit.DB.Structure import *
from pyrevit import forms

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication

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

clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')

# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('ui.xaml')

name ="Test"
# import WPF creator and base Window
import wpf
from System import Windows

listview_a = []
listview1 = []
listview_b = []
listview2 = []
all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
for i in all_views:
    if i.IsTemplate:
        listview_a.append(i)
        listview_b.append(i)
listview1 = sorted(listview_a, key = lambda x: x.Name)
listview2 = sorted(listview_b, key = lambda x: x.Name)
"""class ViewModel(forms.Reactive):
    def __init__(self): 
        self.temp = listview

class MyWindow(forms.WPFWindow, forms.Reactive):
    def __init__(self):
        self.vm = ViewModel()
    
    def setup(self):
        self.listview.ItemsSource = self.vm.temp

    def fun(self, sender, args):
        #print self.listview.SelectedItems.Count.ToString()
        selected_templates = self.listview.SelectedItems

        return selected_templates

ui = script.load_ui(MyWindow(), 'ui.xaml')
ui.show_dialog()   
# let's show the window (modal)

"""

class ListToUi(forms.Reactive):
    def __init__(self):
        self.lista_to = listview1
        self.lista_from = listview2

class MyWindow(forms.WPFWindow,forms.Reactive):
    def __init__(self):
        #wpf.LoadComponent(self, xamlfile)
        self.l = ListToUi()


    def setup(self):
        self.listview1.ItemsSource = self.l.lista_to
        self.listview2.ItemsSource = self.l.lista_from

    @property
    def copy_to_view(self):
        return self.listview1.SelectedItems

    
    @property
    def copy_from_view(self):
        return self.listview2.SelectionBoxItem

    def fun(self, sender, args):
        all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
        template_all = []
        template_keys = []
        template_values = []
        ##################Copy from the template:
        for i in all_views:
            if i.IsTemplate:
                template_keys.append(i.Name)
                template_values.append(i)
        temp_dict = {template_keys[i] : template_values[i] for i in range(len(listview1))}
        template_from = self.copy_from_view
        filters = template_from.GetFilters()

        for j in filters:
            over = template_from.GetFilterOverrides(j)
            
        for k in all_views:
            if k.IsTemplate and k.Name == "cwd-bw":
                new_view = k


        selected_viewtemplates = self.copy_to_view
        tx = Transaction(doc, 'CopyFilters')      
        tx.Start()
        for templates_to_be_changed in selected_viewtemplates:

            for filter in filters:
                try:
                    templates_to_be_changed.AddFilter(filter)
                    over=template_from.GetFilterOverrides(filter)
                    templates_to_be_changed.SetFilterOverrides(filter, over)
                    
                except:
                    pass

        tx.Commit()       

        print "copied from {}".format(self.copy_from_view.Name)
        for i in self.copy_to_view:
            print "copied to {}".format(i.Name)

ui = script.load_ui(MyWindow(), 'ui.xaml')
ui.show_dialog()   


