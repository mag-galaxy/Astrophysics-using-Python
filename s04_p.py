# t^2 / r^3
# p^2 / a^3
earth_a = 1 #au
earth_p = 1 #yr
jupiter_a = 5.2 #au
jupiter_p = ((earth_p**2) / (earth_a**3) * (jupiter_a**3))**(1/2)
print(f'orbital period of Jupiter = {jupiter_p} yr')