import string
import random

list = open("codes.txt", "a")
 
N = 7
L = 500

 
res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=N))
 
for i in range(L):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    list.write(res+"\n")
    print(res)


