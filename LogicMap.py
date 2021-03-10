import copy

class LogicMap():
    def __init__(self,verticalMap=[],horizontalMap=[]) -> None:
        print('map formatting...')
        self.matrix=[]
        self.verticalMap=verticalMap
        self.horizontalMap=horizontalMap
        self.vertical=0
        self.horizontal=0
        self.SetMap(verticalMap,horizontalMap)
    def SetMap(self,verticalMap,horizontalMap) -> None:
        self.verticalMap=copy.copy(verticalMap)
        self.horizontalMap=copy.copy(horizontalMap)
        self.matrix=[]
        self.vertical=len(self.verticalMap)
        self.horizontal=len(self.horizontalMap)
        for i in range(self.vertical*self.horizontal):
            self.matrix.append(-1)
        print(self.vertical,' * ',self.horizontal,' matrix created')
    def GetVerticalMap(self,num):
        return self.verticalMap[num]
    def GetHorizontalMap(self,num):
        return self.horizontalMap[num]
    def Show(self) -> None:
        for i in range(self.vertical):
            for j in range(self.horizontal):
                val=self.matrix[i*self.vertical+j]
                mark='/'
                if val==1:
                    mark='■'
                elif val==0:
                    mark='□'
                print(mark,end='')
            print()
    def SetDot(self,vertical,horizontal,val) -> None:
        self.matrix[vertical*self.vertical+horizontal]=val
    def GetDot(self,vertical,horizontal) -> int:
        return self.matrix[vertical*self.vertical+horizontal]
    def GetVerticalLine(self,num):
        return self.matrix[num::self.horizontal]
    def GetHorizontalLine(self,num):
        return self.matrix[(num*self.horizontal):((self.horizontal)+(num*self.horizontal))]
    def SetVerticalLine(self,num,val) -> int:
        for i in range(len(val)):
            self.matrix[i*self.horizontal+num]=val[i]
    def SetHorizontalLine(self,num,val) -> int:
        for i in range(len(val)):
            self.matrix[i+num*self.horizontal]=val[i]