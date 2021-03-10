import sys #command args
import LogicMap
import LogicSlover

def main():
    vmap=[[2],[0],[2]]
    hmap=[[1,1],[1,1],[0]]
    map=LogicMap.LogicMap(verticalMap=vmap,horizontalMap=hmap)
    LogicSlover.Slove(map)
    map.Show()

if __name__ == '__main__':
    main()