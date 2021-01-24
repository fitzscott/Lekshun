import PoliticalUnit as pu
import HumanCandidate as hc
import RandAllocMachineCandidate as ramc
import RandPropAllocMachineCandidate as rpamc
import random


class Campaign():
    """
    Campaign - Candidates manipulate their alignments and spend money to
    gain approval from sub-units of the body politic.
    """
    def __init__(self, pu=6, cand=4, bucks=21, algns=["a", "b", "c"]):
        self._numpolunits = pu
        self._numcand = cand
        self._moneypercand = bucks
        self._alignments = algns
        self._candidates = []
        self._polunits = []
        self._roundbonus = [2, 3, 5]
        self._minalgn = 1
        self._maxalgn = 6

    @property
    def candidates(self):
        return (self._candidates)

    @property
    def numpoliticalunits(self):
        return (self._numpolunits)

    @property
    def politicalunits(self):
        return (self._polunits)

    @property
    def politicalunitsvotes(self):
        return (self._polunitvotes)

    @property
    def politicalunitsavgalignment(self):
        avgalgn = {}
        for algn in self._alignments:
            # print("Averaging alignment " + algn)
            sumval = 0
            for polu in self._polunits:
                # print("  Adding {0}".format(polu.alignments[algn]))
                sumval += polu.alignments[algn]
            # print("    Dividing by {0}".format(self._numpolunits))
            # avgalgn[algn] = sumval // self._numpolunits
            avgalgn[algn] = round(sumval / self._numpolunits)
        return (avgalgn)

    def setuppoliticalunits(self, numunits, votes=None, rand=False):
        if votes is None:
            if not rand:
                votes = [(v+1) * 10 for v in range(numunits)]
            else:
                votes = [random.randint(10, numunits * 10)
                         for _ in range(numunits)]
        # print(str(votes))
        for uidx in range(numunits):
            polunit = pu.PoliticalUnit(uidx+1, votes[uidx])
            polunit.randomalignments(self._alignments)
            self._polunits.append(polunit)

    def setupcandidates(self, inclhuman=False):
        candtypes = [ramc.RandAllocMachineCandidate,
                     rpamc.RandPropAllocMachineCandidate]
        polunitvotes = [pv.votes for pv in self._polunits]
        polalgns = [self._polunits[idx].algn
                    for idx in range(len(self._polunits))]
        avgaligns = self.politicalunitsavgalignment
        print(str(avgaligns))
        if inclhuman:
            hoomin = hc.HumanCandidate("Human Player", None, self._minalgn,
                                       self._maxalgn)
            hoomin.initapproval(self._numpolunits)
            hoomin.unitvalues = polunitvotes
            hoomin.assignalign(self._alignments)
            hoomin.offsets = polalgns
            # hoomin.allocall(self._numpolunits)
            self._candidates.append(hoomin)
        plcnt = len(self._candidates)
        while plcnt < self._numcand:
            plnm = "Computer Player {0}".format(plcnt+1)
            seltyp = candtypes[random.randint(0, len(candtypes)-1)]
            cand = seltyp(plnm, self._alignments, self._minalgn,
                          self._maxalgn)
            cand.initapproval(self._numpolunits)
            cand.unitvalues = polunitvotes
            cand.assignalign(avgaligns)
            cand.offsets = polalgns
            # cand.allocall(self._numpolunits)
            self._candidates.append(cand)
            plcnt += 1

    def evalallocs(self, round=0):
        for polu in self._polunits:
            print(polu)
        for plyr in self._candidates:
            plyr.money = self._moneypercand
            plyr.allocall(self._numpolunits)
        for poluidx in range(len(self._polunits)):
            highestbid = -1
            bestcandidate = []
            for candidx in range(len(self._candidates)):
                cand = self._candidates[candidx]
                candbid = cand.allocations[poluidx+1]
                # candalgn = cand.alignments
                # offset = self._polunits[poluidx].algn.compare(candalgn)
                offset = cand.offsets[poluidx]
                # print("offset = {0}".format(offset))
                candbid += offset
                # print("bid = {0}".format(candbid))
                if candbid >= highestbid:
                    if candbid == highestbid:
                        bestcandidate.append(candidx)
                    else:
                        bestcandidate = [candidx]
                        highestbid = candbid
                # print("highest = {0}, best = {1}".format(highestbid, bestcandidate))
            print("Unit {0} best candidates: {1}".format(poluidx+1, bestcandidate))
            for bc in bestcandidate:
                self._candidates[bc].creditapproval(poluidx+1,
                                                    self._roundbonus[round])
        for cand in self._candidates:
            cand.penalizeunallocated(-1 * (round+1))    # or maybe just -1?

    def finalscore(self):
        for cand in self._candidates:
            cand.calcscore()
        for poluidx in range(len(self._polunits)):
            bestscore = -1
            winnerz = []
            for candidx in range(len(self._candidates)):
                candscor = self._candidates[candidx].score[poluidx]
                if candscor >= bestscore:
                    if candscor == bestscore:
                        winnerz.append(candidx)
                    else:
                        winnerz = [candidx]
                        bestscore = candscor
            # print(str(winnerz))
            for winr in winnerz:
                self._candidates[winr].totalvotes +=\
                    self._polunits[poluidx].votes // len(winnerz)


if __name__ == "__main__":
    # c = Campaign(6, 4, 21, ["fiscal", "social", "military"])
    # c = Campaign(3, 3, 6, ["fiscal", "social", "military"])
    c = Campaign(6, 4, 21, ["fiscal", "social", "military"])
    c.setuppoliticalunits(c.numpoliticalunits, None, True)
    for polu in c.politicalunits:
        print(polu)
    c.setupcandidates(True)
    for rnd in range(3):
        c.evalallocs(rnd)
        for cand in c.candidates:
            print(cand)
        print("_"*30 + "\n")
    c.finalscore()
    for cand in c.candidates:
        print(cand.enddisp())
