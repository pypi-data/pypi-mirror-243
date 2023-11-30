# -*- coding: utf-8 -*-
import pandas
import matplotlib.pyplot as plt
import numpy as np
import scolor, basic_data
import folium
from folium import plugins
import json
from folium.plugins import MeasureControl

var = {}
class rgraph:
	def __init__(self):
		self.chart = plt
		self.line_color = "k"
		self.line_style = "-"
		self.marker_style = "o"
		self.chart.rc("font", family="Malgun Gothic")
		self.chart_type ="plot"
		self.chart.grid(False)
		self.mycolor = scolor.scolor()
		self.common = basic_data.basic_data()

	def set_chart_type(self, input_type):
		self.chart_type ="plot"
		"""
		plt.bar(x, values)
		plt.pie(ratio, labels=labels, autopct='%.1f%%')
		
		
		
		"""

	def write_text(self):
		# 5. 텍스트 삽입하기
		ax.text(1.5, 3.5, 'Max of Data B')

	def insert_shape(self):
		# 4. 사각형 그리기
		ax.add_patch(
			patches.Rectangle(
				(1.8, 1.0),  # (x, y)
				0.4, 1.5,  # width, height
				edgecolor='deeppink',
				facecolor='lightgray',
				fill=True,
			))



	def set_tile_style(self):
		plt.style.use('bmh')

	# plt.style.use('ggplot')
	# plt.style.use('classic')
	# plt.style.use('Solarize_Light2')
	# plt.style.use('default')


	def set_data(self, input_list_1, input_list_2):
		"""
		좌표값을 넣는 것
		:param input_list_1: 
		:param input_list_2: 
		:return: 
		"""
		self.xy_data = self.check_xy_data(input_list_1, input_list_2)

	def set_grid_line(self, input_onoff=False):
		"""
		그리드 라인을 보이게 할것인지 설정하는것
		:param input_onoff:
		:return:
		"""
		self.chart.grid(input_onoff)


	def set_x_title(self, input_text=""):
		if input_text !="":
			self.chart.xlabel(input_text)

	def set_y_title(self, input_text=""):
		if input_text !="":
			self.chart.ylabel(input_text)

	def set_label(self, input_text=["", ""]):
		if input_text[0] !="":
			self.chart.xlabel(input_text[0])
		if input_text[1] !="":
			self.chart.ylabel(input_text[1])

	def set_x_range(self, input_xy):
		"""
		X축의 범위: [xmin, xmax]
		:param input_xy:
		:return: 
		"""
		self.chart.xlim(input_xy)


	def set_xtick(self, input_list):
		"""

		:param input_list:
		:return:
		"""
		self.chart.xticks(input_list[0], input_list[1])

	def set_ytick(self, input_list):
		"""

		:param input_list:
		:return:
		"""
		self.chart.yticks(input_list[0], input_list[1])

	def set_y_range(self, input_xy):
		"""
		y축의 범위: [ymin, ymax]
		:param input_xy:
		:return:
		"""
		self.chart.ylim(input_xy)

	def set_marker_color(self, input_text):
		"""
		마커의 색
		:param input_text:
		:return:
		"""
		self.line_color = self.check_marker_color(input_text)

	def check_marker_color(self, input_text):
		"""
		색의 이름을 확인하는 부분, 3단어로 색을 표현한다

		:param input_text:
		:return:
		"""
		checked_color = self.common.vars["check_color_name"][input_text]
		print(checked_color)

		m1_dic = {"blu":"b",
		         "gre": "g",
		         "red": "r",
		         "yel": "y",
		         "bla": "k",
				"cya" : 'c',
				"mag": 'm',
				"whi": 'w',
		          }
		result = m1_dic[checked_color]
		return result


	def set_line_style(self, input_text=""):
		"""
		라인의 스타일을 설정하는 것이다

		:param input_text:
		:return:
		"""
		m2_dic = {"-":"-",
		         "--": "--",
		         "-.": "-.",
		         ".": ":",
		         "": "",
		         "none": "",
		         "no": "",
		         }
		self.line_style = m2_dic[input_text]
		return self.line_style


	def set_marker_style(self, input_text):
		m3_dic = {".":".",
		         "o": "o",
		         "rect": "s",
		         "x": "x",
		         "": "",
		         "none": "",
		         "no": "",
		         }
		self.marker_style = m3_dic[input_text]
		return self.marker_style

	def set_title(self, input_text):
		self.chart.title(input_text)

	def check_scale(self):
		pass

	def check_grid(self):
		pass

	def set_chart_type(self, input_text="plot"):
		self.chart_type = input_text

	def check_chart_type(self):
		input_text = self.chart_type
		aaa = self.line_color + self.line_style + self.marker_style

		if input_text == "plot":
			self.chart.plot(self.xy_data[0], self.xy_data[1], aaa)
		elif input_text == "bar":
			self.chart.bar(self.xy_data[0], self.xy_data[1], aaa)
		elif input_text == "pie":
			self.chart.pie(self.xy_data[0], self.xy_data[1], aaa)
		elif input_text == "errorbar":
			self.chart.errorbar(self.xy_data[0], self.xy_data[1], aaa)
		elif input_text == "hist":
			self.chart.hist(self.xy_data[0], self.xy_data[1], aaa)
		elif input_text == "scatter":
			self.chart.scatter(self.xy_data[0], self.xy_data[1], aaa)
			#plt.scatter(x, y, s=area, c=colors, alpha=0.5, cmap='Spectral')

	def set_figure(self):
		#figsize : (width, height)의 튜플을 전달한다. 단위는 인치이다.
		#dpi : 1인치당의 도트 수
		#facecolor : 배경색
		#edgecolor : 외곽선의 색
		pass

	def run(self):
		self.check_chart_type()
		self.save_as_file()
		self.chart.show()



	def save_as_file(self, file_path="D:\\aaa.png", input_format = "PNG"):
		self.chart.savefig(file_path, bbox_inches='tight', dpi=100, format = input_format)
		#self.chart.close()


	def check_xy_data(self, input_list_1="", input_list_2=""):
		"""
		선을 그리는 좌표를 알아서 확인해주는 기능
		:param input_list_1:
		:param input_list_2:
		:return:
		"""
		result_1 = []
		result_2 = []

		if type(input_list_1[0]) == type([]):
			#2차원의 자료이다
			for list_1d in input_list_1:
				result_1.append(list_1d[0])
				result_2.append(list_1d[1])
		else:
			result_1 = input_list_1
			result_2 = input_list_2

		return [result_1, result_2]


	def read_json_data(self,file_path):
		with open(file_path, mode='rt', encoding='utf-8') as f:
			result = json.loads(f.read())
			f.close()
		return result


	def draw_json_data_at_map(self,map_object, json_data, input_name):
		folium.GeoJson(
			json_data,
			name=input_name
		).add_to(map_object)


	def make_main_map_object(self,input_location, zoom_no):
		# 지도의 중앙지점과 줌의 정도를 설정한다
		# 우리나라의 중앙일것같은 온양온천을 기준으로 표시
		result = folium.Map(
			location=input_location,
			zoom_start=zoom_no,
			# width=750,
			# height=500,
			# tiles='Stamen Toner' #타일의 종류를 설정하는 것이다
		)
		return result


	def draw_circle_at_map(self,input_map, input_location, input_radius):
		folium.Circle(
			radius=input_radius,
			location=input_location,
			popup="The Waterfront",
			color="crimson",
			fill=True,
		).add_to(input_map)


	def draw_lines(self,input_map, input_xy_list):
		folium.PolyLine(
			locations=input_xy_list,
			tooltip='PolyLine'
		).add_to(input_map)


	def draw_rectangle(self,input_map, input_xy_list):
		folium.PolyLine(
			locations=input_xy_list,
			tooltip='Rectangle'
		).add_to(input_map)


	def draw_Polygon(self,input_map, input_xy_list):
		# 다각형의 닫힌 도형을 만드는 것이다
		folium.PolyLine(
			locations=input_xy_list,
			tooltip='Polygon',
			fill=True,
		).add_to(input_map)


	def darw_circle_marker_at_map(self,input_map, input_location, input_radius):
		folium.CircleMarker(
			location=input_location,
			radius=input_radius,  # 점의 크기
			popup="Laurelhurst Park",
			color="#3186cc",
			fill=True,
			fill_color="#3186cc",
		).add_to(input_map)


	def darw_line_at_map(self,input_map, input_location):
		folium.PolyLine(locations=input_location, weight=5, color='red').add_to(input_map)


	def make_folium_top_menu_group(self,input_name):
		main_map_object = self.make_main_map_object([36.7835555121117, 126.99992340628], 8)
		result = folium.FeatureGroup(name=input_name)
		main_map_object.add_child(result)
		return result


	def make_basic_data_set(self,input_lists):
		# 일어오고 싶은 자료들을 자료의 형태에 따라서 만들어야 한다
		result = []
		for one_data in input_lists:
			temp_dic = {}
			temp_dic["address_full"] = one_data[9]
			temp_dic["address_middle"] = one_data[8]
			temp_dic["address_top"] = one_data[7]
			temp_dic["water_element"] = one_data[6]
			temp_dic["temp"] = one_data[5]
			temp_dic["ph"] = one_data[4]
			temp_dic["water_type"] = one_data[3]

			# 아래의 자료는 기본적으로 folium에서 사용되는 형태이다
			temp_dic["title"] = str(one_data[3]) + "<br>" + str(one_data[4]) + "<br>" + str(one_data[5]) + "<br>" + str(
				one_data[6]) + "<br>" + str(one_data[7]) + "<br>" + str(one_data[8]) + "<br>" + str(one_data[9])
			temp_dic["xy"] = [one_data[2], one_data[1]]
			temp_dic["pop_text"] = one_data[8]
			temp_dic["html"] = one_data[8] + "<br>" + temp_dic["title"]
			temp_dic["iframe"] = folium.IFrame(html=temp_dic["html"], width=300, height=200)
			result.append(temp_dic)
		return result


	# 오른쪽의 선택하는 그룹에 나타나게 할것인지를 설정하는 것이다
	def make_folium_sub_menu_group(self,top_menu_title, category_location, input_title, all_data_set):
		main_map_object = self.make_main_map_object([36.7835555121117, 126.99992340628], 8)
		dic_sub_menus = {}
		fg_name = folium.FeatureGroup(name=top_menu_title)
		main_map_object.add_child(fg_name)

		for num in range(len(category_location)):
			sun_menu_name = category_location[num]
			aaa = plugins.FeatureGroupSubGroup(fg_name, sun_menu_name, show=True)
			main_map_object.add_child(aaa)
			dic_sub_menus[sun_menu_name] = aaa

			for one_dic in all_data_set:
				if one_dic[input_title] in list(dic_sub_menus.keys()):
					folium.Marker(
						location=one_dic["xy"],
						popup=folium.Popup(one_dic["iframe"]),
						icon=folium.Icon(icon_size=(25)),  # 아이콘을 설정한 것이다
						tooltip=one_dic["title"],
					).add_to(dic_sub_menus[one_dic[input_title]])


	def make_unique_list(self,input_lists, input_no):
		result = set()
		for one in input_lists:
			result.add(one[input_no])
		return list(result)


	def draw_choropleth_at_map(self, geo_data, table_data, bar_title):
		# Choropleth 레이어를 만들고, 맵 m에 추가합니다.
		main_map_object = self.make_main_map_object([36.7835555121117, 126.99992340628], 8)
		folium.Choropleth(
			geo_data=geo_data,
			data=table_data,
			columns=('name', 'code'),
			key_on='feature.properties.name',
			fill_color='BuPu',
			legend_name=bar_title,
		).add_to(main_map_object)


#plt.scatter(x, y, s=area, c=colors)

aaa = rgraph()


aaa.set_title("title / 타이틀")
aaa.set_grid_line("o")
aaa.set_x_title("xxx")
aaa.set_y_title("yyy")
aaa.set_line_style("")
aaa.set_chart_type("plot")

aaa.set_marker_color("blu")
aaa.set_marker_style("o")

aaa.set_xtick([[1, 2, 8], ["Low", "Zero", "High"]])

x, y=[1, 2, 3, 4] ,[2, 3, 5, 10]
x1, y1=[1, 5, 7, 4] ,[2, 3, 4, 10]
aaa.set_data(x, y)
aaa.set_data(x1, y1)
plt.fill_between(x[1:3], y[1:3], alpha=0.5)


aaa.run()

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.2, 1.2)

x, y = [], []
line, = plt.plot([], [], 'bo')


def update(frame):
    x.append(frame)
    y.append(np.sin(frame))
    line.set_data(x, y)
    return line,


ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128))
plt.show()


"""