class Cube:
    def __init__(self, n):
        self.cube_size = n
        self.Cube=self.create_cube()

    @property
    def cube_size(self):
        return self._cubeSize
    
    @cube_size.setter
    def cube_size(self,n):
        self._cubeSize=n


    def create_cube(self):
        n=self.cube_size
        n_size_cube={
            'F':[['G' for _ in range(n)] for _ in range(n)], # Front: Green
            'B':[['B' for _ in range(n)] for _ in range(n)], # Back: Blue
            'L':[['O' for _ in range(n)] for _ in range(n)], # Left: Orange
            'R':[['R' for _ in range(n)] for _ in range(n)], # Right: Red
            'T':[['W' for _ in range(n)] for _ in range(n)], # Top: White
            'D':[['Y' for _ in range(n)] for _ in range(n)], # Down: Yellow
        }
        return n_size_cube
    
    def print_cube(self):
        for i in self.Cube.items():
            print(self.Cube[i[0]])

    def cube_rotation(self, page):
        # selected page rotation
        act_page = self.Cube[page]
        layers = int(len(act_page) / 2)


        





