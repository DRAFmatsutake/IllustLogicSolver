import copy
import LogicMap

def Slover(logicMap:LogicMap,debug=False):
    #データの整理
    horizontal=[]
    Vertical=[]
    for i in range(logicMap.horizontal):
        horizontal.append([LineFragment(0,logicMap.GetHorizontalMap(i),logicMap.GetHorizontalLine(i))])
    for i in range(logicMap.vertical):
        Vertical.append([LineFragment(0,logicMap.GetVerticalMap(i),logicMap.GetVerticalLine(i))])
    lineFragments=[horizontal,Vertical]
    loop=[True,True]
    direction=0
    while loop[0] or loop [1]:
        loop[direction]=False
        if debug:
            if direction ==0:
                print('縦方向を計算します')
            else:
                print('横方向を計算します')
        for i in range(len(lineFragments[direction])):
            if direction ==0:
                array=logicMap.GetHorizontalLine(i)
            else:
                array=logicMap.GetVerticalLine(i)
            if debug:
                #input()
                print(i,' 列目 :',array)
            _array=copy.copy(array)
            for d in lineFragments[direction][i]:
                d.Read(array)
                if debug:# or (direction==0 and i==12):
                    d.Show()
            lineFragments[direction][i]=LineFragmentsSplit(lineFragments[direction][i])
            for j in range(len(lineFragments[direction][i])):
                if debug:
                    print('    ',end='')
                    lineFragments[direction][i][j].Show()
                lineFragments[direction][i][j]=SloveLine(lineFragments[direction][i][j])
                if debug:
                    print('     - > ',end='')
                    lineFragments[direction][i][j].Show()
            for n in range(len(array)):
                if array[n]==-1:
                    array[n]=-2
            for d in lineFragments[direction][i]:
                d.Write(array)
            for n in range(len(array)):
                if array[n]==-2:
                    array[n]=0
            if array!=_array:
                loop[direction]=True
                if direction ==0:
                    logicMap.SetHorizontalLine(i,array)
                else:
                    logicMap.SetVerticalLine(i,array)
        direction=(direction+1)%2


def SloveLine(_lineFragment):
    lineFragment=WasteCut(_lineFragment.editMap,_lineFragment.lineArray,_lineFragment.headNum)
    if len(lineFragment.lineArray)==0:
        return lineFragment
    if len(lineFragment.editMap)==0:
        for i in range(len(lineFragment.lineArray)):
            lineFragment.lineArray[i]=0
        return lineFragment
    confirmArea,possibleArea=PossibleArea(lineFragment.editMap,lineFragment.lineArray)
    SloveLine__Process1(lineFragment.editMap,lineFragment.lineArray,confirmArea)
    SloveLine_Process2(lineFragment.editMap,lineFragment.lineArray,possibleArea)
    return lineFragment

class LineFragment():
    def __init__(self,headNum,editMap,lineArray) -> None:
        self.headNum=headNum
        self.lineArray=lineArray
        self.editMap=editMap
    def Write(self,lineArray):
        for i,d in enumerate(self.lineArray):
            if lineArray[self.headNum+i]>-1 and lineArray[self.headNum+i]!=d:
                print('error')
            lineArray[self.headNum+i]=d
    def Read(self,lineArray):
        for i,d in enumerate(self.lineArray):
            self.lineArray[i]=lineArray[self.headNum+i]
    def Show(self,end='\n'):
        print('head:',self.headNum,'size:',len(self.lineArray),'map:',self.editMap,'array:',self.lineArray,end=end)


def LineFragmentSplit(lineFragment):
    s=0
    newLineFragment=[]
    _,possibleArea=PossibleArea(lineFragment.editMap,lineFragment.lineArray)
    if len(possibleArea)==0:
        newLineFragment.append(LineFragment(0,editMap=[],lineArray=[]))
        return newLineFragment
    headNum=lineFragment.headNum+possibleArea[0][0]
    for i in range(len(possibleArea)):
        if i+1<len(possibleArea):
            if possibleArea[i][1]+1<possibleArea[i+1][0]:
                map=lineFragment.editMap[s:i+1]
                lineArray=lineFragment.lineArray[possibleArea[s][0]:possibleArea[i][1]+1]
                newLineFragment.append(LineFragment(headNum,editMap=map,lineArray=lineArray))
                s=i+1
                headNum=lineFragment.headNum+possibleArea[s][0]
    if 0<len(possibleArea):
        map=lineFragment.editMap[s:]
        lineArray=lineFragment.lineArray[possibleArea[s][0]:possibleArea[-1][1]+1]
        newLineFragment.append(LineFragment(headNum,editMap=map,lineArray=lineArray))
    return newLineFragment

