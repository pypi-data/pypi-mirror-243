# -*- coding: utf-8 -*-
import win32com.client  # pywin32의 모듈
import pythoncom

class han:
	def __init__(self, file_name=""):

		if file_name=="":
			self.active_doc()
		elif file_name=="new":
			self.han_program = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
			self.han_program.XHwpWindows.Item(0).Visible = 1
		else:
			self.han_program = win32com.client.gencache.EnsureDispatch("HWPFrame.HwpObject")
			self.han_program.XHwpWindows.Item(0).Visible = 1
			self.han_program.Open(file_name)

	def active_doc(self):
		context = pythoncom.CreateBindCtx(0)
		running_coms = pythoncom.GetRunningObjectTable()
		monikers = running_coms.EnumRunning()
		for moniker in monikers:
			name = moniker.GetDisplayName(context, moniker)
			if "hwp" in str(name).lower():
				obje = running_coms.GetObject(moniker)
				self.han_program = win32com.client.Dispatch(obje.QueryInterface(pythoncom.IID_IDispatch))
				self.han_program.XHwpWindows.Item(0).Visible = 1
		return self.han_program

	def action_1(self):
		self.han_program.HAction.Run("MoveSelLineEnd")  # 라인 끝까지 선택
		self.han_program.HAction.Run("CharShapeBold")  # 진하게 적용
		self.han_program.HAction.Run("MoveLineBegin")  # 캐럿 원래위치로

	def add_table(self):
		set = self.han_program.CreateSet("Table")
		set.SetItem("Rows", 5)
		set.SetItem("Cols", 5)
		self.han_program.InsertCtrl("tbl", set)

	def alignment(self):
		#self.han_program.HAction.Run("ParagraphShapeAlignLeft")
		pass

	def close(self):
		self.han_program.Clear(3)
		self.han_program.Quit()

	def copy(self):
		self.han_program.HAction.Run('Copy')  # Ctrl-C (복사)

	def count_table(self):
		# hwpctrlapi 기반
		ctrl = self.han_program.HeadCtrl  # 첫번째 컨트롤(HaedCtrl)부터 탐색 시작.
		count = 0
		while ctrl != None:
			nextctrl = ctrl.Next
			print(ctrl.CtrlID)
			if ctrl.CtrlID == "tbl":
				count += 1

			ctrl = nextctrl
		print(count)

	# 표 글자 취급하기
	def insert_next_line(self):
		self.han_program.HAction.Run("BreakPara") #줄바꾸기

	def insert_table_x_line(self):
		self.han_program.HAction.Run("TableInsertLowerRow") #줄추가

	def make_table(self, x, y):
		self.han_program.HParameterSet.HTableCreation.Rows = x
		self.han_program.HParameterSet.HTableCreation.Cols = y
		self.han_program.HParameterSet.HTableCreation.WidthType = 2
		self.han_program.HParameterSet.HTableCreation.HeightType = 1
		self.han_program.HParameterSet.HTableCreation.WidthValue = self.han_program.MiliToHwpUnit(148.0)
		self.han_program.HParameterSet.HTableCreation.HeightValue = self.han_program.MiliToHwpUnit(150)
		self.han_program.HParameterSet.HTableCreation.CreateItemArray("ColWidth", x)
		self.han_program.HParameterSet.HTableCreation.CreateItemArray("RowHeight", y)
		self.han_program.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1  # 글자처럼 취급
		self.han_program.HParameterSet.HTableCreation.TableProperties.Width = self.han_program.MiliToHwpUnit(148)
		self.han_program.HAction.Execute("TableCreate", self.han_program.HParameterSet.HTableCreation.HSet)

	def manual(self):
		obj = self.han_program.HeadCtrl

		idnum = obj.CtrlID
		if (idnum == "gso"):
			pass
		#CtrlID의 종류 : gso(그림객체), eqed(수식), tbl(표), en(미주), fn(각주), secd(구역), cold(단)

		paramSet = obj.GetAnchorPos(0); #그객체의

		list1 = paramSet.Item("List")
		para = paramSet.Item("Para")
		pos = paramSet.Item("Pos")
		self.han_program.SetPos(list1, para, pos)

	def move_cursor_to_begin_of_doc(self):
		self.han_program.HAction.Run("MoveDocBegin")
		#self.han_program.MovePos(2)  # 문서 제일 앞으로

	def move_cursor_to_start_of_next_para(self):
		#다음 분단이 올때까지 이동
		self.han_program.HAction.Run("MoveParaEnd")

	def move_cursor_to_end_of_doc(self):
		# 문서 끝으로 이동
		self.han_program.MovePos(3)

	def move_cursor_to_end_of_range(self):
		self.han_program.HAction.Run("MoveListEnd")

	def move_cursor_to_start_of_range(self):
		self.han_program.HAction.Run("MoveListBegin")


	def move_cursor_to_left_cell_of_table(self):
		self.han_program.HAction.Run("TableLeftCell") #왼쪽셀로 이동

	def move_cursor_to_next_line(self):
		self.han_program.HAction.Run("MoveNextLine")

	def move_cursor_to_next_word(self):
		self.han_program.HAction.Run("MoveNextWord")

	def move_cursor_to_next_char(self):
		self.han_program.HAction.Run("MoveNextChar")

	def move_cursor_to_next_para(self):
		self.han_program.HAction.Run("MoveNextPara")

	def move_cursor_to_next_nth_char(self, input_no):
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextChar")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextChar")

	def move_cursor_to_next_nth_line(self, input_no):
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextLine")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MovePrevLine")

	def move_cursor_to_next_nth_para(self, input_no):
		position_obj = self.han_program.GetPos()
		self.han_program.SetPos(position_obj.list, position_obj.para +input_no, position_obj.pos)

	def move_cursor_to_next_nth_word(self, input_no):
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextWord")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveNextWord")

	def move_cursor_to_previous_nth_page(self, input_no):
		if input_no > 0:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveUp")
		else:
			for no in range(input_no):
				self.han_program.HAction.Run("MoveUp")

	def move_page(self):
		# 5페이지로 이동
		target_page = 5
		self.han_program.HAction.Run("MoveDocBegin") # 문서 시작으로 이동
		for _ in range(target_page-1):
			self.han_program.HAction.Run("MovePageDown") # 문서 시작으로 이동
		self.han_program.InitScan(...)

	def new_table(self):
		self.han_program.HParameterSet.HTableCreation.Rows = 5
		self.han_program.HParameterSet.HTableCreation.Cols = 5
		self.han_program.HParameterSet.HTableCreation.WidthType = 2
		self.han_program.HParameterSet.HTableCreation.HeightType = 1
		self.han_program.HParameterSet.HTableCreation.WidthValue = self.han_program.MiliToHwpUnit(148.0)
		self.han_program.HParameterSet.HTableCreation.HeightValue = self.han_program.MiliToHwpUnit(150)
		self.han_program.HParameterSet.HTableCreation.CreateItemArray("ColWidth", 5)
		self.han_program.HParameterSet.HTableCreation.ColWidth.SetItem(0, self.han_program.MiliToHwpUnit(16.0))
		self.han_program.HParameterSet.HTableCreation.ColWidth.SetItem(1, self.han_program.MiliToHwpUnit(36.0))
		self.han_program.HParameterSet.HTableCreation.ColWidth.SetItem(2, self.han_program.MiliToHwpUnit(46.0))
		self.han_program.HParameterSet.HTableCreation.ColWidth.SetItem(3, self.han_program.MiliToHwpUnit(16.0))
		self.han_program.HParameterSet.HTableCreation.ColWidth.SetItem(4, self.han_program.MiliToHwpUnit(16.0))
		self.han_program.HParameterSet.HTableCreation.CreateItemArray("RowHeight", 5)
		self.han_program.HParameterSet.HTableCreation.RowHeight.SetItem(0, self.han_program.MiliToHwpUnit(40.0))
		self.han_program.HParameterSet.HTableCreation.RowHeight.SetItem(1, self.han_program.MiliToHwpUnit(20.0))
		self.han_program.HParameterSet.HTableCreation.RowHeight.SetItem(2, self.han_program.MiliToHwpUnit(50.0))
		self.han_program.HParameterSet.HTableCreation.RowHeight.SetItem(3, self.han_program.MiliToHwpUnit(20.0))
		self.han_program.HParameterSet.HTableCreation.RowHeight.SetItem(4, self.han_program.MiliToHwpUnit(20.0))
		self.han_program.HParameterSet.HTableCreation.TableProperties.TreatAsChar = 1  # 글자처럼 취급
		self.han_program.HParameterSet.HTableCreation.TableProperties.Width = self.han_program.MiliToHwpUnit(148)
		self.han_program.HAction.Execute("TableCreate", self.han_program.HParameterSet.HTableCreation.HSet)

	def page_break(self):
		self.han_program.HAction.Run("BreakPage") #쪽나눔

	def save(self, file_name=""):
		self.han_program.SaveAs(file_name)
		self.han_program.Quit()

	def paint_color_for_selection(self):
		pass

	def select_all(self):
		self.han_program.Run('SelectAll')

	def select_current_line(self):
		self.han_program.HAction.Run("MoveLineBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveLineEnd")

	def select_current_para(self):
		self.han_program.HAction.Run("MoveParaBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveParaEnd")

	def select_current_word(self):
		self.han_program.HAction.Run("MoveWordBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveWordEnd")

	def select_previous_char(self):
		self.han_program.HAction.Run("MoveSelPrevPos")

	def select_previous_word(self):
		self.han_program.HAction.Run("MoveSelPrevWord")

	def select_previous_line(self):
		self.han_program.HAction.Run("MovePrevLine")
		self.han_program.HAction.Run("MoveLineBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveLineEnd")

	def select_previous_para(self):
		self.han_program.HAction.Run("MovePrevPara")
		self.han_program.HAction.Run("MoveParaBegin")
		self.han_program.Run("Select")
		self.han_program.HAction.Run("MoveParaEnd")

	def select_start_of_word_from_selection(self):
		self.han_program.HAction.Run("MoveSelWordEnd")

	def select_end_of_para_from_selection(self):
		self.han_program.HAction.Run("MoveSelParaEnd")

	def select_start_of_para_from_selection(self):
		self.han_program.HAction.Run("MoveSelParaBegin")

	def select_next_nth_char_from_selection(self, input_no):
		position_obj = self.han_program.GetPos()
		self.han_program.Run("Select")
		self.han_program.SetPos(position_obj.list, position_obj.para, position_obj.pos +input_no)

	def select_next_nth_line_from_selection(self, input_no):
		for no in range(input_no):
			self.han_program.HAction.Run("MoveSelNextLine")

	def select_next_nth_para_from_selection(self, input_no):
		position_obj = self.han_program.GetPos()
		self.han_program.Run("Select")
		self.han_program.SetPos(position_obj.list, position_obj.para +input_no, position_obj.pos)

	def select_next_nth_word_from_selection(self, input_no):
		for no in range(input_no):
			self.han_program.HAction.Run("MoveSelNextWord")

	def check_selection_status(self):
		result = self.han_program.SelectionMode
		return result

	def selection_value(self):
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def read_value_in_selection(self):
		result = self.han_program.GetTextFile("TEXT", "saveblock")
		return result

	def select_start_of_line_from_selection(self):
		self.han_program.HAction.Run('MoveSelLineBegin')

	def select_start_of_list_from_selection(self):
		self.han_program.HAction.Run('MoveSelListBegin')

	def select_end_of_line_from_selection(self):
		self.han_program.HAction.Run("MoveSelLineEnd")

	def select_start(self):
		self.han_program.HAction.Run("Select")

	def move_begin_of_xline_for_table(self):
		self.han_program.HAction.Run("TableRowBegin")

	def move_begin_of_yline_for_table(self):
		self.han_program.HAction.Run("TableColBegin")

	def move_begin_cell_of_table(self):
		self.han_program.HAction.Run("TableLeftCell")

	def set_table_cell_address(self, addr):
		init_addr = self.han_program.KeyIndicator()[-1][1:].split(")")[0]  # 함수를 실행할 때의 주소를 기억.
		if not self.han_program.CellShape:  # 표 안에 있을 때만 CellShape 오브젝트를 리턴함
			raise AttributeError("현재 캐럿이 표 안에 있지 않습니다.")
		if addr == self.han_program.KeyIndicator()[-1][1:].split(")")[0]:  # 시작하자 마자 해당 주소라면
			return  # 바로 종료
		self.han_program.HAction.Run("CloseEx")  # 그렇지 않다면 표 밖으로 나가서
		self.han_program.FindCtrl()  # 표를 선택한 후
		self.han_program.HAction.Run("ShapeObjTableSelCell")  # 표의 첫 번째 셀로 이동함(A1으로 이동하는 확실한 방법 & 셀선택모드)
		while True:
			current_addr = self.han_program.KeyIndicator()[-1][1:].split(")")[0]  # 현재 주소를 기억해둠
			self.han_program.HAction.Run("TableRightCell")  # 우측으로 한 칸 이동(우측끝일 때는 아래 행 첫 번째 열로)
			if current_addr == self.han_program.KeyIndicator()[-1][1:].split(")")[0]:  # 이동했는데 주소가 바뀌지 않으면?(표 끝 도착)
				# == 한 바퀴 돌았는데도 목표 셀주소가 안 나타났다면?(== addr이 표 범위를 벗어난 경우일 것)
				self.set_table_cell_address(init_addr)  # 최초에 저장해둔 init_addr로 돌려놓고
				self.han_program.HAction.Run("Cancel")  # 선택모드 해제
				raise AttributeError("입력한 셀주소가 현재 표의 범위를 벗어납니다.")
			if addr == self.han_program.KeyIndicator()[-1][1:].split(")")[0]:  # 목표 셀주소에 도착했다면?
				return  # 함수 종료


	def tblchar(self):
		code = self.han_program.HeadCtrl
		tp = self.han_program.CreateSet("Table")
		tp.SetItem("TreatAsChar", 1)

		while code != None:
			nextctrl = code.Next

			if code.CtrlID == "tbl":
				code.Properties = tp
			code = nextctrl

	def write_text_at_cursor(self, input_value):
		action = self.han_program.CreateAction("InsertText")
		pset = action.CreateSet()
		pset.SetItem("Text", input_value)
		action.Execute(pset)

	def read_current_char_no(self):
		result = self.han_program.GetPos()
		return result




