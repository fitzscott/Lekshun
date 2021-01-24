import MachineCandidate as mc
import random

class RandPropAllocMachineCandidate(mc.MachineCandidate):
    """
    RandPropAllocMachineCandidate - allocate funds in RandProportional to
    electoral value.
    """
    def allocall(self, cnt):
        # Allocate proportionally, but with random addition
        origmoney = self.money
        totvotes = sum(self.unitvalues)
        avgfund = self.money / totvotes
        for puidx in range(cnt-1):
            allocfund = max(min(int(avgfund * self.unitvalues[puidx]) +
                                cnt // 2 - random.randint(0, cnt),
                                self.money), 0)
            self.allocate(puidx + 1, allocfund)
        self.allocate(cnt, self.money)

    def assignalign(self, algns):
        """
        assignalign
        :param algns: dictionary with alignments & average values
        :return:
        """
        self.alignments.assignall(algns)

if __name__ == "__main__":
    rpamc = RandPropAllocMachineCandidate("Random Proportional Richard")
    rpamc.unitvalues = [1,2,3,4,5,6]
    rpamc.money = 21
    rpamc.allocall(6)
    print(rpamc)
