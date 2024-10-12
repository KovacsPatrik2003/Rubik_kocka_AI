from cube import Cube

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


c=Cube(3)
print()
# c.print_cube()

# probaDict={'p':[[0,1,2,3],[4,5,6,7],[8,9,10,11], [12,13,14,15]]}
#
# for _ in probaDict['p']:
#     print(_)
#
#
# def rotate_face_counterclockwise(probaDict, face):
#     n = 4
#     new_face = [[probaDict[face][j][n - i - 1] for j in range(n)] for i in range(n)]
#     probaDict[face] = new_face
#
#
# rotate_face_counterclockwise(probaDict, 'p')
# print()
# for _ in probaDict['p']:
#     print(_)

colors = {
            'R': 'red',
            'O': 'orange',
            'G': 'green',
            'B': 'blue',
            'W': 'white',
            'Y': 'yellow'
        }

def draw_square(ax, vertices, face, face_color):
    for i in range(3):
        for j in range(3):
            # Egy négyzet sarkainak koordinátái
            square = [
                [vertices[0][0] + i, vertices[0][1] + j, vertices[0][2]],
                [vertices[1][0] + i, vertices[1][1] + j, vertices[1][2]],
                [vertices[2][0] + i, vertices[2][1] + j, vertices[2][2]],
                [vertices[3][0] + i, vertices[3][1] + j, vertices[3][2]]
            ]
            # Négyzet hozzáadása a megfelelő színnel
            ax.add_collection3d(Poly3DCollection([square], color=face_color[face[i][j]], edgecolors='black'))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# A hat oldal rajzolása a megfelelő pozíciókba és irányba
size = 3

# Front
draw_square(ax, [[0, 0, 0], [0, size, 0], [size, size, 0], [size, 0, 0]], c.Cube['F'], colors)
# Back
draw_square(ax, [[0, 0, -size], [0, size, -size], [size, size, -size], [size, 0, -size]], c.Cube['B'], colors)
# Left
draw_square(ax, [[0, 0, 0], [0, size, 0], [0, size, -size], [0, 0, -size]], c.Cube['L'], colors)
# Right
draw_square(ax, [[size, 0, 0], [size, size, 0], [size, size, -size], [size, 0, -size]], c.Cube['R'], colors)
# Top
draw_square(ax, [[0, size, 0], [0, size, -size], [size, size, -size], [size, size, 0]], c.Cube['T'], colors)
# Bottom
draw_square(ax, [[0, 0, 0], [0, 0, -size], [size, 0, -size], [size, 0, 0]], c.Cube['D'], colors)

# Axes beállítása
ax.set_xlim([0, size])
ax.set_ylim([0, size])
ax.set_zlim([-size, size])

# Plot megjelenítése
plt.show()