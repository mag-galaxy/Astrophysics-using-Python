# M = m + 5 - 5*log(d) , d (pc) is distance from Earth to the target.

m = 18.2
M = -4.1
d = 10**((m - M + 5) / 5.0)
print(f'distance from Earth to Andromeda: {d}pc')
