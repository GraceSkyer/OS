# 实验内容：设计一个请求页式存储管理方案，并编写模拟程序实现之。淘汰算法采用两种不同的算法如：FIFO和LRU，并比较它们的不同之处。

# 不同的置换算法，可使同一组进程发生的缺页率不同，如果采用的置换算法不当，会大大降低CPU的使用高效率。
# FIFO算法优先置换最先进入内存的页。LRU每次选择离当前时间被访问最远的页置换。

def lru(numbers, block):
    count = 0       # 缺页次数
    chart = []      # 主存块
    vis = block*[]
    t = 0
    flag = True     # True表示缺页
    print("三个主存块的数据变化情况:")
    for i in numbers:
        t += 1
        if i not in chart:  # i不在chart中，缺页
            flag = True
            if len(chart) < block:  # 长度小于block,在尾部加i
                chart[len(chart)::] = [i]
                vis[len(chart)::] = [t]
            else:
                pos = vis.index(min(vis))
                chart[pos:pos+1:] = [i]
                vis[pos:pos+1:] = [t]
            count += 1
        else:   # 不缺页
            flag = False
            vis[chart.index(i):chart.index(i)+1:] = [t]

        print(chart, '缺页' if flag is True else '')
    rate = count / len(numbers)
    print("LRU算法结束，总的缺页次数为：", count, '，缺页率为：', rate)


def fifo(numbers, block):
    count = 0       # 缺页次数
    chart = []      # 主存块
    flag = True     # True表示缺页
    print("三个主存块的数据变化情况:")
    for i in numbers:
        if i not in chart:  # i不在chart中，缺页
            flag = True
            if len(chart) < block:  # 长度小于block,在尾部加i
                chart[len(chart)::] = [i]
            else:   # 否则，将后几个往前复制，i往后填
                chart[0:block-1:] = chart[1:block:]
                chart[block-1::] = [i]
            count += 1
        else:
            flag = False
        print(chart, '缺页' if flag is True else '')
    rate = count / len(numbers)
    print("FIFO算法结束，总的缺页次数为：", count, '，缺页率为：', rate)


while True:
    num = int(input('请输入页面访问总次数数目：'))
    str_in = input('请输入访问页面次序的列表：')
    number = [int(n) for n in str_in.split()]
    blocks = int(input('请输入主存块数目：'))
    while True:
        op = int(input('请选择页面置换算法：(1)LRU (2)FIFO:'))
        lru(number, blocks) if op == 1 else fifo(number, blocks)
        flag1 = input('是否继续选择页面置换算法？（y/n）')
        if flag1 == 'n':
            break
    flag2 = input('是否继续？（y/n）')
    if flag2 == 'n':
        break

# 例子输入：
# 20
# 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
# 4
