from PyQt5 import QtWidgets
from PCB_control import pcb_simulator
import threading
import time
import global_pcb

class thread_process_monitor(threading.Thread):
    def __init__(self, QWidget):
        super(thread_process_monitor, self).__init__()
        self.mainwindow = QWidget
        self.running = True

    def run(self):
        while self.running:
            # 检查new缓冲区
            head = global_pcb.pcb.head_new
            p = head.next
            while p != None:
                if p.pid == 1:
                    self.mainwindow.admit1_signal.emit(1)
                elif p.pid == 2:
                    self.mainwindow.admit2_signal.emit(2)
                elif p.pid == 3:
                    self.mainwindow.admit3_signal.emit(3)
                elif p.pid == 4:
                    self.mainwindow.admit4_signal.emit(4)
                elif p.pid == 5:
                    self.mainwindow.admit5_signal.emit(5)
                p = p.next


            # 检查ready队列
            head = global_pcb.pcb.head_ready
            p = head.next
            if p != None:
                if p.pid == 1:
                    self.mainwindow.running1_signal.emit(1)
                elif p.pid == 2:
                    self.mainwindow.running2_signal.emit(2)
                elif p.pid == 3:
                    self.mainwindow.running3_signal.emit(3)
                elif p.pid == 4:
                    self.mainwindow.running4_signal.emit(4)
                elif p.pid == 5:
                    self.mainwindow.running5_signal.emit(5)
            else:
                if global_pcb.pcb.head_running.next == None:
                    time.sleep(1)
                    continue
                else:
                    p = global_pcb.pcb.head_running.next
            # 开始执行一段时间片
            global_pcb.pcb.running()
            time.sleep(1)
            p.run_progress += 100
            p.run_time += 3

            progress_list = []
            progress_list.append(str(p.pid))
            progress_list.append(str(p.PRL))
            progress_list.append(str(p.mem_size))
            progress_list.append(str(p.run_progress))
            progress_list.append(str(p.total_progress))
            progress_list.append(p.run_time - p.start_time)
            self.mainwindow.progress_signal.emit(progress_list)

            if p.run_progress >= p.total_progress:
                if p.pid == 1:
                    self.mainwindow.release1_signal.emit(1)
                elif p.pid == 2:
                    self.mainwindow.release2_signal.emit(2)
                elif p.pid == 3:
                    self.mainwindow.release3_signal.emit(3)
                elif p.pid == 4:
                    self.mainwindow.release4_signal.emit(4)
                elif p.pid == 5:
                    self.mainwindow.release5_signal.emit(5)

            time.sleep(2)

    def terminate(self):
        self.running = False