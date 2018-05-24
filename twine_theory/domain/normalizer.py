from twine_theory.domain import twine_theory as twine

def kseq_dir(k1,k2):
    if k1.low < k2.low and k1.high < k2.high: return 'up'
    elif k1.low > k2.low and k1.high > k2.high: return 'down'
    return 'inclusion'

def kseq_type(k1,k2,k3):
    if k1.low <= k2.low and k1.high<=k2.high and \
       k2.low <= k3.low and k2.high<=k3.high: return 'up'
    elif k1.low >= k2.low and k1.high>=k2.high and \
       k2.low >= k3.low and k2.high>=k3.high: return 'down'
    elif k1.low<k2.low and k1.high<k2.high and \
       k2.low > k3.low and k2.high>k3.high: return 'top'        
    elif k1.low>k2.low and k1.high>k2.high and \
       k2.low < k3.low and k2.high<k3.high: return 'bottom'
    return 'unnormalized'



def kseq_merge(k1,k2,isUp):
    if isUp:
        return twine.K(k2.time,k1.start,max(k1.high,k2.high),k2.end,max(k1.low,k2.low),k1.volume+k2.volume)
    return twine.K(k2.time,k1.start,min(k1.high,k2.high),k2.end,min(k1.low,k2.low),k1.volume+k2.volume)

class Normalizer():
    def __init__(self):
        self.log = []
        pass

    def normalize(self,ksequence):
        normalizedK = [ksequence[0]]
        dir = 'up'
        for i in range(1,len(ksequence)):
            ndir = kseq_dir(normalizedK[-1],ksequence[i])
            if ndir=='inclusion':
                normalizedK[-1] = kseq_merge(normalizedK[-1],ksequence[i],dir=='up')
            else:
                normalizedK.append(ksequence[i])
                dir = ndir
                                   
        return normalizedK
                             
                             
