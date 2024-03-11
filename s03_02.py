import numpy as np

# generate 10^8 random numbers of standard Gaussion distribution
# using ".standard_normal()"
arr1 = np.random.standard_normal(10**8)
print(f'all numbers =\n{arr1}\n')

# calculate mean
arr_mean = np.mean(arr1)
print(f'mean = {arr_mean}')

# calculate standard deviation
arr_dev = np.std(arr1)
print(f'standard deviation = {arr_dev}')

# outside of range[m-3σ, m+3σ], using mask
arr_ceiling = arr_mean + 3 * arr_dev
arr_floor = arr_mean - 3 * arr_dev
arr_mask = (arr1 < arr_floor) | (arr1 > arr_ceiling)

# number of data that out of range
count = 0
for i in range(10**8):
  if(arr_mask[i]):
    count+=1

print(f'numbers out of [m-3σ, m+3σ] : {count} numbers')
print(f'numbers out of [m-3σ, m+3σ] : {count/10**6:.2f}%')