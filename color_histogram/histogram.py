"""
Author:      www.tropofy.com

Copyright 2015 Tropofy Pty Ltd, all rights reserved.

This source file is part of Tropofy and governed by the Tropofy terms of service
available at: http://www.tropofy.com/terms_of_service.html

This source file is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
"""

from tropofy.app import AppWithDataSets, Step, StepGroup, ParameterGroup, Parameter
from tropofy.widgets import ParameterForm, Chart
import requests
from PIL import Image
from StringIO import StringIO
from collections import OrderedDict

MAX_NUM = int('FFFFFF', 16)
PARTITIONS = 35


class UrlParameterGroup(ParameterGroup):
    URL = Parameter(name='url', label='Image Url', default='https://tropofy.com/static/css/img/get_started.png', allowed_type=str)


class ColorHistogram(Chart):
    def get_chart_type(self, app_session):
        return Chart.BARCHART

    def get_table_data(self, app_session):
        # Get the image
        link = app_session.data_set.get_param(UrlParameterGroup.URL.name)
        response = requests.get(link)
        img = Image.open(StringIO(response.content))

        # Get RGB values for the image
        rgb_img = img.convert('RGBA')
        width, height = rgb_img.size

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

        # The total number of pixels is width * height
        # Use this value to normalise the values in the map
        total = width * height
        return [{"color": '#' + hex(k)[2:].upper(), "pct": float(v)/total} for k, v in result_dict.iteritems()]

    def get_table_schema(self, app_session):
        return {
            "color": ("string", "Color"),
            "pct": ("number", "pct")
        }

    def get_column_ordering(self, app_session):
        return ["color", "pct"]

    def get_order_by_column(self, app_session):
        return "color"


class HistogramApp(AppWithDataSets):
    def get_name(self):
        return "Color Histogram App"

    def get_gui(self):
        return [
            StepGroup(name='Input', steps=[
                Step(name='URL', widgets=[
                    ParameterForm()
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
