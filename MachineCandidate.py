import Candidate as cnd

class MachineCandidate(cnd.Candidate):
    """
    MachineCandidate - basic functionality for an automated candidate
    """
    def __init__(self, nm, algns=None, almin=-2, almax=2):
        super().__init__(nm, algns, almin, almax)

    def allocall(self, cnt):
        # Allocate same funds to each political unit, roughly..
        avgfund = self.money // cnt
        for pu in range(cnt - 1):
            self.allocate(pu+1, avgfund)
        self.allocrest()

    def assignalign(self, algns=None):
        self.alignments.randassgn(algns, self.minalgn, self.maxalgn)

if __name__ == "__main__":
    mc = MachineCandidate("Borg Rorgerts")
    mc.money = 21
    mc.assignalign({"strength": 18, "dexterity": 11, "wisdom": 7})
    mc.allocall(6)
    print(mc)
