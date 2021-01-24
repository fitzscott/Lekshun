import Alignment as algn
import random


def rolldice(num, sides=6):
    tot = 0
    for _ in range(num):
        tot += random.randint(1, sides)
    return (tot)


class Candidate():
    """
    Candidate represents a political candidate.
    A candidate has:
        Positions, represented as numerical scores for alignments.
        Funds it can allocate to political units to curry favor in that unit.
        Good (or ill) will accumulated in political units.
    """

    def __init__(self, nm, algnstrs=None, minalgn=1, maxalgn=6):
        self._name = nm
        self._money = 0
        self._allocs = {}
        # Why is this a list while allocations are a dictionary? Kicks.
        self._approval = []
        self._unitvals = []
        self._alignments = algn.Alignment(algnstrs, minalgn, maxalgn)
        self._score = None
        self._totalvotes = 0
        self._minalgn = minalgn
        self._maxalgn = maxalgn
        self._offsets = []

    def __str__(self):
        retstr = "Name: {0}".format(self._name)
        retstr += "\n" + str(self._alignments)
        # for alloc in sorted(self._allocs.keys()):
        #     retstr += "\n\tAllocation {0} = {1}".format(alloc,
        #                                                 self._allocs[alloc])
        retstr += "\nAllocations  " + "\t".join([str(self._allocs[alkey])
                                    for alkey in self._allocs.keys()])
        # for nu in range(len(self._approval)):
        #     retstr += "\n\tApproval {0} = {1}".format(nu+1,
        #                                                self._approval[nu])
        retstr += "\nApproval     " + "\t".join([str(appr) for appr in self._approval])
        retstr += "\nPolitical unit values = {0}".format(self._unitvals)
        return (retstr)

    @property
    def money(self):
        return (self._money)

    @money.setter
    def money(self, bucks):
        self._money = bucks

    @property
    def alignments(self):
        return (self._alignments)

    @property
    def allocations(self):
        return (self._allocs)

    @property
    def approval(self):
        return (self._approval)

    @property
    def unitvalues(self):
        return (self._unitvals)

    @unitvalues.setter
    def unitvalues(self, val):
        self._unitvals = val

    @property
    def score(self):
        return (self._score)

    @property
    def totalvotes(self):
        return (self._totalvotes)

    @totalvotes.setter
    def totalvotes(self, val):
        self._totalvotes = val

    @property
    def minalgn(self):
        return (self._minalgn)

    @property
    def maxalgn(self):
        return (self._maxalgn)

    @property
    def offsets(self):
        return (self._offsets)

    @offsets.setter
    def offsets(self, polalgns):
        # print(str(polalgns))
        # print(str(self._alignments.alignments))
        self._offsets = [polalgns[idx].compare(self._alignments)
                         for idx in range(len(polalgns))]
        # print(str(self._offsets))

    def enddisp(self):
        dispstr = """{0}
        \t\tPolitical unit votes: {1}
        \t\tTotal votes: {2}
        """.format(self, ", ".join([str(sc) for sc in self._score]),
                   str(self._totalvotes))
        # dispstr = str(self) + "\n\t\t" +\
        #           ", ".join([str(sc) for sc in self._score]) +\
        #           "\n\t\tTotal votes: " + str(self.totalvotes)
        return (dispstr)

    def allocate(self, puid, bucks):
        assert (bucks <= self._money)
        self._allocs[puid] = bucks
        self._money -= bucks

    def allocrest(self):
        minpuid = min(self._allocs.keys())
        maxpuid = max(self._allocs.keys())
        if minpuid != 1:    # missing 1st political unit
            self.allocate(1, self._money)
        else:
            for puid in sorted(self._allocs.keys()):
                if puid == 1:
                    prevpuid = puid
                    continue
                else:
                    if puid != prevpuid + 1:
                        # We have skipped prevpuid + 1, so assign it
                        self.allocate(prevpuid + 1, self._money)
                        break
                    prevpuid = puid
        if self._money > 0:
            self.allocate(maxpuid + 1, self._money)

    def resetalloc(self, maxid=None):
        if maxid is not None:
            valz = [x+1 for x in range(maxid)]
        else:
            valz = self._allocs.keys()
        for val in valz:
            self._allocs[val] = 0

    def allocall(self, cnt):
        pass

    def initapproval(self, numpu):
        for _ in range(numpu):
            self._approval.append(0)

    def creditapproval(self, pu, cred):
        assert(pu > 0 and pu <= len(self._approval))
        self._approval[pu-1] += cred

    def penalizeunallocated(self, penalty=-1):
        for pu in self._allocs.keys():
            if self._allocs[pu] <= 0:
                self.creditapproval(pu, penalty)

    def assignalign(self, algns=None):
        pass

    def calcscore(self):
        self._score = [rolldice(appr) for appr in self._approval]
        # print(str(self._score))

if __name__ == "__main__":
    c = Candidate("Bob Roberts", ["honesty", "intelligence", "goofballitude"])
    c.money = 21
    # c.allocate(1, 2)
    # c.allocate(2, 3)
    # c.allocate(4, 4)
    # c.allocate(5, 5)
    # c.allocate(6, 2)
    # c.allocate(5, 2)
    # c.allocate(2, 3)
    # c.allocate(4, 4)
    # c.allocate(3, 5)
    # c.allocate(1, 2)
    # c.allocate(1, 7)
    # print(c)
    # c.allocrest()
    # print(c)
    c.resetalloc(6)
    c.allocate(2, 3)
    c.allocate(4, 4)
    c.allocate(3, 5)
    c.allocate(1, 2)
    c.allocate(5, 7)
    c.initapproval(6)
    c.penalizeunallocated()
    c.creditapproval(2, 3)
    c.unitvalues = [1,2,3,4,5,6]
    print(c)
