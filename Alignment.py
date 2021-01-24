import random
import math


class Alignment():
    """
    Alignment - capture elements / factors / axes related to political
    identity.
    """
    def __init__(self, algnstr=None, minv=-2, maxv=2):
        if algnstr is None:
            self._alignments = {"fiscal": 0, "social": 0, "control": 0}
        else:
            self._alignments = {algn: 0 for algn in algnstr}
        self._minval = minv
        self._maxval = maxv

    @property
    def alignments(self):
        return (self._alignments)

    def __str__(self):
        # retstr = ""
        # for algn in self._alignments.keys():
        #     retstr += "\n\tAlignment " + algn + ": " + str(self._alignments[algn])
        retstr = "Alignments:  " + "\t".join([algn + ": " + str(self._alignments[algn])
                                             for algn in self._alignments.keys()])
        return (retstr)

    def clear(self):
        self._alignments = {}

    def assign(self, algn, val):
        if val < self._minval or val > self._maxval:
            print("Alignment value must be between {0} and {1}".format(self._minval,
                                                                       self._maxval))
            return (False)
        self._alignments[algn] = val
        return (True)

    def assignall(self, algns):
        self.clear()
        for alkey in algns.keys():
            self.assign(alkey, algns[alkey])

    def compare(self, otheralgn):
        diff = 0
        # print(str(self))
        # print(str(otheralgn))
        for algn in self._alignments.keys():
            # print("Comparing " + algn)
            diff += math.fabs(self._alignments[algn] -
                              otheralgn._alignments[algn])
        return (len(self._alignments.keys()) - diff)

    def randassgn(self, algns=None):
        if algns is not None:
            self._alignments = {}
            keyz = algns
        else:
            keyz = self._alignments.keys()
        for algn in keyz:
            # range from min to max, but weighted toward middle
            rng = self._maxval - self._minval
            val = int(math.sqrt(random.randint(0, rng ** 2)) + self._minval)
            self._alignments[algn] = val


if __name__ == "__main__":
    algn = Alignment()
    print(algn)
    algn.randassgn()
    print(algn)
