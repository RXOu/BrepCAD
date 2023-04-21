# -*- coding: utf-8 -*-
import threading

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.GC import GC_MakeSegment
from OCC.Core.gp import gp_Pnt
from OCC.Core.AIS import AIS_Shape

class InteractiveOperate(object):
	def __init__(self,parent=None):
		self.parent=parent
		self.InteractiveModule=None
		self.select_shape_list=[]
		self.dragStartPosX = 0
		self.dragStartPosY = 0
		self.aisline=None
		
		
	def clicked_callback(self,shp, *kwargs):
		try:
			if self.InteractiveModule=="SKETCH":
				print(5555,shp)
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(self.parent.Displayshape_core.canva.dragStartPosX,
																				  self.parent.Displayshape_core.canva.dragStartPosY)
				self.point=(x,y,z)
				t = threading.Thread(target=self.getmousemove, args=())
				t.start()
				
		
		except Exception as e:
			print(e)
	
	


	def getmousemove(self):
		while True:
			_dragStartPosY = self.parent.Displayshape_core.canva.dragStartPosY
			_dragStartPosX = self.parent.Displayshape_core.canva.dragStartPosX
			if self.dragStartPosY != _dragStartPosY or self.dragStartPosX != _dragStartPosX:
				(x, y, z, vx, vy, vz) = self.parent.Displayshape_core.canva._display.View.ProjReferenceAxe(_dragStartPosX,
																									   _dragStartPosY)
				#print(x, y, z)
				try:
					x0=self.point[0]
					y0 = self.point[1]
					z0 = self.point[2]
					aSegment = GC_MakeSegment(gp_Pnt(x0, y0, z0), gp_Pnt(x, y, z))
					anEdge = BRepBuilderAPI_MakeEdge(aSegment.Value())
					aWire = BRepBuilderAPI_MakeWire(anEdge.Edge()).Shape()
					if self.aisline == None:
						self.aisline = AIS_Shape(aWire)
						self.aisline=self.parent.Displayshape_core.canva._display.DisplayShape(aWire, True,
																					   False)  # 重新计算更新已经显示的物体
					else:
						self.aisline[0].SetShape(aWire)  # 将已经显示的零件设置成另外一个新零件
					self.parent.Displayshape_core.canva._display.Context.Redisplay(self.aisline[0], True,
																				   False)  # 重新计算更新已经显示的物体
					#self.parent.Displayshape_core.canva._display.FitAll()
				except Exception as e:
					print(e)
					pass
				
			
			
			self.dragStartPosX = _dragStartPosX
			self.dragStartPosY = _dragStartPosY