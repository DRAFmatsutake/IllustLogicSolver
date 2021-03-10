import copy
import LogicMap

def Slove(logicMap:LogicMap):
    for i in range(logicMap.horizontal):
        map=logicMap.GetHorizontalMap(i)
        lineArray=logicMap.GetHorizontalLine(i)
        SloveLine(map,lineArray)
        logicMap.SetHorizontalLine(i,lineArray)


def SloveLine(map,lineArray):

    editMap,editArray,top=SloveLine_process1(map,lineArray)

    pointEmpty=[]
    pointFull=[]
    
    #端に寄せたときに重なる位置を推定する
    pointHead=[]
    pointTail=[]
    SloveLine_process2(editMap,editArray,pointHead,pointEmpty)    #左または上から詰めた場合
    SloveLine_process3(editMap,editArray,pointTail,pointEmpty)    #右または下から詰めた場合
    for i in range(len(pointHead)):                           #結果の整理
        p=pointTail[-(i+1)]
        g=pointHead[i]
        while p<=g:
            pointFull.append(p)
            p+=1
            
    for d in pointFull:
        editArray[d]=1
    for d in pointEmpty:
        editArray[d]=0
        
    for i,d in enumerate(editArray):
        lineArray[top+i]=d


#配列の確定している部分を切り取る
def SloveLine_process1(map,lineArray):
    editMap=copy.copy(map)
    top=0
    flug=False
    #確定している先頭部分の消去
    for i in range(len(lineArray)):
        if lineArray[i]==0:
            if flug:
                editMap.pop(0)
                flug=False
        elif lineArray[i]==1:
            flug=True
        else:
            top=i
            break
    #確定している後方部分の消去
    bottom=len(lineArray)
    flug=False
    for i in range(len(lineArray)):
        if lineArray[-(i+1)]==0:
            if flug:
                editMap.pop(-1)
                flug=False
        elif lineArray[-(i+1)]==1:
            flug=True
        else:
            bottom=len(lineArray)-i
            break

    editArray=lineArray[top:bottom]
    return editMap,editArray,top

#手前から詰めていった時の位置を推定する
def SloveLine_process2(map,lineArray,pointArray,emptyArray):
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
def SloveLine_process3(map,lineArray,pointArray,emptyArray):
    _pointArray=[]
    _emptyArray=[]
    SloveLine_process2(list(reversed(map)),list(reversed(lineArray)),_pointArray,_emptyArray)
    n=len(lineArray)
    for d in _pointArray:
        pointArray.append(n-d-1)
    for d in _emptyArray:
        emptyArray.append(n-d-1)

SloveLine([2,2,2],[0,1,1,0,-1,-1,-1,0,0,0,1,1,0,0])