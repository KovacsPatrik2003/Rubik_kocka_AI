class Cube:
    def __init__(self, n):
        self.n = n
        self.Cube=self.create_cube()

    @property
    def n(self):
        return self._cubeSize
    
    @n.setter
    def n(self, n):
        self._cubeSize=n


    def create_cube(self):
        n=self.n
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
        for face, grid in self.Cube.items():
            print(f"{face} face:")
            for row in grid:
                print(" ".join(row))
            print()

    def rotate_face_counterclockwise(self, face):
        n = self.n
        new_face = [[self.Cube[face][j][n - i - 1] for j in range(n)] for i in range(n)]
        self.Cube[face] = new_face

    def rotate_page(self, face):
        self.rotate_face_counterclockwise(face)
        # Update adjacent faces (this is a simplified example for the 'F' face)
        n = self.n
        if face == 'F':
            top = self.Cube['T'][-1]
            self.Cube['T'][-1] = [self.Cube['R'][i][0] for i in range(n)]
            for i in range(n):
                self.Cube['R'][i][0] = self.Cube['D'][0][n - 1 - i]
            self.Cube['D'][0] = [self.Cube['L'][i][-1] for i in range(n)]
            for i in range(n):
                self.Cube['L'][i][-1] = top[n - 1 - i]

        elif face == 'B':
            top = self.Cube['T'][0]
            self.Cube['T'][0] = [self.Cube['L'][i][0] for i in range(n)]
            for i in range(n):
                self.Cube['L'][i][0] = self.Cube['D'][-1][n - 1 - i]
            self.Cube['D'][-1] = [self.Cube['R'][i][-1] for i in range(n)]
            for i in range(n):
                self.Cube['R'][i][-1] = top[n - 1 - i]

        elif face == 'L':
            top = [self.Cube['T'][i][0] for i in range(n)]
            for i in range(n):
                self.Cube['T'][i][0] = self.Cube['F'][i][0]
                self.Cube['F'][i][0] = self.Cube['D'][i][0]
                self.Cube['D'][i][0] = self.Cube['B'][n - 1 - i][-1]
                self.Cube['B'][n - 1 - i][-1] = top[i]

        elif face == 'R':
            top = [self.Cube['T'][i][-1] for i in range(n)]
            for i in range(n):
                self.Cube['T'][i][-1] = self.Cube['B'][n - 1 - i][0]
                self.Cube['B'][n - 1 - i][0] = self.Cube['D'][i][-1]
                self.Cube['D'][i][-1] = self.Cube['F'][i][-1]
                self.Cube['F'][i][-1] = top[i]

        elif face == 'T':
            front = self.Cube['F'][0]
            self.Cube['F'][0] = [self.Cube['R'][0][i] for i in range(n)]
            for i in range(n):
                self.Cube['R'][0][i] = self.Cube['B'][0][n - 1 - i]
            self.Cube['B'][0] = [self.Cube['L'][0][i] for i in range(n)]
            for i in range(n):
                self.Cube['L'][0][i] = front[n - 1 - i]

        elif face == 'D':
            front = self.Cube['F'][-1]
            self.Cube['F'][-1] = [self.Cube['L'][-1][i] for i in range(n)]
            for i in range(n):
                self.Cube['L'][-1][i] = self.Cube['B'][-1][n - 1 - i]
            self.Cube['B'][-1] = [self.Cube['R'][-1][i] for i in range(n)]
            for i in range(n):
                self.Cube['R'][-1][i] = front[n - 1 - i]


        





