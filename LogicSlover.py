import copy
import LogicMap

def Slove(logicMap:LogicMap):
    for i in range(logicMap.horizontal):
        map=logicMap.GetHorizontalMap(i)
        lineArray=logicMap.GetHorizontalLine(i)
        SloveLine(map,lineArray)
        logicMap.SetHorizontalLine(i,lineArray)

#p1 分解(+不要部切り落とし)
#p2 埋める位置の計算処理
#p3 チェック処理
def SloveLine(map,lineArray):
    lineFragment=SloveLine_WasteCut(map,lineArray)
    SloveLine_ShiftStack(lineFragment.editMap,lineFragment.lineArray)
    lineFragment.OverWrite(lineArray)

class LineFragment():
    def __init__(self,headNum,editMap,lineArray) -> None:
        self.hedNum=headNum
        self.lineArray=lineArray
        self.editMap=editMap
    def OverWrite(self,lineArray):
        for i,d in enumerate(self.lineArray):
            lineArray[self.hedNum+i]=d

#-----------------------------------------------------------------------------------------------------------------------
#配列の確定している部分を切り取る
#-----------------------------------------------------------------------------------------------------------------------
def SloveLine_WasteCut(map,lineArray):
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
    return LineFragment(top,editMap,editArray)


#-----------------------------------------------------------------------------------------------------------------------
#ずらして埋める
#-----------------------------------------------------------------------------------------------------------------------
def SloveLine_ShiftStack(map,lineArray):
    #埋める場所、開ける場所
    pointFull=[]
    pointEmpty=[]
    #端に寄せたときに重なる位置を推定する
    pointHead=[]
    pointTail=[]
    SloveLine_ShiftStack_prosses1(map,lineArray,pointHead,pointEmpty)    #左または上から詰めた場合
    SloveLine_ShiftStack_prosses2(map,lineArray,pointTail,pointEmpty)    #右または下から詰めた場合

    n=len(lineArray)
    for i in range(len(lineArray)):
        if lineArray[i]==1:
            if pointHead[0]>i and pointTail[-1]>=i:
                pointTail[-1]=i
            break
    for i in range(len(lineArray)):
        nn=n-(i+1)
        if lineArray[nn]==1:
            if pointHead[-1]<nn and pointTail[0]<=nn:
                pointHead[-1]=nn
            break
    
    for i in range(len(pointHead)):                           #結果の整理
        p=pointTail[-(i+1)]
        g=pointHead[i]
        while p<=g:
            pointFull.append(p)
            p+=1
            
    for d in pointFull:
        lineArray[d]=1
    for d in pointEmpty:
        lineArray[d]=0

#手前から詰めていった時の位置を推定する
def SloveLine_ShiftStack_prosses1(map,lineArray,pointArray,emptyArray):
    head=0
    for i in range(len(map)):
        count=0
        while True:    #連続で埋められるマスをカウントする
            if lineArray[head]==0:
                count=0
            else:
                count+=1
            head+=1    #1マス進める
            if count>=map[i]:    #範囲を確保できたら
                if i==0 and lineArray[head]==1:    #特殊処理
                    emptyArray.append(head-map[i])
                else:       #ループ抜けして次の値へ
                    head-=1    #塗りつぶし位置にする
                    break
        pointArray.append(head)
        head+=2    #隣のマス+1マス開ける
#奥から詰めていった時の位置を推定する
def SloveLine_ShiftStack_prosses2(map,lineArray,pointArray,emptyArray):
    _pointArray=[]
    _emptyArray=[]
    SloveLine_ShiftStack_prosses1(list(reversed(map)),list(reversed(lineArray)),_pointArray,_emptyArray)
    n=len(lineArray)
    for d in _pointArray:
        pointArray.append(n-d-1)
    for d in _emptyArray:
        emptyArray.append(n-d-1)
#-----------------------------------------------------------------------------------------------------------------------
#斜線を入れられる場所を探す
#-----------------------------------------------------------------------------------------------------------------------
def SloveLine_FindEmptyZone(map,lineArray):
    #1,-1,1時に繋げたらオーバーする場合
    #最大値と同数の1のつながりを見つけたとき
    #それよりも端に確保できない1郡が必要個数になっていた時
    #1の配置的に絶対にその区域に1が来ることが無いとき
    pass

#-----------------------------------------------------------------------------------------------------------------------
#
#-----------------------------------------------------------------------------------------------------------------------
SloveLine([1,3,3,1],[0,1,0,0,1,-1,-1,-1,-1,-1,-1,1,0,0,1,0])