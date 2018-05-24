from twine_theory.domain import twine_theory as twine
from twine_theory.domain import normalizer as norm
class NormalizeUseCase():
    def __init__(self,ksequence):
        self.kseq = []
        for k in ksequence:
            self.kseq.append(twine.K(k['time'],k['start'],k['high'],k['end'],k['low'],k['volume']))
        
    def execute(self):
        n = norm.Normalizer()
        self.normalizedK = n.normalize(self.kseq)
        print(n.log)
        return self.normalizedK
