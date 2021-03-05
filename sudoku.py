class heap:
    def __init__(self):
        self.heap = []

    def isEmpty(self):
        return self.heap == []

    def heapPush(self, state):
        #self.heap.append(state)
        self.heap.insert(0, state)
        self.arrange()
        return self

    def heapPop(self):
        t = self.heap[0]
        if(len(self.heap) >= 2):
            self.heap[0] = self.heap[len(self.heap) - 1]
            self.heap.pop(len(self.heap) - 1)
            self.arrange()
        else:
            self.heap.pop(0)
        return t
    #ヒープ構造の再構築

    def arrange(self):
        '''
        #単純なヒープ構造の構築方法 O(n)
        n = len(self.heap) - 1
        while n != 0:
            t = self.heap[n].f
            parrent = self.heap[(n - 1) // 2].f
            if (t < parrent):
                self.heap[n], self.heap[(n - 1) // 2] = self.heap[(n - 1) // 2], self.heap[n]
            n -= 1
        '''
        #効率の良いヒープ構造の構築方法 O(log n)
        self.downToLeaf(0, len(self.heap))

    def downToLeaf(self, root, len):
        if 2*root + 1 >= len:
            return
        elif 2*root + 2 >= len or self.heap[2*root + 1].f < self.heap[2*root + 2].f:
            j = 2*root + 1
        else:
            j = 2*root + 2
        if self.heap[j].f < self.heap[root].f:
            #swap
            self.heap[root], self.heap[j] = self.heap[j], self.heap[root]
            self.downToLeaf(j, len)


class Table:
    def __init__(self, table = None):
        if table == None:
            self.table = []
            for _ in range(9):
                str = input().replace('.', '0')
                l = [int(s) for s in str]
                self.table.append(l)
        else:
            self.table = table

    def __copy__(self):
        return Table(self.table)
    
    #[[0]
    # [1]
    # [2]
    # [3]
    # [4]
    # [5]
    # [6]
    # [7]
    # [8]]
    def getRow(self, num):
        ret = []
        for i in range(9):
            ret.append(self.table[num][i])
        return ret
    
    #[[0][1][2][3][4][5][6][7][8]]
    def getColumn(self, num):
        ret = []
        for i in range(9):
            ret.append(self.table[i][num])
        return ret
    
    #[[0][1][2]
    # [3][4][5]
    # [6][7][8]]
    def getBlock(self, num):
        ret = []
        i = num // 3
        j = num % 3
        for y in range(i * 3, (i + 1) * 3):
            for x in range(j * 3, (j + 1) * 3):
                ret.append(self.table[y][x])
        return ret
    def getCount(self, n):
        num = 0
        for i in range(9):
            for j in range(9):
                if self.table[i][j] == n:
                    num += 1
        return num
    def toString(self):
        return str(self.table)
class State:
    import sys, copy

    def __init__(self, table):
        self.table = table
        self.numCandidate = [[0]*9 for i in range(9)]
        for i in range(9):
            for j in range(9):
                if self.table.table[i][j] == 0:
                    self.numCandidate[i][j] = len(self.getCandidate(i, j))
        self.f = self.hCost()
    #(i,j)のブロックに入る事ができる数字の集合を返す
    def getCandidate(self, i, j):
        num_list = {i for i in range(1, 10)}
        t = set(self.table.getRow(i))
        t.discard(0)
        num_list -= t
        t = set(self.table.getColumn(j))
        t.discard(0)
        num_list -= t
        t = set(self.table.getBlock((i // 3) * 3 + (j // 3)))
        t.discard(0)
        num_list -= t
        return num_list
    def hCost(self):
        min = 10
        for i in range(9):
            for j in range(9):
                if self.numCandidate[i][j] < min and self.numCandidate[i][j] > 0:
                    min = self.numCandidate[i][j]
        return min
    def isClear(self):
        return self.table.getCount(0) == 0
    #最小コストのブロックに入りうる数字を入れたオブジェクトのリストを返す
    def nextStates(self):
        import copy
        set = []
        for i in range(9):
            for j in range(9):
                if self.numCandidate[i][j] == self.f:
                    t = self.getCandidate(i, j)
                    if len(t) == 0:
                        continue
                    for itr in t:
                        cp_table = copy.deepcopy(self.table)
                        cp_table.table[i][j] = itr
                        s = State(cp_table)
                        set.append(s)
                    return set
        return set
        
    def printBoard(self):
        print('---------------------------------')
        for i in range(9):
            for j in range(9):
                print(' %d ' % self.table.table[i][j], end='')
                if j % 3 == 2 and j != 8:
                    print(' | ', end='')
                elif j == 8:
                    print()
            if i % 3 == 2:
                print('---------------------------------')

    def candidates(self):
        for i in range(9):
            for j in range(9):
                print(' %d ' % self.numCandidate[i][j], end='')
                if j % 3 == 2 and j != 8:
                    print(' | ', end='')
                elif j == 8:
                    print()
            if i % 3 == 2:
                print('---------------------------------')

def validBlock(block):
    for i in range(1, 10):
        #数字のブロックに重複がある
        if block.count(str(i)) != 1:
            return False
    return True

if __name__ == "__main__":
    import sys

    print("Please input 9*9 sudoku table with swapping blank to '.'")
    init_state = Table()
    start = State(init_state)
    frontier = heap()
    frontier.heapPush(start)
    #exploredは作らない


    while True:
        if frontier.isEmpty():
            print("### Goal not found!")
            break
        s = frontier.heapPop()

        if s.isClear():
            print("### Goal found!")
            for i in range(9):
                for j in range(9):
                    if not validBlock(s.table.getRow(i)):
                        continue
                    elif not validBlock(s.table.getColumn(j)):
                        continue
                    elif not validBlock(s.table.getBlock((i // 3) * 3 + (j // 3))):
                        continue
            s.printBoard()
            break
        for n in s.nextStates():
            #探索済みかのチェックはなし

            #n.printBoard()
            frontier.heapPush(n)
            
