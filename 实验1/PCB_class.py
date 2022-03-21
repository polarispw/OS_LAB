import time

class process_node():
    def __init__(self, pid, mem_size, PRL=1, next_=None):
        self.pid = pid
        self.PRL = PRL
        self.status = ''
        self.mem_size = mem_size
        self.start_time = int(time.time())
        self.run_time = self.start_time  # 实际运行时间

        # 每次running进度+100,运行10release
        self.run_progress = 0  # 初始化程序运行进度
        self.total_progress = 1000  # 程序运行总进度

        self.next = next_

    def print_status(self):
        print('pid: ', self.pid)
        print('PRL: ', self.PRL)
        print('status: ', self.status)
        print('mem_size：', self.mem_size)
        print('start_time：', self.start_time)
        print('run_progress:', self.run_progress)