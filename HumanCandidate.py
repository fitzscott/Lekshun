import Candidate as cnd

class HumanCandidate(cnd.Candidate):
    """
    Let the human try being a candidate for a change.
    """
    def assignalign(self, algns=None):
        if algns is not None:
            algnlst = algns
            self.alignments.clear()
        else:
            algnlst = self.alignments.alignments
        for algn in algnlst:
            prmpt = "Enter value ({0} to {1}) for alignment {2}: "\
                .format(self.minalgn, self.maxalgn, algn)
            val = int(input(prmpt))
            assert(val >= self.minalgn and val <= self.maxalgn)
            self.alignments.assign(algn, val)

    def allocall(self, cnt):
        for puidx in range(cnt-1):
            prmpt = "Remaining money {0}. How much for political unit {1}? "\
                .format(self.money, puidx+1)
            bucks = int(input(prmpt))
            self.allocate(puidx+1, bucks)
        self.allocate(cnt, self.money)

if __name__ == "__main__":
    hc = HumanCandidate("Hoomin Imposter")
    hc.assignalign(["flexibility", "morality", "finesse"])
    hc.money = 21
    hc.initapproval(6)
    hc.allocall(6)
    hc.penalizeunallocated(-2)
    print(hc)
