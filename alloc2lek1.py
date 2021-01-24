import random

def rolldice(num, sides=6):
    tot = 0
    for _ in range(num):
        tot += random.randint(1, sides)
    return (tot)

class alloc2lek1():
    """
    Allocate funds to a variety of geographic areas to win their
    electoral votes.
    """

    def __init__(self, numgeo, numplay):
        self._geocnt = numgeo
        self._plyrcnt = numplay
        self._geovotes = []
        self._plyrfun = []
        self._plyralloc = []
        self._plyrimpact = []
        self._plyrscor = [0 for _ in range(numplay)]
        self._money = 0
        for i in range(self._geocnt):
            self._money += i+1

    def setupgeo(self, base=10):
        for g in range(self._geocnt):
            self._geovotes.append(base * (g+1))
        print(str(self._geovotes))

    def allocstraight(self):
        return ([x+1 for x in range(self._geocnt)])

    def allocrand(self):
        tot = 0
        alloc = []
        for i in range(self._geocnt-1):
            amt = random.randint(0, self._geocnt)
            if tot + amt >= self._money:
                amt = self._money - tot
            tot += amt
            alloc.append(amt)
        alloc.append(max(0, self._money - tot))
        return (alloc)

    def allocnearstraight(self, var=1):
        tot = 0
        alloc = []
        for i in range(self._geocnt-1):
            amt = max(0, random.randint(-1 * var, var) + i + 1)
            if tot + amt >= self._money:
                amt = self._money - tot
            tot += amt
            alloc.append(amt)
        alloc.append(max(0, self._money - tot))
        return (alloc)

    def allocfromuser(self):
        tot = 0
        print("Allocations can be from 0 to as much money as you have.")
        alloc = [0 for _ in range(self._geocnt)]
        for i in range(self._geocnt-1):
            prmpt = "Enter allocation for area w/ {0} votes: ".format(self._geovotes[i])
            amt = int(input(prmpt))
            if tot + amt >= self._money:
                print("You spent too much! You are under arrest!")
                amt = self._money - tot
            tot += amt
            alloc[i] = amt
        alloc[self._geocnt-1] = max(0, self._money - tot)
        return (alloc)

    def mkplyrz(self):
        # Start w/ 1 straight, 2 random, 1 near-straight
        # self._plyrfun = [self.allocstraight, self.allocrand, self.allocrand,
        #                  self.allocnearstraight]
        # self._plyrfun = [self.allocstraight for _ in range(self._plyrcnt)]
        # self._plyrfun = [self.allocnearstraight for _ in range(self._plyrcnt)]
        self._plyrfun = [self.allocfromuser, self.allocstraight,
                         self.allocrand, self.allocnearstraight]
        for fun in self._plyrfun:
            self._plyralloc.append(fun())
        print(str(self._plyralloc))

    def resolvealloc(self, roll=False):
        if roll:        # impact is dice rolls for allocation
            for plnum in range(self._plyrcnt):
                self._plyrimpact.append([rolldice(alloc)
                                         for alloc in self._plyralloc[plnum]])
            print(str(self._plyrimpact))
        else:           # impact is allocation
            self._plyrimpact = self._plyralloc
        for geo in range(self._geocnt):
            print("\t\tGeo #{0}".format(geo))
            winscor = -1
            winrz = []
            # Determine winning bid
            for plnum in range(self._plyrcnt):
                if self._plyrimpact[plnum][geo] > winscor:
                    winscor = self._plyrimpact[plnum][geo]
            # Find all players who made the winning bid
            for plnum in range(self._plyrcnt):
                if self._plyrimpact[plnum][geo] == winscor:
                    winrz.append(plnum)
            for winr in winrz:
                # Divide proceeds evenly for ties
                award = self._geovotes[geo] / len(winrz)
                print("Player {0} wins {1}".format(winr, award))
                self._plyrscor[winr] += award
        print("_"*40)

    def printscorz(self):
        for plyrnum in range(self._plyrcnt):
            print("Player {0} scored {1}".format(plyrnum,
                                                 self._plyrscor[plyrnum]))

if __name__ == "__main__":
    for num in range(5):
        print(str(rolldice(num+1)))
    a2l = alloc2lek1(6, 4)
    a2l.setupgeo()
    # print(str(a2l.allocstraight()))
    # for _ in range(10):
    #     print(str(a2l.allocnearstraight()))
    a2l.mkplyrz()
    a2l.resolvealloc(True)
    a2l.printscorz()
