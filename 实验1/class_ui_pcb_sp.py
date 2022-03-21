from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QInputDialog
from ui_pcb_simulator_panel import Ui_MainWindow
from PCB_control import pcb_simulator
from PCB_process import thread_process_monitor
import global_pcb
import time

class ui_pcb_sp(QtWidgets.QMainWindow,Ui_MainWindow):

	#按钮信号
	create1_signal = QtCore.pyqtSignal(int) #create按钮信号
	create2_signal = QtCore.pyqtSignal(int) #create按钮信号
	create3_signal = QtCore.pyqtSignal(int) #create按钮信号
	create4_signal = QtCore.pyqtSignal(int) #create按钮信号
	create5_signal = QtCore.pyqtSignal(int) #create按钮信号
	admit1_signal = QtCore.pyqtSignal(int)  # 修改admit状态信号
	admit2_signal = QtCore.pyqtSignal(int)  # 修改admit状态信号
	admit3_signal = QtCore.pyqtSignal(int)  # 修改admit状态信号
	admit4_signal = QtCore.pyqtSignal(int)  # 修改admit状态信号
	admit5_signal = QtCore.pyqtSignal(int)  # 修改admit状态信号
	running1_signal = QtCore.pyqtSignal(int)  # 修改running状态信号
	running2_signal = QtCore.pyqtSignal(int)  # 修改running状态信号
	running3_signal = QtCore.pyqtSignal(int)  # 修改running状态信号
	running4_signal = QtCore.pyqtSignal(int)  # 修改running状态信号
	running5_signal = QtCore.pyqtSignal(int)  # 修改running状态信号
	event_wait1_signal = QtCore.pyqtSignal(int) #event_wait按钮信号
	event_wait2_signal = QtCore.pyqtSignal(int) #event_wait按钮信号
	event_wait3_signal = QtCore.pyqtSignal(int) #event_wait按钮信号
	event_wait4_signal = QtCore.pyqtSignal(int) #event_wait按钮信号
	event_wait5_signal = QtCore.pyqtSignal(int) #event_wait按钮信号
	event_occur1_signal = QtCore.pyqtSignal(int) #event_occur按钮信号
	event_occur2_signal = QtCore.pyqtSignal(int) #event_occur按钮信号
	event_occur3_signal = QtCore.pyqtSignal(int) #event_occur按钮信号
	event_occur4_signal = QtCore.pyqtSignal(int) #event_occur按钮信号
	event_occur5_signal = QtCore.pyqtSignal(int) #event_occur按钮信号
	release1_signal = QtCore.pyqtSignal(int) #release按钮信号
	release2_signal = QtCore.pyqtSignal(int) #release按钮信号
	release3_signal = QtCore.pyqtSignal(int) #release按钮信号
	release4_signal = QtCore.pyqtSignal(int) #release按钮信号
	release5_signal = QtCore.pyqtSignal(int) #release按钮信号

	#文本框信号
	PID1_signal = QtCore.pyqtSignal(str)  # PID设置信号
	PID2_signal = QtCore.pyqtSignal(str)  # PID设置信号
	PID3_signal = QtCore.pyqtSignal(str)  # PID设置信号
	PID4_signal = QtCore.pyqtSignal(str)  # PID设置信号
	PID5_signal = QtCore.pyqtSignal(str)  # PID设置信号
	PRL1_signal = QtCore.pyqtSignal(str)  # PRL设置信号
	PRL2_signal = QtCore.pyqtSignal(str)  # PRL设置信号
	PRL3_signal = QtCore.pyqtSignal(str)  # PRL设置信号
	PRL4_signal = QtCore.pyqtSignal(str)  # PRL设置信号
	PRL5_signal = QtCore.pyqtSignal(str)  # PRL设置信号
	mem_size1_signal = QtCore.pyqtSignal(str)  # mem_size设置信号
	mem_size2_signal = QtCore.pyqtSignal(str)  # mem_size设置信号
	mem_size3_signal = QtCore.pyqtSignal(str)  # mem_size设置信号
	mem_size4_signal = QtCore.pyqtSignal(str)  # mem_size设置信号
	mem_size5_signal = QtCore.pyqtSignal(str)  # mem_size设置信号

	progress_signal = QtCore.pyqtSignal(list) #传递进程运行状态信号

	def __init__(self):
		super(ui_pcb_sp, self).__init__()
		self.setupUi(self)
		self.stylesheet=""
		
		#启动进程监视器,监视ready队列
		self.process_monitor = thread_process_monitor(self)
		self.process_monitor.start()
		self.progressdisplay.appendPlainText(self.get_time()+'\t[main]\tPCB Simulator ready')
		self.closeButton.clicked.connect(thread_process_monitor.terminate)
		#给所有create按钮通过信号槽绑定创建进程事件
		self.create1.clicked.connect(self.create1_emit)
		self.create2.clicked.connect(self.create2_emit)
		self.create3.clicked.connect(self.create3_emit)
		self.create4.clicked.connect(self.create4_emit)
		self.create5.clicked.connect(self.create5_emit)
		self.create1_signal.connect(self.create_process)
		self.create2_signal.connect(self.create_process)
		self.create3_signal.connect(self.create_process)
		self.create4_signal.connect(self.create_process)
		self.create5_signal.connect(self.create_process)
		
		#给所有wait按钮通过信号槽绑定阻塞进程事件
		self.event_wait1.clicked.connect(self.event_wait1_emit)
		self.event_wait2.clicked.connect(self.event_wait2_emit)
		self.event_wait3.clicked.connect(self.event_wait3_emit)
		self.event_wait4.clicked.connect(self.event_wait4_emit)
		self.event_wait5.clicked.connect(self.event_wait5_emit)
		self.event_wait1_signal.connect(self.event_wait_process)
		self.event_wait2_signal.connect(self.event_wait_process)
		self.event_wait3_signal.connect(self.event_wait_process)
		self.event_wait4_signal.connect(self.event_wait_process)
		self.event_wait5_signal.connect(self.event_wait_process)
		
		#给所有occur按钮通过信号槽绑定唤醒进程事件
		self.event_occur1.clicked.connect(self.event_occur1_emit)
		self.event_occur2.clicked.connect(self.event_occur2_emit)
		self.event_occur3.clicked.connect(self.event_occur3_emit)
		self.event_occur4.clicked.connect(self.event_occur4_emit)
		self.event_occur5.clicked.connect(self.event_occur5_emit)
		self.event_occur1_signal.connect(self.event_occur_process)
		self.event_occur2_signal.connect(self.event_occur_process)
		self.event_occur3_signal.connect(self.event_occur_process)
		self.event_occur4_signal.connect(self.event_occur_process)
		self.event_occur5_signal.connect(self.event_occur_process)

		# 给所有release按钮通过信号槽绑定唤醒进程事件
		self.release1.clicked.connect(self.release1_emit)
		self.release2.clicked.connect(self.release2_emit)
		self.release3.clicked.connect(self.release3_emit)
		self.release4.clicked.connect(self.release4_emit)
		self.release5.clicked.connect(self.release5_emit)
		self.release1_signal.connect(self.release_process)
		self.release2_signal.connect(self.release_process)
		self.release3_signal.connect(self.release_process)
		self.release4_signal.connect(self.release_process)
		self.release5_signal.connect(self.release_process)

		# 给所有running状态信号绑定running_process函数
		self.admit1_signal.connect(self.admit_process)
		self.admit2_signal.connect(self.admit_process)
		self.admit3_signal.connect(self.admit_process)
		self.admit4_signal.connect(self.admit_process)
		self.admit5_signal.connect(self.admit_process)

		# 给所有running状态信号绑定running_process函数
		self.running1_signal.connect(self.running_process)
		self.running2_signal.connect(self.running_process)
		self.running3_signal.connect(self.running_process)
		self.running4_signal.connect(self.running_process)
		self.running5_signal.connect(self.running_process)
		
		#给progress处理信号绑定process_progress函数
		self.progress_signal.connect(self.process_progress)

		#初始化按钮
		self.create1.setEnabled(True)
		self.event_wait1.setEnabled(False)
		self.event_occur1.setEnabled(False)
		self.release1.setEnabled(False)
		self.create2.setEnabled(True)
		self.event_wait2.setEnabled(False)
		self.event_occur2.setEnabled(False)
		self.release2.setEnabled(False)
		self.create3.setEnabled(True)
		self.event_wait3.setEnabled(False)
		self.event_occur3.setEnabled(False)
		self.release3.setEnabled(False)
		self.create4.setEnabled(True)
		self.event_wait4.setEnabled(False)
		self.event_occur4.setEnabled(False)
		self.release4.setEnabled(False)
		self.create5.setEnabled(True)
		self.event_wait5.setEnabled(False)
		self.event_occur5.setEnabled(False)
		self.release5.setEnabled(False)
		
	def create1_emit(self):
		self.create1_signal.emit(1)
	def create2_emit(self):
		self.create2_signal.emit(2)
	def create3_emit(self):
		self.create3_signal.emit(3)
	def create4_emit(self):
		self.create4_signal.emit(4)
	def create5_emit(self):
		self.create5_signal.emit(5)
		
	def event_wait1_emit(self):
		self.event_wait1_signal.emit(1)
	def event_wait2_emit(self):
		self.event_wait2_signal.emit(2)
	def event_wait3_emit(self):
		self.event_wait3_signal.emit(3)
	def event_wait4_emit(self):
		self.event_wait4_signal.emit(4)
	def event_wait5_emit(self):
		self.event_wait5_signal.emit(5)
		
	def event_occur1_emit(self):
		self.event_occur1_signal.emit(1)
	def event_occur2_emit(self):
		self.event_occur2_signal.emit(2)
	def event_occur3_emit(self):
		self.event_occur3_signal.emit(3)
	def event_occur4_emit(self):
		self.event_occur4_signal.emit(4)
	def event_occur5_emit(self):
		self.event_occur5_signal.emit(5)

	def release1_emit(self):
		self.release1_signal.emit(1)
	def release2_emit(self):
		self.release2_signal.emit(2)
	def release3_emit(self):
		self.release3_signal.emit(3)
	def release4_emit(self):
		self.release4_signal.emit(4)
	def release5_emit(self):
		self.release5_signal.emit(5)

	# 打印日志
	def process_progress(self,progress_list):
		self.progressdisplay.appendPlainText(self.get_time()+'\t[PID'+progress_list[0]+']\tPID'+progress_list[0]+'已执行: '+progress_list[3]+'/'+progress_list[4])
		self.progressdisplay.appendPlainText(self.get_time()+'\t[PID'+progress_list[0]+']\tPID'+progress_list[0]+'已运行时间: '+self.get_time(progress_list[5]))

	# 如节点为None，则只能先创建节点
	def init_button(self, number):
		if number == 1:
			self.create1.setEnabled(False)
			self.event_wait1.setEnabled(True)
			self.event_occur1.setEnabled(True)
			self.release1.setEnabled(True)
		elif number == 2:
			self.create2.setEnabled(False)
			self.event_wait2.setEnabled(True)
			self.event_occur2.setEnabled(True)
			self.release2.setEnabled(True)
		elif number == 3:
			self.create3.setEnabled(False)
			self.event_wait3.setEnabled(True)
			self.event_occur3.setEnabled(True)
			self.release3.setEnabled(True)
		elif number == 4:
			self.create4.setEnabled(False)
			self.event_wait4.setEnabled(True)
			self.event_occur4.setEnabled(True)
			self.release4.setEnabled(True)
		elif number == 5:
			self.create5.setEnabled(False)
			self.event_wait5.setEnabled(True)
			self.event_occur5.setEnabled(True)
			self.release5.setEnabled(True)

	# 创建进程，根据按钮的点击来创建对应进程
	def create_process(self, number):
		if number == 1:
			global_pcb.pid1 = global_pcb.pcb.create(pid=1)
			self.pid1.setText('PID1')
			self.prl1.setText(str(global_pcb.pid1.PRL))
			self.memsize1.setText(str(global_pcb.pid1.mem_size))
			self.init_button(number)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID1]\tPID1 is created')
			# #将status状态颜色变为淡黄
			self.stylesheet = self.stylesheet + "#status1{background-color:#FFFF66;}"
			self.setStyleSheet(self.stylesheet)
		elif number == 2:
			global_pcb.pid2 = global_pcb.pcb.create(pid=2)
			self.pid2.setText('PID2')
			self.prl2.setText(str(global_pcb.pid2.PRL))
			self.memsize2.setText(str(global_pcb.pid2.mem_size))
			self.init_button(number)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID2]\tPID2 is created')
			# #将status状态颜色变为淡黄
			self.stylesheet = self.stylesheet + "#status2{background-color:#FFFF66;}"
			self.setStyleSheet(self.stylesheet)
		elif number == 3:
			global_pcb.pid3 = global_pcb.pcb.create(pid=3)
			self.pid3.setText('PID3')
			self.prl3.setText(str(global_pcb.pid3.PRL))
			self.memsize3.setText(str(global_pcb.pid3.mem_size))
			self.init_button(number)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID3]\tPID3 is created')
			# #将status状态颜色变为淡黄
			self.stylesheet = self.stylesheet + "#status3{background-color:#FFFF66;}"
			self.setStyleSheet(self.stylesheet)
		elif number == 4:
			global_pcb.pid4 = global_pcb.pcb.create(pid=4)
			self.pid4.setText('PID4')
			self.prl4.setText(str(global_pcb.pid4.PRL))
			self.memsize4.setText(str(global_pcb.pid4.mem_size))
			self.init_button(number)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID4]\tPID4 is created')
			# #将status状态颜色变为淡黄
			self.stylesheet = self.stylesheet + "#status4{background-color:#FFFF66;}"
			self.setStyleSheet(self.stylesheet)
		elif number == 5:
			global_pcb.pid5 = global_pcb.pcb.create(pid=5)
			self.pid5.setText('PID5')
			self.prl5.setText(str(global_pcb.pid5.PRL))
			self.memsize5.setText(str(global_pcb.pid5.mem_size))
			self.init_button(number)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID5]\tPID5 is created')
			# #将status状态颜色变为淡黄
			self.stylesheet = self.stylesheet + "#status5{background-color:#FFFF66;}"
			self.setStyleSheet(self.stylesheet)
		self.change_status(number, "<html><head/><body><p align=\"center\">New</p></body></html>")

	def admit_process(self, number):
		if number == 1:
			if global_pcb.pcb.admit(global_pcb.pid1) == True:
				self.progressdisplay.appendPlainText(self.get_time() + '\t[PID1]\tPID1 is ready')
				# 将status状态颜色变为淡蓝
				self.stylesheet = self.stylesheet + '#status1{background-color:#99CCFF;}'
				self.setStyleSheet(self.stylesheet)
				self.change_status(number, "<html><head/><body><p align=\"center\">Ready</p></body></html>")
		elif number == 2:
			if global_pcb.pcb.admit(global_pcb.pid2) == True:
				self.progressdisplay.appendPlainText(self.get_time() + '\t[PID2]\tPID2 is ready')
				# 将status状态颜色变为淡蓝
				self.stylesheet = self.stylesheet + '#status2{background-color:#99CCFF;}'
				self.setStyleSheet(self.stylesheet)
				self.change_status(number, "<html><head/><body><p align=\"center\">Ready</p></body></html>")
		elif number == 3:
			if global_pcb.pcb.admit(global_pcb.pid3) == True:
				self.progressdisplay.appendPlainText(self.get_time() + '\t[PID3]\tPID3 is ready')
				# 将status状态颜色变为淡蓝
				self.stylesheet = self.stylesheet + '#status3{background-color:#99CCFF;}'
				self.setStyleSheet(self.stylesheet)
				self.change_status(number, "<html><head/><body><p align=\"center\">Ready</p></body></html>")
		elif number == 4:
			if global_pcb.pcb.admit(global_pcb.pid4) == True:
				self.progressdisplay.appendPlainText(self.get_time() + '\t[PID4]\tPID4 is ready')
				# 将status状态颜色变为淡蓝
				self.stylesheet = self.stylesheet + '#status4{background-color:#99CCFF;}'
				self.setStyleSheet(self.stylesheet)
				self.change_status(number, "<html><head/><body><p align=\"center\">Ready</p></body></html>")
		elif number == 5:
			if global_pcb.pcb.admit(global_pcb.pid5) == True:
				self.progressdisplay.appendPlainText(self.get_time() + '\t[PID5]\tPID5 is ready')
				# 将status状态颜色变为淡蓝
				self.stylesheet = self.stylesheet + '#status5{background-color:#99CCFF;}'
				self.setStyleSheet(self.stylesheet)
				self.change_status(number, "<html><head/><body><p align=\"center\">Ready</p></body></html>")

	# 运行进程
	def running_process(self,number):
		if number == 1:
			self.clear_status_running()
			self.status1.setText("<html><head/><body><p align=\"center\">Running</p></body></html>")
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID1]\tPID1 is running')
			#将status状态颜色变为绿色
			self.stylesheet = self.stylesheet+'#status1{background-color:#99CC33;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 2:
			self.clear_status_running()
			self.status2.setText("<html><head/><body><p align=\"center\">Running</p></body></html>")
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID2]\tPID2 is running')
			# 将status状态颜色变为绿色
			self.stylesheet = self.stylesheet + '#status2{background-color:#99CC33;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 3:
			self.clear_status_running()
			self.status3.setText("<html><head/><body><p align=\"center\">Running</p></body></html>")
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID3]\tPID3 is running')
			# 将status状态颜色变为绿色
			self.stylesheet = self.stylesheet + '#status3{background-color:#99CC33;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 4:
			self.clear_status_running()
			self.status4.setText("<html><head/><body><p align=\"center\">Running</p></body></html>")
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID4]\tPID4 is running')
			# 将status状态颜色变为绿色
			self.stylesheet = self.stylesheet + '#status4{background-color:#99CC33;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 5:
			self.clear_status_running()
			self.status5.setText("<html><head/><body><p align=\"center\">Running</p></body></html>")
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID5]\tPID5 is running')
			# 将status状态颜色变为绿色
			self.stylesheet = self.stylesheet + '#status5{background-color:#99CC33;}'
			self.setStyleSheet(self.stylesheet)
		
	# 将status为running的状态栏进程的状态栏变为ready
	def clear_status_running(self):
		if self.status1.text() == "<html><head/><body><p align=\"center\">Running</p></body></html>":
			self.status1.setText("<html><head/><body><p align=\"center\">Ready</p></body></html>")
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status1{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif self.status2.text() == "<html><head/><body><p align=\"center\">Running</p></body></html>":
			self.status2.setText("<html><head/><body><p align=\"center\">Ready</p></body></html>")
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status2{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif self.status3.text() == "<html><head/><body><p align=\"center\">Running</p></body></html>":
			self.status3.setText("<html><head/><body><p align=\"center\">Ready</p></body></html>")
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status3{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif self.status4.text() == "<html><head/><body><p align=\"center\">Running</p></body></html>":
			self.status4.setText("<html><head/><body><p align=\"center\">Ready</p></body></html>")
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status4{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif self.status5.text() == "<html><head/><body><p align=\"center\">Running</p></body></html>":
			self.status5.setText("<html><head/><body><p align=\"center\">Ready</p></body></html>")
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status5{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)

	#阻塞进程按钮绑定函数
	def event_wait_process(self,number):
		if number == 1:
			global_pcb.pcb.event_wait(global_pcb.pid1)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID1]\tPID1 is blocked')
			#将status状态颜色变为红色
			self.stylesheet = self.stylesheet + '#status1{background-color:#CC3333;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 2:
			global_pcb.pcb.event_wait(global_pcb.pid2)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID2]\tPID2 is blocked')
			#将status状态颜色变为红色
			self.stylesheet = self.stylesheet+'#status2{background-color:#CC3333;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 3:
			global_pcb.pcb.event_wait(global_pcb.pid3)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID3]\tPID3 is blocked')
			#将status状态颜色变为红色
			self.stylesheet = self.stylesheet+'#status3{background-color:#CC3333;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 4:
			global_pcb.pcb.event_wait(global_pcb.pid4)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID4]\tPID4 is blocked')
			#将status状态颜色变为红色
			self.stylesheet = self.stylesheet+'#status4{background-color:#CC3333;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 5:
			global_pcb.pcb.event_wait(global_pcb.pid5)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID5]\tPID5 is blocked')
			#将status状态颜色变为红色
			self.stylesheet = self.stylesheet+'#status5{background-color:#CC3333;}'
			self.setStyleSheet(self.stylesheet)
		self.change_status(number,"<html><head/><body><p align=\"center\">Block</p></body></html>")
	
	# 唤醒进程按钮绑定函数
	def event_occur_process(self,number):
		if number == 1:
			global_pcb.pcb.event_occur(global_pcb.pid1)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID1]\tPID1 is ready')
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status1{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 2:
			global_pcb.pcb.event_occur(global_pcb.pid2)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID2]\tPID2 is ready')
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status2{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 3:
			global_pcb.pcb.event_occur(global_pcb.pid3)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID3]\tPID3 is ready')
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status3{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 4:
			global_pcb.pcb.event_occur(global_pcb.pid4)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID4]\tPID4 is ready')
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status4{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 5:
			global_pcb.pcb.event_occur(global_pcb.pid5)
			self.progressdisplay.appendPlainText(self.get_time()+'\t[PID5]\tPID5 is ready')
			#将status状态颜色变为淡蓝
			self.stylesheet = self.stylesheet+'#status5{background-color:#99CCFF;}'
			self.setStyleSheet(self.stylesheet)
		self.change_status(number,"<html><head/><body><p align=\"center\">Ready</p></body></html>")

	# 释放进程
	def release_process(self,number):
		if number == 1:
			global_pcb.pcb.release(global_pcb.pid1)
			self.create1.setEnabled(True)
			self.event_wait1.setEnabled(False)
			self.event_occur1.setEnabled(False)
			self.release1.setEnabled(False)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID1]\tPID1 is blocked')
			# 将status状态颜色变为红色
			self.stylesheet = self.stylesheet + '#status1{background-color:#A9A9A9;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 2:
			global_pcb.pcb.release(global_pcb.pid2)
			self.create2.setEnabled(True)
			self.event_wait2.setEnabled(False)
			self.event_occur2.setEnabled(False)
			self.release2.setEnabled(False)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID2]\tPID2 is blocked')
			# 将status状态颜色变为红色
			self.stylesheet = self.stylesheet + '#status2{background-color:#A9A9A9;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 3:
			global_pcb.pcb.release(global_pcb.pid3)
			self.create3.setEnabled(True)
			self.event_wait3.setEnabled(False)
			self.event_occur3.setEnabled(False)
			self.release3.setEnabled(False)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID3]\tPID3 is blocked')
			# 将status状态颜色变为红色
			self.stylesheet = self.stylesheet + '#status3{background-color:#A9A9A9;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 4:
			global_pcb.pcb.release(global_pcb.pid4)
			self.create4.setEnabled(True)
			self.event_wait4.setEnabled(False)
			self.event_occur4.setEnabled(False)
			self.release4.setEnabled(False)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID4]\tPID4 is blocked')
			# 将status状态颜色变为红色
			self.stylesheet = self.stylesheet + '#status4{background-color:#A9A9A9;}'
			self.setStyleSheet(self.stylesheet)
		elif number == 5:
			global_pcb.pcb.release(global_pcb.pid5)
			self.create5.setEnabled(True)
			self.event_wait5.setEnabled(False)
			self.event_occur5.setEnabled(False)
			self.release5.setEnabled(False)
			self.progressdisplay.appendPlainText(self.get_time() + '\t[PID5]\tPID5 is blocked')
			# 将status状态颜色变为红色
			self.stylesheet = self.stylesheet + '#status5{background-color:#A9A9A9;}'
			self.setStyleSheet(self.stylesheet)
		self.change_status(number, "<html><head/><body><p align=\"center\">Exit</p></body></html>")

	#进程状态发生变化时执行的参数，传入参数为number是第几行，status是进程状态如: ready running status block
	def change_status(self,number,status=''):
		if number == 1:
			label_status =  self.status1
		elif number == 2:
			label_status =  self.status2
		elif number == 3:
			label_status =  self.status3
		elif number == 4:
			label_status =  self.status4
		elif number == 5:
			label_status =  self.status5
		label_status.setText(status)
	
	def get_time(self,run_time=0):
		if run_time == 0:
			timestamp = int(time.time())
			tArray = time.localtime(timestamp)
			return time.strftime('%H:%M:%S',tArray)
		else:
			timestamp = run_time
			run_hours = timestamp // 3600
			timestamp = timestamp % 3600
			run_minutes = timestamp // 60
			run_seconds = timestamp % 60
			return str(run_hours)+'时 '+str(run_minutes)+'分 '+str(run_seconds)+'秒'