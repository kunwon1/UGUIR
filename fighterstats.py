from constants import *
from msgbox import msgBox
from spritesheet import getCorpseSprite
from dice import Dice

class Stats(object):
    def __init__(self, parent, hpRoll=10,
                 Str=12, Dex=12,
                 Con=12, Int=12,
                 Wis=12, Cha=12):

        self.parent = parent
        self.mbox = msgBox()
        self.dice = Dice()

        self.Str = Str
        self.Dex = Dex
        self.Con = Con
        self.Int = Int
        self.Wis = Wis
        self.Cha = Cha
        
        self.baseAttack = 2
        self.baseDefense = 2
        
        self.attackRoll
        
        self.hp = hpRoll + bonus[str(Con)]
        self.maxhp = self.hp

    def dmg(self):
        damage = self.dice.roll('1d6+' + str(bonus[str(self.Str)]))
#        damage = randint(1,6 + bonus[str(self.Str)])
        if damage < 1:
            damage = 1
        return damage

    def attackOther(self, other):
        if other.dead:
            return
        if self.parent.name == 'Player':
            self.parent.map.objectUpdateRequired = 1
        if self.attackRoll() >= other.stats.defenseRoll():
            self.doHit(other)
        else:
            pass        
        
    def attackRoll(self):
        return self.baseAttack + \
               bonus[str((self.Str + self.Dex) / 2)] + self.dice.roll('1d20')

    def defenseRoll(self):
        return self.baseDefense + bonus[str(self.Dex)] + self.dice.roll('1d20')

    def doHit(self, other):
        damage = self.dmg()
        other.stats.gotHit(self.parent, damage)
        if self.parent.name == 'Player':
            self.mbox.addMsg(
                'You hit %s for %i damage!' % (other.name, damage))
            self.mbox.addMsg(
                '%s hp: %i/%i' % (other.name,
                                  other.stats.hp,
                                  other.stats.maxhp))

    def gotHit(self, other, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        if self.parent.name == 'Player':
            self.mbox.addMsg(
                'You got hit for %i damage by %s' % (damage,other.name))
            self.mbox.addMsg(
                'Current hp: %i/%i' % (self.hp,self.maxhp))
        if self.hp == 0:
            self.gotKilled(other)

    def gotKilled(self, other):
        self.parent.dead = True
        self.parent.blocked = False
        self.parent.image = getCorpseSprite()
        if self.parent.name == 'Player':
            self.mbox.addMsg('You got killed by a %s!' % other.name)
