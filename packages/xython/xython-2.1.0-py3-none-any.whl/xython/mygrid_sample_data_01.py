# -*- coding: utf-8 -*-
from datetime import datetime #내장모듈

#from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

result = []
for x in range(0, 20):
	for y in range(0, 50):
		temp = {"x": x, "y": y, "text": str(str(x) + "-" + str(y))}
		result.append(temp)

mydic = {
    "font_color": None, "font_size": None, "font_background": None, "font_bold": None,
    "font_colorindex": None, "font_creator": None, "font_style": None, "font_italic": None,
    "font_name": None, "font_strikethrough": None, "font_subscript": None, "font_superscript": None,
    "font_themecolor": None, "font_themefont": None, "font_tintandshade": None, "font_underline": None,
    "line_top_do": None, "line_top_color": None, "line_top_colorindex": None, "line_top_tintandshade": None,
    "line_top_thick": None, "line_top_style": None, "line_top_brush": None,
    "line_bottom_do": None, "line_bottom_color": None, "line_bottom_colorindex": None, "line_bottom_tintandshade": None,
    "line_bottom_thick": None, "line_bottom_style": None, "line_bottom_brush": None,
    "line__do": None, "line__color": None, "line__colorindex": None, "line__tintandshade": None, "line__thick": None,
    "line__style": None, "line__brush": None,
    "line_right_do": None, "line_right_color": None, "line_right_colorindex": None, "line_right_tintandshade": None,
    "line_right_thick": None, "line_right_style": None, "line_right_brush": None,
    "line_left_do": None, "line_left_color": None, "line_left_colorindex": None, "line_left_tintandshade": None,
    "line_left_thick": None, "line_left_style": None, "line_left_brush": None,
    "line_x1_do": None, "line_x1_color": None, "line_x1_colorindex": None, "line_x1_tintandshade": None,
    "line_x1_thick": None, "line_x1_style": None, "line_x1_brush": None,
    "line_x2_do": None, "line_x2_color": None, "line_x2_colorindex": None, "line_x2_tintandshade": None,
    "line_x2_thick": None, "line_x2_style": None, "line_x2_brush": None,
    "kind_big": None, "kind_middle": None,    "memo": None,    "action": None,
    "checked": None,    "caption": None,    "fun": None,    "kind_1": None,
    "kind_2": None,    "user_type": None,    "text": None,    "text_kind": None,
    "value": None,    "value2": None,    "formularr1c1": None,    "formular": None,
    "background_color": None,    "background_colorindex": None,    "numberformat": None,    "widget": None,
    "align": None,    "decoration": None,    "edit": None,    "access_text": None,
    "access": None,    "order": None,    "size": None,    "check": None,
    "color": None,    "function": None,    "icon": None,    "draw_line": None,
    "protect": None,    "status": None,    "what": None,    "setup": None,
    "tool_tip": None,    "etc": None,    "user_1": None,    "user_2": None,
    "user_3": None,    "x": None,    "y": None,
}


my_values_1 = [
			{"x": 2, "y": 1, "kind_1": "basic", "kind_2":"date", "value": datetime(2002, 2, 2)},
			{"x": 2, "y": 3, "kind_1": "basic", "kind_2":"basic", "text": "값"},
			{"x": 2, "y": 5, "kind_1": "basic", "kind_2":"basic", "text": "값"},
			{"x": 2, "y": 7, "kind_1": "basic", "kind_2":"date", "value": datetime(2002, 2, 2)},
			{"x": 8, "y": 8, "draw_line":"yes", "line_top_dic": {"do": "yes", "color": Qt.GlobalColor.red, "thick": 3, "style": Qt.PenStyle.SolidLine, "brush": "basic", }},
			{"x": 8, "y": 9, "draw_line": "yes",
			 "line_top_dic": {"do": "yes", "color": Qt.GlobalColor.red, "thick": 3, "style": Qt.PenStyle.SolidLine, "brush": "basic", }},
			{"x": 8, "y": 8, "draw_line": "yes",
			 "line_bottom_dic": {"do": "yes", "color": Qt.GlobalColor.red, "thick": 3, "style": Qt.PenStyle.SolidLine, "brush": "basic", }},
			{"x": 8, "y": 8, "draw_line": "yes",
			 "line_left_dic": {"do": "yes", "color": Qt.GlobalColor.red, "thick": 3, "style": Qt.PenStyle.SolidLine, "brush": "basic", }},

			{"x": 2, "y": 6, "kind_1": "tool_tip", "text": "tool_tip", "tool_tip": "툴팁입니다"},
			{"x": 5, "y": 3, "kind_1": "widget", "kind_2":"combo", "value": [1, 2, 3, 4, 5]},
			{"x": 5, "y": 5, "kind_1": "widget", "kind_2": "check_box", "checked": 1, "text":"check"},
			{"x": 5, "y": 7, "kind_1": "widget", "kind_2":"progress_bar", "value": 30},
			{"x": 5, "y": 8, "kind_1": "widget", "kind_2":"button", "caption": "button_1", "action":"action_def"},

			{"x": 10, "y": 10, "kind_1": "memo", "value": "memo memo"},
			{"x": 2, "y": 2, "kind_1": "memo", "value": "memo memo"},

			{"x": 7, "y": 3, "kind_1": "font_color", "value": [255, 63, 24]},
			{"x": 7, "y": 5, "kind_1": "background_color", "value": [255, 63, 24]},
					   ]

result.extend(my_values_1)

common_var = {"basic_color": [217, 217, 217],
			  "color": "",
			  "copy_items": [],
			  "grid_x_len": 5000,
			  "grid_y_len": 100,
			  "window_title": "Grid_Man",
			  "background_color": [123, 123, 123],
			  "grid_height": 25,
			  "grid_width": 200,
			  }

def write_data():
	return result

def setup_data():
	return mydic