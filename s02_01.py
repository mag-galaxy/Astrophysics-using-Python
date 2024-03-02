def is_prime(num):
    
    for i in range(2, num):
        if num % i == 0:
            print(f'{num} is not a prime number')
            # print(f'{num} has a factor {i}')
            return False

    print(f'{num} is a prime number')
    return True

is_prime(131071)
