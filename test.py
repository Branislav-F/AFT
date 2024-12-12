print("hello world")
#test 

#loop for generating random data and save it to tuples
import random   
data = []
for _ in range(10):
    tup = (random.randint(1, 100), random.random())
    data.append(tup)

print(data)
# commit from laptop
