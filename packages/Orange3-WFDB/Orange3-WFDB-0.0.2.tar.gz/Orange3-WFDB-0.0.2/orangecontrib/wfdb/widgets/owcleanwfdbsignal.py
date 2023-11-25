#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:51:26 2023

@author: chris
"""
from Orange.data import Table
from Orange.widgets import widget, gui
from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from orangecontrib.timeseries import Timeseries
import numpy as np

class OWCleanWFDBSignal(OWWidget):
    name = 'Clean WFDB Signal'
    description = 'Fills in 0s with window-statistical values'
    icon = 'icons/clean_wfdb.svg'
    priority = 20
    
    class Inputs:
        time_series = Input("Time series", Table)
        
    class Outputs:
        time_series = Output("Time series", Timeseries)
        
    class Warning(OWWidget.Warning):
        no_aggregations = widget.Msg("No (applicable) aggregations are selected")
        inapplicable_aggregations = \
            widget.Msg("Some aggregations are applicable "
                       "only to sliding window ({})")
        window_to_large = widget.Msg("Window width is too large")
        block_to_large = widget.Msg("Block width is too large")

    class Error(OWWidget.Error):
        migrated_aggregate = widget.Msg(
            "Aggregate was replaced with Moving Transform; "
            "manually re-set the widget")

    want_main_area = False
    
    def __init__(self):
        self.data = None
        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something.")
        self.infob = gui.widgetLabel(box, '')
        
    @Inputs.time_series
    def set_data(self, dataset):
        if dataset is not None:
            #self.data = dataset
            self.infoa.setText("%d instances in input data set" % len(dataset))
            fhr = dataset.get_column('FHR')
            smooth_fhr = OWCleanWFDBSignal.smooth_zeros(fhr)
            xdf, ydf, mdf = list(dataset.to_pandas_dfs())
            xdf["FHR Smooth"] = smooth_fhr.reshape(len(smooth_fhr), 1)
            output = Table.from_pandas_dfs(xdf, ydf, mdf)
            ts_output = Timeseries(output)
            self.Outputs.time_series.send(ts_output)
        else:
            self.infoa.setText(
                "No data on input yet, waiting to get something.")
            self.infob.setText('')
            self.Outputs.time_series.send(None)

    @staticmethod
    def smooth_zeros(arr: np.array) -> np.array:
        out = arr.copy()
        window = []
        zero_len = 0
        avg = 0
        stdev = 0
        for i in range(len(arr)):
            if avg > 0 and arr[i] == 0:
                zero_len += 1
            elif avg > 0 and arr[i] < avg - (8*stdev):
                zero_len += 1
            else:
                if zero_len > 0:
                    fillin = np.random.normal(avg, stdev, zero_len)
                    out[i-zero_len:i] = fillin
                    zero_len = 0
                window.append(arr[i])
                if len(window) > 40:
                    window.pop(0)
                avg = np.average(window)
                stdev = np.std(window)
        return out

if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview

    WidgetPreview(OWCleanWFDBSignal).run(
        Table("/home/chris/code/orange/wfdb_test.tab"))
