import copy
import LogicMap

#イラストロジックを解く
def Solver(logicMap:LogicMap,debug=False):
    #データの整形
    horizontal=[]
    Vertical=[]
    for i in range(logicMap.horizontal):
        horizontal.append([LineFragment(0,logicMap.GetHorizontalMap(i),logicMap.GetHorizontalLine(i))])
    for i in range(logicMap.vertical):
        Vertical.append([LineFragment(0,logicMap.GetVerticalMap(i),logicMap.GetVerticalLine(i))])
    lineFragments=[horizontal,Vertical]

    #ここからロジックを解く
    loop=[True,True]
    direction=0     #縦に読むか横に読むか
    while loop[0] or loop [1]:    #縦横両方が変化なしの場合ループ解除
        loop[direction]=False
        if debug:
            if direction ==0:
                print('縦方向を計算します')
            else:
                print('横方向を計算します')
            
        for i,d in enumerate(lineFragments[direction]):
            #読み出し処理
            if direction == 0:
                array=logicMap.GetHorizontalLine(i)
            else:
                array=logicMap.GetVerticalLine(i)
            if debug:
                print('\n',i,' 列目 :',array)
            _array=copy.copy(array)     #処理前値の保存
            for j in range(len(d)):
                d[j].Read(array)        #最新の値の読み出し
                if debug:
                    d[j].Show()
            #計算処理
            d=LineFragmentsSplit(d)     #配列の分割
            for j in range(len(d)):     #計算処理
                dd=d[j]
                if debug:
                    d[j].Show(start='    ')
                d[j]=SloveLine(d[j])
                if debug:
                    d[j].Show(start='     - > ')
            #書き込み処理
            for n in range(len(array)): #上書き準備
                if array[n]==-1:
                    array[n]=-2         #マスを-2で初期化
            for dd in d:
                dd.Write(array)         #初期化したマスに書き込み
            for n in range(len(array)):
                if array[n]==-2:        #上書きされていない->1では無いところなので0にする
                    array[n]=0
            if array!=_array:           #値が変化していたら
                loop[direction]=True
                if direction ==0:       #マップに反映
                    logicMap.SetHorizontalLine(i,array)
                else:
                    logicMap.SetVerticalLine(i,array)
        direction=(direction+1)%2       #行列入れ替え

#行（または列）ごとの処理
def SloveLine(_lineFragment):
    lineFragment=WasteCut(_lineFragment.editMap,_lineFragment.lineArray,_lineFragment.headNum)      #両端の確定している不要部分のカット
    if len(lineFragment.lineArray)==0:      #分割されたマスの数が0だった場合何もしない
        return lineFragment
    if len(lineFragment.editMap)==0:    #黒塗りの場所がない場合（空の場合）に全て0にする
        for i in range(len(lineFragment.lineArray)):
            lineFragment.lineArray[i]=0
        return lineFragment
    #計算処理
    confirmArea,possibleArea=PossibleArea(lineFragment.editMap,lineFragment.lineArray)
    SloveLine__Process1(lineFragment.editMap,lineFragment.lineArray,confirmArea)
    SloveLine_Process2(lineFragment.editMap,lineFragment.lineArray,possibleArea)
    return lineFragment


#-----------------------------------------------------------------------------------------------------------------------
#行（または列）をより細かくしたもの
#-----------------------------------------------------------------------------------------------------------------------
#マスを分割可能な範囲ごとに分割したもの
class LineFragment():
    def __init__(self,headNum,editMap,lineArray) -> None:
        self.headNum=headNum        #分割した列の先頭位置
        self.lineArray=lineArray    #マス情報
        self.editMap=editMap        #数字の情報
    def Write(self,lineArray):      #マスに書き込み
        for i,d in enumerate(self.lineArray):
            if lineArray[self.headNum+i]>-1 and lineArray[self.headNum+i]!=d:
                print('error')
            lineArray[self.headNum+i]=d
    def Read(self,lineArray):       #マスから読み込み
        for i,d in enumerate(self.lineArray):
            self.lineArray[i]=lineArray[self.headNum+i]
    def Show(self,start='',end='\n'):
        print(start,'head:',self.headNum,'size:',len(self.lineArray),'map:',self.editMap,'array:',self.lineArray,end=end)