def LineFragmentsSplit(lineFragments):
    newLineFragments=[]
    for d in lineFragments:
        for dd in LineFragmentSplit(d):
            if -1 in dd.lineArray:
                newLineFragments.append(dd)
    return newLineFragments

#-----------------------------------------------------------------------------------------------------------------------
#配列の確定している部分を切り取る
#-----------------------------------------------------------------------------------------------------------------------
def WasteCut(map,lineArray,headNum):
    editMap=copy.copy(map)
    top=0
    flug=False
    #確定している先頭部分の消去
    for i in range(len(lineArray)):
        if lineArray[i]==0:
            top=i+1
            if flug:
                editMap.pop(0)
                flug=False
        elif lineArray[i]==1:
            flug=True
        else:
            break
    #確定している後方部分の消去
    bottom=len(lineArray)
    flug=False
    for i in range(len(lineArray)):
        if lineArray[-(i+1)]==0:
            bottom=len(lineArray)-(i+1)
            if flug:
                editMap.pop(-1)
                flug=False
        elif lineArray[-(i+1)]==1:
            flug=True
        else:
            break
    if bottom==-1:
        editArray=[]
    else:
        editArray=lineArray[top:bottom]
    return LineFragment(headNum+top,editMap,editArray)
#-----------------------------------------------------------------------------------------------------------------------
#ずらして埋める
#-----------------------------------------------------------------------------------------------------------------------
def SloveLine__Process1(map,lineArray,confirmArea):

    #[3] 010000→011000にする（端っこの黒から塗るようにする）
    n=len(lineArray)
    for i in range(len(lineArray)):
        if lineArray[i]==1:
            if confirmArea[0][0]>i and confirmArea[0][1]>=i:
                confirmArea[0][0]=i
            break
    for i in range(len(lineArray)):
        nn=n-(i+1)
        if lineArray[nn]==1:
            if confirmArea[-1][1]<nn and confirmArea[-1][0]<=nn:
                confirmArea[-1][1]=nn
            break
    
    for d in confirmArea:                           #結果の反映
        p=d[0]
        while p<=d[1]:
            lineArray[p]=1
            p+=1

#手前から詰めていった時の位置を推定する
def DotBring(map,lineArray):
    head=0
    pointTops=[]
    pointBottoms=[]
    for i in range(len(map)):
        count=0
        while True:    #連続で埋められるマスをカウントする
            if lineArray[head]==0:
                count=0
            else:
                count+=1
            if count>=map[i]:    #範囲を確保できたら
                if 0<i or head+1==len(lineArray) or lineArray[head+1]!=1:
                    break
            head+=1    #1マス進める
        pointTops.append(head-(map[i]-1))
        pointBottoms.append(head)
        head+=2    #1マス進める+1つ離す
    return pointTops,pointBottoms

