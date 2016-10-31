"""
Author:      www.tropofy.com

Copyright 2015 Tropofy Pty Ltd, all rights reserved.

This source file is part of Tropofy and governed by the Tropofy terms of service
available at: http://www.tropofy.com/terms_of_service.html

This source file is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
"""

from collections import OrderedDict
from StringIO import StringIO

import requests
from PIL import Image
from tropofy.app import AppWithDataSets, Parameter, ParameterGroup, Step, StepGroup
from tropofy.widgets import Chart, ExecuteFunction, ParameterForm
from tropofy.widgets.text_widget import TextWidget


# The total number of colours in the colour pallete for an RGB image
MAX_NUM = int('FFFFFF', 16)
# The number of partitions that the colour pallete will be split into
# 65 evenly divides 0xFFFFFF so it was chosen for that reason
PARTITIONS = 65


class UrlParameterGroup(ParameterGroup):
    URL = Parameter(name='url', label='Image Url', default='http://j754.xyz/other/image.jpg', allowed_type=str)


class ColorHistogram(Chart):
    def get_chart_type(self, app_session):
        return Chart.BARCHART

    def get_table_data(self, app_session):
        return app_session.data_set.get_var('data')

    def get_table_schema(self, app_session):
        return {
            "color": ("string", "Color"),
            "pct": ("number", "pct")
        }

    def get_column_ordering(self, app_session):
        return ["color", "pct"]

    def get_order_by_column(self, app_session):
        return "color"


class CreateHistogram(ExecuteFunction):
    def get_button_text(self, app_session):
        return "Create Histogram"

    def execute_function(self, app_session):
        link = app_session.data_set.get_param(UrlParameterGroup.URL.name)
        response = requests.get(link)
        img = Image.open(StringIO(response.content))

        # Get RGB values for the image
        rgb_img = img.convert('RGBA')
        width, height = rgb_img.size
        total = width * height
        
        app_session.task_manager.send_progress_message("Image Width: " + str(width) + "px")
        app_session.task_manager.send_progress_message("Image Height: " + str(height) + "px")
        app_session.task_manager.send_progress_message("Total Image Size: " + str(total) + "px")
        # Create buckets for each color to go into
        keys = []
        for i in xrange(PARTITIONS + 1):
            keys.append((MAX_NUM / PARTITIONS) * i)
        result_dict = OrderedDict(sorted({key: 0 for key in keys}.items()))

        # For each pixel get the base 16 representation of the color and place it into the closest bucket
        for x in xrange(width):
            for y in xrange(height):
                r, b, g, a = rgb_img.getpixel((x, y))
                hex_code = int(str(r) + str(g) + str(b), 16)
                result_dict[min(result_dict, key=lambda p:abs(p - hex_code))] += 1

        # Normalise the values in the map
        app_session.data_set.set_var('data', [{"color": '#' + hex(k)[2:].upper(), "pct": float(v)/total} for k, v in result_dict.iteritems()])
        app_session.task_manager.send_progress_message("Histogram successfully created. Go to next step to view it.")



class HistogramApp(AppWithDataSets):
    def get_name(self):
        return "Color Histogram App"

    def get_gui(self):
        return [
            StepGroup(name='Input', steps=[
                Step(name='URL', widgets=[
                    ParameterForm()
                ]),
                Step(name='Generate', widgets=[
                    TextWidget(text='Generate the histogram, this may take a little while'),
                    CreateHistogram()
                ])
            ]),
            StepGroup(name='Output', steps=[
                Step(name='Histogram', widgets=[
                    ColorHistogram()
                ])
            ])
        ]

    def get_parameters(self):
        return UrlParameterGroup.get_params()
    
    def get_home_page_content(self):
        return {
            'content_app_name_header': '<div style="align: center;">Color Histogram</div>',
            'content_single_column_app_description': 
                """
                <p>An app that can generate a colour histogram from an image hosted on the internet</p>
                """
        }
