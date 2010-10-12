from constants import bonus

from random import randint

class Stats(object):
    def __init__(self, hpRoll=10,
                 Str=12, Dex=12,
                 Con=12, Int=12,
                 Wis=12, Cha=12):

        self.Str = Str
        self.Dex = Dex
        self.Con = Con
        self.Int = Int
        self.Wis = Wis
        self.Cha = Cha
        
        self.dmg = lambda: randint(1,6) + bonus[str(Str)]
        
        self.hp = hpRoll + bonus[str(Con)]
        self.maxhp = self.hp
