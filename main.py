from cube import Cube


c=Cube(3)
# print(c.CubeSize)
# c.Print_Cube()

probaDict={'p':[[0,1,2],[3,4,5],[6,7,8]]}

for _ in probaDict['p']:
    print(_)    

result=c.CubeRotation(probaDict['p'], 'p')

print()
for _ in result:
    print(_)  




# szamlalo=0
# for _ in range(6):
#     for i in range(c.CubeSize):
#         for j in range(c.CubeSize):
#             print(c.Cube[szamlalo], end='')
#             szamlalo+=1
#         print(end='\n')
#     print(end='\n')
