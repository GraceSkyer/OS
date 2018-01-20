# 实验内容：
# 通过编写和调试一个系统动态分配资源的简单模拟程序，观察死锁产生的条件，并采用适当的算法，有效地防止和避免死锁地发生。要求如下：
# （1） 模拟一个银行家算法；
# （2） 初始化时让系统拥有一定的资源；
# （3） 用键盘输入的方式申请资源；
# （4） 如果预分配后，系统处于安全状态，则修改系统的资源分配情况；
# （5） 如果预分配后，系统处于不安全状态，则提示不能满足请求。

# 实验原理：
# 银行家算法， 顾名思义是来源于银行的借贷业务，一定数量的本金要应多个客户的借贷周转，为了防止银行加资金无法周转而倒闭，对每一笔贷款，必须考察其是否能限期归还。在操作系统中研究资源分配策略时也有类似问题，系统中有限的资源要供多个进程使用，必须保证得到的资源的进程能在有限的时间内归还资源，以供其他进程使用资源。如果资源分配不得到就会发生进程循环等待资源，则进程都无法继续执行下去的死锁现象。
# 把一个进程需要和已占有资源的情况记录在进程控制中，假定进程控制块PCB其中“状态”有就绪态、等待态和完成态。当进程在处于等待态时，表示系统不能满足该进程当前的资源申请。“资源需求总量”表示进程在整个执行过程中总共要申请的资源量。显然，，每个进程的资源需求总量不能超过系统拥有的资源总数, 银行算法进行资源分配可以避免死锁。

import numpy as np

# 初始化各数据结构   初始化有3种资源，5个进程
# 可利用各资源总数
Available = np.array([3, 3, 2])
# 各进程最大需求资源数
Max = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
# 已分配各进程的资源数
Allocation = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
# 各进程尚需的资源数
Need = np.array([[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]])

safeList = []             # 安全进程执行序列
Request = []              # 各进程对各资源的请求
Request_name = ""         # 进程名称


def input_req():
    global Allocation, Available, Max, Need, safeList, Request, Request_name
    try:
        Request_name = int(input("请输入请求进程的编号(编号从0开始计)："))
        str_in = input("请输入对各资源的请求数 :")
        req = [int(n) for n in str_in.split()]

        Request = np.array(req)

    except:
        print("输入错误，请重新输入")
        input_req()


def banker_algorithm():
    global Allocation, Available, Max, Need, safeList, Request, Request_name
    input_req()

    if (Request <= Need[Request_name]).all():
        if (Request <= Available).all():
            Allocation[Request_name] += Request    # 已分配资源增加
            Available -= Request                   # 可利用资源减少
            Need[Request_name] -= Request          # 尚需的资源数减少

            f = safe()                                 # 执行安全算法
            if f is False:
                Allocation[Request_name] -= Request
                Available += Request
                Need[Request_name] += Request
        else:
            print("进程请求超出可利用的资源数，请等待")
    else:
        print("进程请求超出所需的资源数")


def safe():
    work = Available.copy()            # 工作向量
    finish = 5 * [False]
    global safeList
    safeList = []

    while True:
        flag = False

        for i in range(0, 5):
            # print(Need[i], work)
            if (finish[i] is False) and (Need[i] <= work).all():
                for k in range(3):
                    work[k] = work[k] + Allocation[i][k]
                finish[i] = True
                safeList.append(i)
                flag = True
        if flag is False:
            break

    if False in finish:
        print("系统处于不安全状态")
        return False
    else:
        print("系统处于安全状态")
        print("安全序列为：", safeList)
        return True


while True:
    print('每个进程所需的各资源数：')
    print(Need)
    print('每个进程已分配的各资源数：')
    print(Allocation)
    print('可利用的各资源数：')
    print(Available)
    safe()
    banker_algorithm()
    flag2 = input('是否继续？（y/n）')
    if flag2 == 'n':
        break