#奥から詰めていった時の位置を推定する
def PossibleArea(map,lineArray):
    confirmArea=[]
    possibleArea=[]
    _placeTops,_placeBottoms=DotBring(map,lineArray)
    __placeTops,__placeBottoms=DotBring(list(reversed(map)),list(reversed(lineArray)))
    n=len(lineArray)-1
    for i in range(len(__placeTops)):
        __placeTops[i]=n-__placeTops[i]
        __placeBottoms[i]=n-__placeBottoms[i]
    for i in range(len(_placeTops)):
        confirmArea.append([__placeBottoms[-(1+i)],_placeBottoms[i]])
        possibleArea.append([_placeTops[i],__placeTops[-(1+i)]])
    #端っこは特定の条件下だと確定できるので
    if len(confirmArea)>0: 
        for i in range(confirmArea[0][0]):
            if lineArray[i]==1:
                confirmArea[0][0]=i
                for j in range(map[0]):
                    if i+j==n or lineArray[i+j+1]==0:
                        possibleArea[0][1]=(i+j)
                        if i+j-(map[0]-1)<confirmArea[0][0]:
                            confirmArea[0][0]=i+j-(map[0]-1)
                        break
                break
        for i in range(n-confirmArea[-1][1]):
            if lineArray[-(1+i)]==1:
                confirmArea[-1][1]=n-i
                for j in range(map[-1]):
                    if i+j==n or lineArray[-(i+j+1)]==0:
                        possibleArea[-1][0]=n-(i+j)
                        if n-(i+j)+(map[-1]-1)>confirmArea[-1][1]:
                            confirmArea[-1][1]=n-(i+j)+(map[-1]-1)
                        break
                break
    return confirmArea,possibleArea
#-----------------------------------------------------------------------------------------------------------------------
#斜線を入れられる場所を探す
#-----------------------------------------------------------------------------------------------------------------------
def SloveLine_Process2(map,lineArray,possibleArea):
    dotZone=[]
    #点がある地点を線として求める
    i=0
    n=len(lineArray)
    while i < n:
        if lineArray[i]==1:     #1になっている領域を見つけたら
            s=i        #領域を求める
            while i+1 < n and lineArray[i+1]==1:
                i+=1
            possible=[]
            for j,d in enumerate(possibleArea):
                if d[0]<=s and i<=d[1]:
                    possible.append(j)
            dotZone.append({'position':[s,i],'size':i-s+1,'possibleArea':possible})
        i+=1
    #繋ぐことができる線と線を繋げる
    pre=[]
    for d in dotZone:
        if len(pre)!=0 and len(d['possibleArea'])==1 and d['possibleArea'] == pre[-1]['possibleArea']:
            for i in range(pre[-1]["position"][1],d["position"][0]):
                lineArray[i]=1
            pre[-1]["position"][1]=d["position"][1]
            pre[-1]['size']=pre[-1]["position"][1]-pre[-1]["position"][0]+1
        else:
            pre.append(d)
    dotZone=pre

    nn=len(dotZone)-1
    for i,d in enumerate(dotZone):
        #線が確定したとき両端を空ける
        if len(d['possibleArea'])==1:
            if d['size']==map[d['possibleArea'][0]]:
                if 0<d['position'][0]:
                    lineArray[d['position'][0]-1]=0
                if d['position'][1]<n-1:
                    lineArray[d['position'][1]+1]=0
            #1の配置的に絶対にその区域に1が来ることが無いとき
            if i==0 or not(d['possibleArea'][0] in dotZone[i-1]['position']):
                for j in range(possibleArea[d['possibleArea'][0]][0],d['position'][1]-map[d['possibleArea'][0]]+1):
                    if d['possibleArea'][0]==0 or possibleArea[d['possibleArea'][0]-1][1]<j:
                        lineArray[j]=0
            if i==nn or not(d['possibleArea'][0] in dotZone[i+1]['position']):
                for j in range(d['position'][0]+map[d['possibleArea'][0]],possibleArea[d['possibleArea'][0]][1]+1):
                    if d['possibleArea'][-1]==(len(possibleArea)-1) or possibleArea[d['possibleArea'][0]+1][0]>j:
                        lineArray[j]=0
    #1,-1,1時に繋げたらオーバーする場合
    for i in range(len(dotZone)):
        if i!=0 and dotZone[i]['position'][0]==dotZone[i-1]['position'][1]+2:
            mixsize = dotZone[i]['size']+dotZone[i-1]['size']+1
            over = True
            for d in map:
                if mixsize<=d:
                    over=False
                    break
            if over:
                lineArray[dotZone[i]['position'][0]-1]=0

#-----------------------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------------------
#a=LineFragment(0,[3],[-1, 0, 1, -1, -1])
#a=LineFragment(0,[3],[-1, -1, 1, 0, -1])
#print(PossibleArea(a.editMap,a.lineArray))
# for d in a:
#     d.Show()