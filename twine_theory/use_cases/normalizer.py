from twine_theory.domain import twine_theory as twine

class NormalizeUseCase():
    def __init__(self,ksequence):
        self._seq = ksequence
        
    def execute(self):
        self.kseq = twine.KSeq('day',self._seq)
        return self.kseq.getNorm()