#マスの分割
def LineFragmentSplit(lineFragment):
    s=0
    newLineFragment=[]
    _,possibleArea=PossibleArea(lineFragment.editMap,lineFragment.lineArray)
    if len(possibleArea)==0:    #処理する必要が無い場合
        newLineFragment.append(LineFragment(0,editMap=[],lineArray=[]))
        return newLineFragment
    #計算処理
    headNum=lineFragment.headNum+possibleArea[0][0]     #先頭位置
    for i in range(len(possibleArea)):
        if i+1<len(possibleArea):                       #分割可能な場所があったら
            if possibleArea[i][1]+1<possibleArea[i+1][0]:
                map=lineFragment.editMap[s:i+1]
                lineArray=lineFragment.lineArray[possibleArea[s][0]:possibleArea[i][1]+1]
                newLineFragment.append(LineFragment(headNum,editMap=map,lineArray=lineArray))
                s=i+1
                headNum=lineFragment.headNum+possibleArea[s][0]
    if 0<len(possibleArea):                             #余ったものを最後に追加する
        map=lineFragment.editMap[s:]
        lineArray=lineFragment.lineArray[possibleArea[s][0]:possibleArea[-1][1]+1]
        newLineFragment.append(LineFragment(headNum,editMap=map,lineArray=lineArray))
    return newLineFragment

#マス群の配列の分割
def LineFragmentsSplit(lineFragments):
    newLineFragments=[]
    for d in lineFragments:
        for dd in LineFragmentSplit(d):
            if -1 in dd.lineArray:    #まだ不定部分が存在する場合
                newLineFragments.append(dd)
    return newLineFragments

#-----------------------------------------------------------------------------------------------------------------------
#配列の両端の確定している部分を切り取る
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
#穴埋め処理系
#-----------------------------------------------------------------------------------------------------------------------

#Process1
#ずらして重なった部分を埋める
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

#端から詰めていった時の位置を推定する
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

#両端から詰めていった時の重なった部分を推定する
#    戻り値: confirmArea    数字ごとの確定で黒く塗れるエリア 
#    　　　  possibleArea   数字ごとの黒に塗られうるエリア
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
    #端っこは確定できる部分が多いため追加で処理を行う
    if len(confirmArea)>0: 
        for i in range(confirmArea[0][0]):
            if lineArray[i]==1:                                #端の数より手前に1がある場合そこから塗るようにする     [5]  ??1?????? -> ??111????
                confirmArea[0][0]=i
                for j in range(map[0]):
                    if i+j==n or lineArray[i+j+1]==0:          #上の場合かつ先に0がある場合、ありうる領域を再計算     [5]  ??111?0??
                        possibleArea[0][1]=(i+j)
                        if i+j-(map[0]-1)<confirmArea[0][0]:   #上の場合かつ先に0がある場合、確定できる領域を再計算   [5]  ??111?0?? -> ?1111?0??
                            confirmArea[0][0]=i+j-(map[0]-1)
                        break
                break
        for i in range(n-confirmArea[-1][1]):       #上と同じ処理を反対でも行う
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



#Process2
#白塗り部分を推定
def SloveLine_Process2(map,lineArray,possibleArea):
    #データの整理
    dotZone=[]                                          #点がある地点を線として求める
    i=0
    n=len(lineArray)
    while i < n:
        if lineArray[i]==1:                             #1になっている領域を見つけたら
            s=i                                         #スタート地点の記憶
            while i+1 < n and lineArray[i+1]==1:
                i+=1
            possible=[]
            for j,d in enumerate(possibleArea):         #どの数字の一部がありうるか
                if d[0]<=s and i<=d[1]:
                    possible.append(j)
            dotZone.append({'position':[s,i],'size':i-s+1,'possibleArea':possible})     #連続する1の　位置、連結数、どの数字の一部か
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

    #0確定の位置の推定
    nn=len(dotZone)-1
    for i,d in enumerate(dotZone):
        if len(d['possibleArea'])==1:
            #線が確定したとき両端を0とする
            if d['size']==map[d['possibleArea'][0]]:
                if 0<d['position'][0]:
                    lineArray[d['position'][0]-1]=0
                if d['position'][1]<n-1:
                    lineArray[d['position'][1]+1]=0
            #1の配置的に絶対にその区域に1が来ることが無いとき両端から0で埋める
            if i==0 or not(d['possibleArea'][0] in dotZone[i-1]['position']):
                for j in range(possibleArea[d['possibleArea'][0]][0],d['position'][1]-map[d['possibleArea'][0]]+1):
                    if d['possibleArea'][0]==0 or possibleArea[d['possibleArea'][0]-1][1]<j:
                        lineArray[j]=0
            if i==nn or not(d['possibleArea'][0] in dotZone[i+1]['position']):
                for j in range(d['position'][0]+map[d['possibleArea'][0]],possibleArea[d['possibleArea'][0]][1]+1):
                    if d['possibleArea'][-1]==(len(possibleArea)-1) or possibleArea[d['possibleArea'][0]+1][0]>j:
                        lineArray[j]=0
    #1マス空いた線同士を繋げたらオーバーする場合、間を0とする
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