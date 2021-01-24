import MachineCandidate as mc

class PropAllocMachineCandidate(mc.MachineCandidate):
    """
    PropAllocMachineCandidate - allocate funds in proportional to
    electoral value.
    """
    def allocall(self, cnt):
        # Allocate proportionally to vote count in unit values
        totvotes = sum(self.unitvalues)
        avgfund = self.money / totvotes
        for puidx in range(cnt-1):
            allocfund = int(avgfund * self.unitvalues[puidx])
            self.allocate(puidx + 1, allocfund)
        self.allocrest()

if __name__ == "__main__":
    pamc = PropAllocMachineCandidate("Reasonable Rhonda")
    pamc.unitvalues = [1,2,3,4,5,6]
    pamc.money = 36
    pamc.allocall(len(pamc.unitvalues))
    print(pamc)
