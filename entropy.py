import math

#Shannon Entropy -> minimum bits per symbol -> * message length = minimum bits needed to encode message
def InfoSize(st):
   stList = list(st)
   alphabet = list(set(stList))
   freqList = []
   for symbol in alphabet:
       ctr = 0
       for sym in stList:
           if sym == symbol:
               ctr += 1
       freqList.append(float(ctr) / len(stList))
   ent = 0.0
   for freq in freqList:
       ent = ent + freq * math.log(freq, 2)
   ent = -ent
   mbps = int(math.ceil(ent))
   return mbps*len(stList)

#Convert to base in list form, fix to 14 digits (by looping)
def numberToBase(n, b):
    if n == 0:
        digits=[0]
    else:
       digits = []
       while n:
           digits.append(int(n % b))
           n /= b
    while len(digits)<14:
       digits+=digits[0:14-len(digits)]
    return digits[::-1]
 
