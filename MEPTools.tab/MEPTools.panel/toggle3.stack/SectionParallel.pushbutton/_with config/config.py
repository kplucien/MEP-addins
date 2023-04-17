# coding: utf8

import clr
import System

from Autodesk.Revit.DB import *
try: # Revit ⩽ 2021
    from Autodesk.Revit.DB import  DisplayUnitType, UnitType, UnitSymbolType
except ImportError:  # Revit ⩾ 2022
    from Autodesk.Revit.DB import SpecTypeId, UnitTypeId

import rpw
from pyrevit import forms, script, HOST_APP

doc = rpw.revit.doc  # type: Document

if HOST_APP.is_older_than(2022):
    length_unit = UnitType.UT_Length
else:
    length_unit = SpecTypeId.Length

unit_format_options = doc.GetUnits().GetFormatOptions(length_unit)

if HOST_APP.is_older_than(2022):
    symbol_type = unit_format_options.UnitSymbol
    if symbol_type == UnitSymbolType.UST_NONE:
        try:
            symbol_type = unit_format_options.GetValidUnitSymbols().Item[1]
        except System.ArgumentOutOfRangeException:
            symbol_type = FormatOptions.GetValidUnitSymbols(DisplayUnitType.DUT_DECIMAL_FEET).Item[1]
    symbol = LabelUtils.GetLabelFor(symbol_type)
else:
    symbol_type = unit_format_options.GetSymbolTypeId()
    if symbol_type.Empty():
        try:
            symbol_type = unit_format_options.GetValidSymbols()[1]
        except System.ArgumentOutOfRangeException:
            symbol_type = FormatOptions.GetValidSymbols(UnitTypeId.Feet).Item[1]
    symbol = LabelUtils.GetLabelForSymbol(symbol_type)


UNITS = doc.GetUnits()

listview_a = []
templates = []

all_views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
for i in all_views:
    if i.IsTemplate:
        listview_a.append(i)
templates = sorted(listview_a, key = lambda x: x.Name)

class ListToUi(forms.Reactive):
    def __init__(self):
        self.lista = templates

class options(forms.WPFWindow, forms.Reactive):
    def __init__(self):
        #forms.WPFWindow.__init__(self, "options.xaml")
        self.vm = ListToUi()

    def setup(self):
        self.pole.ItemsSource = self.vm.lista
        # get parameters from config file or use default values
        self._config = script.get_config()
    

    @property
    def selected_temp(self):
        return self.pole.SelectionBoxItem

    def sel(self, sender, e):
            self._config.use_template = self.selected_temp.Name
            script.save_config()
            self.Close()



"""
class options(forms.WPFWindow):
    def __init__(self):
        forms.WPFWindow.__init__(self, "options.xaml")

        # get parameters from config file or use default values
        self._config = script.get_config()

        self.tbox_prefix.Text = self._config.get_option('prefix', 'Mur')


    def import_config_length(self, name):
        length = float(self._config.get_option(name, '1'))
        if HOST_APP.is_older_than(2022):
            return UnitFormatUtils.Format(UNITS, length_unit, length, True, True)
        else:
            return UnitFormatUtils.Format(UNITS, length_unit, length, True)

    def export_config_length(self, name, text):
        ref = clr.Reference[float]()
        if UnitFormatUtils.TryParse(UNITS, length_unit, text, ref):
            setattr(self._config, name, str(ref.Value))
        else:
            forms.alert("Invalid value for {}".format(name))

    def save_options(self, sender, e):
        self._config.prefix = self.tbox_prefix.Text
        self.export_config_length("depth_offset", self.tbox_depth_offset.Text)
        self.export_config_length("height_offset", self.tbox_height_offset.Text)
        self.export_config_length("width_offset", self.tbox_width_offset.Text)
        script.save_config()
        self.Close()

    def reset_options(self, sender, e):
        script.reset_config()
        self.Close()
        reseted_gui = CreateSectionOptions().show_dialog()
"""

ui = script.load_ui(options(), 'options.xaml')
ui.show_dialog()