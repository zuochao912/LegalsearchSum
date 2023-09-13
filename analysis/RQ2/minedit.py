import json

def minDistance(word1: str, word2: str) -> int:
    n = len(word1)
    m = len(word2)
    
    # 有一个字符串为空串
    if n * m == 0:
        return n + m
    
    # DP 数组
    D = [ [0] * (m + 1) for _ in range(n + 1)]
    
    # 边界状态初始化
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    
    # 计算所有 DP 值
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            left = D[i - 1][j] + 1
            down = D[i][j - 1] + 1
            left_down = D[i - 1][j - 1] 
            if word1[i - 1] != word2[j - 1]:
                left_down += 1
            D[i][j] = min(left, down, left_down)
    
    return D[n][m]

string1="猜猜我是谁"
string2="我是z谁c"
'''
operation:
插入一个字符；
删除一个字符；
替换一个字符。
'''

print(minDistance(string1,string2))
'''
本质等价于：
在单词 A 中插入一个字符；
在单词 B 中插入一个字符；
修改单词 A 的一个字符。
'''