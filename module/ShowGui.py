# -*- coding: utf-8 -*-


from OCC.Display.qtDisplay import qtViewer3d
from PyQt5 import QtCore, QtGui, QtWidgets
from ui import MainGui
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem, QAbstractItemView,
							 QComboBox, QPushButton, QDockWidget, QListWidget)
from PyQt5.QtGui import QKeySequence as QKSec
from PyQt5.QtGui import QIcon,QBrush
from GUI.RibbonButton import RibbonButton
from GUI.RibbonScrollarea import RibbonScrollarea
from GUI.Icons import get_icon
from GUI.RibbonTextbox import RibbonTextbox
from GUI.RibbonWidget import *
from PyQt5.QtCore import  Qt
from module import DisplayManager,ModelTree,OCAFModule


class Auto_create_ribbon(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.ribbon_dict={}
		self.ribbon_table={}  # table 选项
		self._action_dict = {}
		self.ribbon_list = []
		self.panel_dict = {}
		self.Read_ribbon_init()
		self.Create_ribbon()
	def Read_ribbon_init(self):
		with open("./GUI/Ribbon.ini","r",encoding="utf-8") as f:
			inner=f.readlines()
			for i in inner:
				if i=="\t":
					continue
				else:
					i=i.replace("\n","")
					self.ribbon_list.append(i)
	def Create_ribbon(self):
		for ribbon in self.ribbon_list:
			ribbon_list=ribbon.split(" ")
			table_name=ribbon_list[0].split("=")[1]
			panel_name = ribbon_list[1].split("=")[1]
			action_name = ribbon_list[2].split("=")[1]
			icon_name = ribbon_list[3].split("=")[1]
			status_tip = ribbon_list[4].split("=")[1]
			icon_visible = ribbon_list[5].split("=")[1]
			connection = ribbon_list[6].split("=")[1]
			shortcut = ribbon_list[7].split("=")[1]
			if connection=="None":
				connection="self.void_funtion"
			if not table_name in self.ribbon_table.keys():
				self.ribbon_table[table_name]=self.parent._ribbon.add_ribbon_tab(table_name) #创建table
			self._action_dict[action_name]=self.add_action(action_name, icon_name, status_tip, True, eval(connection), None)#创建action
			
			if  not table_name in self.ribbon_dict.keys():
				self.panel_dict[panel_name]=self.ribbon_table[table_name].add_ribbon_pane(panel_name)#创建panel
				self.ribbon_dict[table_name]=self.panel_dict.keys()
			else:
				if not panel_name in self.ribbon_dict[table_name]:
					self.panel_dict[panel_name] = self.ribbon_table[table_name].add_ribbon_pane(panel_name)  # 创建panel
					self.ribbon_dict[table_name] = self.panel_dict.keys()
			self.panel_dict[panel_name].add_ribbon_widget(RibbonButton(self.parent, self._action_dict[action_name], True))
			
	def Set_font(self):
		font = QtGui.QFont()
		font.setFamily("微软雅黑")
		font.setPointSize(12)
	
	def add_action(self, caption, icon_name, status_tip, icon_visible, connection, shortcut=None):
		action = QAction(get_icon(icon_name), caption, self.parent)
		action.setStatusTip(status_tip)
		action.triggered.connect(connection)
		action.setIconVisibleInMenu(icon_visible)
		if shortcut is not None:
			action.setShortcuts(shortcut)
		#self.addAction(action)
		return action
	def void_funtion(self):
		pass
	
	
	
class Ui_MainWindow(MainGui.Ui_MainWindow):
	def __init__(self):
		self.setupUi(self)
		#self.setWindowFlags(Qt.FramelessWindowHint)
		self.Displayshape_core=DisplayManager.DisplayManager(self)
		self.OCAF=OCAFModule.OCAF(parent=self)
		self.modeltree=ModelTree.ModelTree()
		self.setCentralWidget(self.Displayshape_core.canve)
		# Create Ribbon
		self._ribbon = RibbonWidget(self)
		self.addToolBar(self._ribbon)
		self.init_ribbon()
		#Create ToolBar
		self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
		self.insertToolBarBreak(self.toolBar)
	
		#self.Displayshape_core.canve.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		#self.Displayshape_core.canve.customContextMenuRequested['QPoint'].connect(self.rightMenuShow)
		
		#Create ModelTree
		self.items = QDockWidget('组合浏览器', self)  # 新建QDockWidget
		self.addDockWidget(Qt.LeftDockWidgetArea, self.items)  # 在主显示区域右侧显示
		self.items.setMinimumWidth(350)# 设置最小大小
		self.items.setWidget(self.modeltree.tree)

	def closeEvent(self, close_event):
		pass

	def init_ribbon(self):
		RibbonMange=Auto_create_ribbon(parent=self)
		
	def rightMenuShow(self):
		try:
			if True:
				rightMenu = QtWidgets.QMenu(self.menuBar)
				self.actionreboot = QtWidgets.QAction(self.canva)
				self.actionreboot.setObjectName("actionreboot")
				self.actionreboot.setText(QtCore.QCoreApplication.translate("MainWindow", "距离测量"))

				self.actionreboot_1 = QtWidgets.QAction(self.canva)
				self.actionreboot_1.setObjectName("actionreboot_1")
				self.actionreboot_1.setText(QtCore.QCoreApplication.translate("MainWindow", "孔径测量"))

				rightMenu.addAction(self.actionreboot)
				rightMenu.addAction(self.actionreboot_1)

				self.actionreboot.triggered.connect(self.Measure_distance_fun)
				self.actionreboot_1.triggered.connect(self.Measure_diameter_fun)

				rightMenu.exec_(QtGui.QCursor.pos())

		except Exception as e:
			print(e)
			pass







