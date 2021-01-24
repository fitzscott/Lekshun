import random
import math
import Alignment as algn

class PoliticalUnit():
    """
    PoliticalUnit represents a single division of an overall political
    body, e.g. a province or state within a nation, or a county or
    district within a state.
    """
    def __init__(self, id, votes, minalgn=1, maxalgn=6):
        self._id = id
        self._votes = votes
        self._algn = None
        self._minalgn = minalgn
        self._maxalgn = maxalgn

    @property
    def id(self):
        return (self._id)

    @property
    def votes(self):
        return (self._votes)

    @property
    def algn(self):
        return (self._algn)

    @property
    def alignments(self):
        return (self._algn.alignments)

    def __str__(self):
        retstr = "ID: {0}, vote count: {1}".format(self._id, self._votes)
        retstr += "\t" + str(self._algn)
        return (retstr)

    def randomalignments(self, algns=None):
        self._algn = algn.Alignment(algns, self._minalgn, self._maxalgn)
        self._algn.randassgn(algns)


if __name__ == "__main__":
    pu = PoliticalUnit(1, 5)
    # pu.alignments["fiscal"] = -1
    # pu.alignments["social"] = 2
    # pu.alignments["control"] = 0
    pu.randomalignments()
    print(pu)
