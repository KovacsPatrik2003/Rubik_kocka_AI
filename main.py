from cube import Cube


c=Cube(3)
print()
c.print_cube()

probaDict={'p':[[0,1,2],[3,4,5],[6,7,8]]}

for _ in probaDict['p']:
    print(_)


def rotate_face_counterclockwise(probaDict, face):
    n = 3
    new_face = [[probaDict[face][j][n - i - 1] for j in range(n)] for i in range(n)]
    probaDict[face] = new_face


rotate_face_counterclockwise(probaDict, 'p')
print()
for _ in probaDict['p']:
    print(_)