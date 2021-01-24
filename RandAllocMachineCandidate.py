import MachineCandidate as mc
import random

class RandAllocMachineCandidate(mc.MachineCandidate):
    """
    RandAllocMachineCandidate - allocate funds in Randortional to
    electoral value.
    """
    def allocall(self, cnt):
        # Allocate randomly
        origmoney = self.money
        for puidx in range(cnt-1):
            # allocfund = random.randint(0, self.money)
            allocfund = min(random.randint(0, origmoney // cnt + cnt // 2),
                            self.money)
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
    pamc = RandAllocMachineCandidate("Random Rita")
    pamc.money = 21
    pamc.allocall(6)
    print(pamc)
