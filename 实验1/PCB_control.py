# coding:utf8

# 模拟pcb类,所有链表都是有空头的

from PCB_class import process_node
import random

class pcb_simulator():
    def __init__(self):
        #队列管理
        self.head_running = process_node(pid=-1,mem_size=0)  # 初始化running队列的head
        self.head_ready = process_node(pid=-1,mem_size=0)  # 初始化ready队列的head
        self.head_block = process_node(pid=-1,mem_size=0)  # 初始化block队列的head
        self.head_new = process_node(pid=-1,mem_size=0)  # 初始化new队列的head
        #内存管理
        self.total_memsize = 1000
        self.occupied_size = 0

    # 找到此节点的所在队列的head
    def find_head(self, status):
        if status == 'ready':
            return self.head_ready
        elif status == 'running':
            return self.head_running
        elif status == 'blocked':
            return self.head_block
        elif status == 'new':
            return self.head_new
    # 删除某节点，传入参数为要删除的节点
    def drop_node(self, drop_node):
        head = self.find_head(drop_node.status)
        p = head
        while p.next != drop_node:
            p = p.next
        p.next = drop_node.next
        drop_node.next = None
        return drop_node
    # 传入参数为某队列的head节点，求出队列的长度
    def length(self, head):
        p, n = head, 0
        while p.next != None:
            n += 1
            p = p.next
        return n
    # 遍历head为首的队列
    def travel(self, head):
        p = head;
        q = []
        while p.next != None:
           q.append(p.next.pid)
           p=p.next
        return q

    # 新建一个节点，将它放入new队列中 状态为new
    def create(self, pid, mem_size=200, PRL=1):
        mem_size = random.randint(200, 400)
        PRL = random.randint(1,5)
        new_node = process_node(pid,mem_size,PRL)
        new_node.status = 'new'
        if self.head_new.next == None:
            self.head_new.next = new_node
        else:
            p = self.head_new
            while p.next != None:
                p = p.next
            p.next = new_node
        return new_node
    # 使进程ready的函数
    def admit(self, ready_node):
        if self.occupied_size+ready_node.mem_size <= self.total_memsize:
            ready_node = self.drop_node(ready_node)
            head = self.head_ready
            p = head
            while p.next != None and ready_node.PRL >= p.PRL:
                p = p.next
            if p.next == None:
                p.next = ready_node
            else:
                ready_node.next=p.next
                p.next=ready_node
            ready_node.status = 'ready'
            self.occupied_size += ready_node.mem_size
            return True
        else:
            return False
    # 将某节点放入block队列中
    def event_wait(self, block_node):
        block_node = self.drop_node(block_node)
        block_node.status = 'blocked'
        p = self.head_block
        while p.next != None and block_node.PRL >= p.PRL:
            p = p.next
        if p.next == None:
            p.next = block_node
        else:
            block_node.next = p.next
            p.next = block_node
    # 在时间片用完时自动调用 在ready队列中找优先级最高的节点置于running队列中 此队列只能有一个节点
    def running(self):
        if self.head_running.next != None:
            if self.head_ready.next == None:
                return
            else:
                running_node = self.head_running.next
                running_node = self.drop_node(running_node)
                running_node.status = 'ready'

                ready_node = self.head_ready.next
                ready_node = self.drop_node(ready_node)
                ready_node.status = 'running'

                self.head_running.next = ready_node

                p = self.head_ready
                while p.next != None and running_node.PRL >= p.PRL:
                    p = p.next
                if p.next == None:
                    p.next = running_node
                else:
                    running_node.next = p.next
                    p.next = running_node
        # running队列为空
        else:
            if self.head_ready.next == None:
                return
            # running队列为空，ready队列不为空
            else:
                ready_node = self.head_ready.next
                ready_node = self.drop_node(ready_node)
                ready_node.status = 'running'
                self.head_running.next = ready_node

    # 使进程从阻塞(block)队列中被唤醒，进入ready队列
    def event_occur(self, wakeup_node):
        wakeup_node = self.drop_node(wakeup_node)

        head_ready = self.head_ready
        p = head_ready
        while p.next != None and wakeup_node.PRL >= p.PRL:
            p = p.next
        if p.next == None:
            p.next = wakeup_node
        else:
            wakeup_node.next = p.next
            p.next = wakeup_node
        wakeup_node.status = 'ready'
    # 释放进程
    def release(self, terminate_node):
        terminate_node = self.drop_node(terminate_node)
        terminate_node.status = 'exit'
        self.occupied_size -= terminate_node.mem_size

# 测试函数
if __name__ == '__main__':
    pcb = pcb_simulator()
    pid1 = pcb.create(1,200,1)
    pid2 = pcb.create(2,400,2)
    pid3 = pcb.create(3,500,5)
    pid4 = pcb.create(4,800,3)
    pid5 = pcb.create(5,100,3)
    print(pcb.travel(pcb.head_new))

    pcb.event_wait(pid4)
    pcb.event_occur(pid4)
    pcb.running()

    p = pcb.head_new.next
    while p != None:
        p.print_status()
        p = p.next