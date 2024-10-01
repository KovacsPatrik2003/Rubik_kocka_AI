class Cube:
    def __init__(self, n):
        self.CubeSize = n
        self.Cube=self.CreateCube(self.CubeSize)

    @property
    def CubeSize(self):
        return self._cubeSize
    
    @CubeSize.setter
    def CubeSize(self,n):
        self._cubeSize=n

    def CreateCube(self, n):
        nSizeCube={
            'F':[['G' for j in range(n)] for i in range(n)], # Front: Green
            'B':[['B' for _ in range(n)] for _ in range(n)], # Back: Blue
            'L':[['O' for _ in range(n)] for _ in range(n)], # Left: Orange
            'R':[['R' for _ in range(n)] for _ in range(n)], # Right: Red
            'T':[['W' for _ in range(n)] for _ in range(n)], # Top: White
            'D':[['Y' for _ in range(n)] for _ in range(n)], # Down: Yellow        
        }
        # nSizeCube=""
        # szamlalo=-1
        # for i in range(6):
        #     for j in range(n):
        #         for k in range(n):
        #             szamlalo+=1
        #             if i==0:
        #                 nSizeCube+=str(szamlalo)
        #             elif i==1:
        #                 nSizeCube+='B'
        #             elif i==2:
        #                 nSizeCube+='O'
        #             elif i==3:
        #                 nSizeCube+='R'
        #             elif i==4:
        #                 nSizeCube+='w'
        #             elif i==5:
        #                 nSizeCube+='Y'
                        
        return nSizeCube
    
    def Print_Cube(self):
        for i in self.Cube.items():
            print(self.Cube[i[0]])
    
    def CubeRotation(self, proba, page):
        #selected page rotation
        thisPageNodes=list()
        for row in proba:
            for node in row:
                thisPageNodes.append(node)
        firstNode=thisPageNodes[0]
        variable=firstNode
        for i in range(len(thisPageNodes)-1):
            actualNode=variable
            nextNode=thisPageNodes[i+1]
            thisPageNodes[i+1]=actualNode
            variable=nextNode
        thisPageNodes[0]=variable


        # the front page rotation is done. remainder: have to return this list as a dictionary
        resultDict={page: []}
        counter=0
        helperList=list()
        for i in thisPageNodes:
            
            if counter%3!=0:
                helperList.append(i)
            
            else:
                helperList.append(i)
                resultDict[page].append(helperList)
                helperList=list()
            counter+=1
                

        return resultDict[page]


        





