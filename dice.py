import random, re, os
from time import time

class Dice(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Dice, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        seed = int(time()) * os.getpid()
        self.seed = seed
        random.seed(seed)
        self.diceRegex = re.compile('(\d+)d(\d+)([+-]?)(\d+)?', re.I)

    def roll(self, diceSpecString):
        mod = None
        matchObj = self.diceRegex.match(diceSpecString)
        plusOrMinus = matchObj.group(3)
        modifier = matchObj.group(4)
        if not (plusOrMinus is None or modifier is None):
            mod = int(str(plusOrMinus) + str(modifier))
        numDice = int(matchObj.group(1))
        numSides = int(matchObj.group(2))
        
        total = 0
        
        for x in range(numDice):
            i = random.randint(1,numSides)
            total += i
        if mod is not None:
            total += mod
        return total

if __name__ == '__main__':
    from time import clock

    d = Dice()
    t1 = clock()

    for x in ['1d2','1d6','1d8','1d10','1d20','1d100','1d20+20','1d20+100',
              '6d20', '20d20', '10000d10', '1d100+100', '1d1000+1000',
              '1d10000']:
        print 'rolling %s: ' % x + str(d.roll(x))
        
    t2 = clock()
    t3 = t2 - t1
    print '%f seconds elapsed' % t3
        