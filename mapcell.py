from constants import *

class MapCell:
    def __init__(self, pos, batch,
                 group, blockedByTerrain=True,
                 blockedByObject=False, visible=True,
                 discovered=False):
        self.blockedByTerrain = blockedByTerrain
        self.blockedByObject = blockedByObject
        self.visible = visible
        self.discovered = discovered
        self.batch = batch
        self.group = group
        self.pos = pos
        self.xPx = self.pos.x * SPRITE_SIZE
        self.yPx = self.pos.y * SPRITE_SIZE
        self.type = DUNGEON_WALL
        self.objects = []

    def checkDoorPlacement(self, gameMap):
        for r in gameMap.rooms:
            if r.checkPointIntersect(self.pos):
                return False

        iterPos = Position(self.pos.x,self.pos.y)
        results = []
        topResult = self.checkCell(gameMap, iterPos.moveUp())
        results.append(self.checkCell(gameMap, iterPos.moveRight()))
        rightResult = self.checkCell(gameMap, iterPos.moveDown())
        results.append(self.checkCell(gameMap, iterPos.moveDown()))
        bottomResult = self.checkCell(gameMap, iterPos.moveLeft())
        results.append(self.checkCell(gameMap, iterPos.moveLeft()))
        leftResult = self.checkCell(gameMap, iterPos.moveUp())
        results.append(self.checkCell(gameMap, iterPos.moveUp()))

        if topResult == DUNGEON_DOOR and bottomResult == DUNGEON_WALL:
            return True
        if bottomResult == DUNGEON_DOOR and topResult == DUNGEON_WALL:
            return True
        if leftResult == DUNGEON_DOOR and rightResult == DUNGEON_WALL:
            return True
        if rightResult == DUNGEON_DOOR and leftResult == DUNGEON_WALL:
            return True 

        if not topResult == DUNGEON_WALL \
        and not bottomResult == DUNGEON_WALL:
            if not leftResult == DUNGEON_WALL \
            and not rightResult == DUNGEON_WALL:
                return False
        
        results.append(topResult)
        results.append(bottomResult)
        results.append(leftResult)
        results.append(rightResult)
        
        found = [0,0,0,0] 
        for i in results:
            found[i] += 1

        if found[DUNGEON_FLOOR] > 1:
            if found[DUNGEON_WALL] > 2:
                return True
        return False

    def checkCell(self, gameMap, pos):
        try:
            cell = gameMap.getCellAtPos(pos)
        except IndexError:
            return OUT_OF_BOUNDS
        return cell.type