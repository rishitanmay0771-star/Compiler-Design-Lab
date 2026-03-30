import sys

# ACTION TABLE
A = [
    ["sf","emp","emp","se","emp","emp"],
    ["emp","sg","emp","emp","emp","acc"],
    ["emp","rc","sh","emp","rc","rc"],
    ["emp","re","re","emp","re","re"],
    ["sf","emp","emp","se","emp","emp"],
    ["emp","rg","rg","emp","rg","rg"],
    ["sf","emp","emp","se","emp","emp"],
    ["sf","emp","emp","se","emp","emp"],
    ["emp","sg","emp","emp","sl","emp"],
    ["emp","rb","sh","emp","rb","rb"],
    ["emp","rb","rd","emp","rd","rd"],
    ["emp","rf","rf","emp","rf","rf"]
]

# GOTO TABLE
G = [
    ["b","c","d"],
    ["emp","emp","emp"],
    ["emp","emp","emp"],
    ["emp","emp","emp"],
    ["i","c","d"],
    ["emp","emp","emp"],
    ["emp","j","d"],
    ["emp","emp","k"],
    ["emp","emp","emp"],
    ["emp","emp","emp"],
    ["emp","emp","emp"],
    ["emp","emp","emp"]
]

ter = ['i','+','*',')','(','$']
nter = ['E','T','F']
states = ['a','b','c','d','e','f','g','h','m','j','k','l']

# Grammar rules
rl = [
    ('E',"E+T"),
    ('E',"T"),
    ('T',"T*F"),
    ('T',"F"),
    ('F',"(E)"),
    ('F',"i"),
]

stack = []
temp = ""

# ---------- Helper Functions ----------

def push(item):
    stack.append(item)

def pop():
    if not stack:
        print("Stack empty")
        sys.exit()
    return stack.pop()

def stacktop():
    return stack[-1]

def ister(x):
    return ter.index(x) + 1 if x in ter else 0

def isnter(x):
    return nter.index(x) + 1 if x in nter else 0

def isstate(p):
    return states.index(p) + 1 if p in states else 0

def isproduct(x, p):
    global temp
    k = ister(x)
    l = isstate(p)
    temp = A[l-1][k-1]

def isreduce(x, p):
    global temp
    k = isstate(x)
    l = isnter(p)
    temp = G[k-1][l-1]

def error():
    print("Error in input")
    sys.exit()

def printt(inp, i):
    print("\nStack:", ''.join(stack), "\t Input:", inp[i:])

def rep(c):
    mapping = {
        'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5',
        'g':'6','h':'7','m':'8','j':'9','k':'10','l':'11'
    }
    return mapping.get(c, c)

# ---------- Main Logic ----------

inp = input("Enter input: ")
inp += '$'

push('a')  # initial state

i = 0
printt(inp, i)

while True:
    x = inp[i]
    p = stacktop()

    isproduct(x, p)

    if temp == "emp":
        error()

    if temp == "acc":
        print("\nAccepted input")
        break

    if temp[0] == 's':  # shift
        push(x)
        push(temp[1])
        i += 1

    elif temp[0] == 'r':  # reduce
        j = isstate(temp[1])
        left, right = rl[j-2]

        # pop 2 * len(right)
        for _ in range(2 * len(right)):
            pop()

        push(left)

        y = stack[-2]  # state before non-terminal
        isreduce(y, left)

        push(temp)

    printt(inp, i)

if temp != "acc":
    print("\nNot accepted")
