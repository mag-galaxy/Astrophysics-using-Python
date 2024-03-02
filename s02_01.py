def is_prime(num):
    #even number
    if num % 2 == 0:
        print(f'{num} is not a prime number')
        return False
    a = 3
    for i in range(num//2 - 1):
        if num % a == 0:
            print(f'{num} is not a prime number')
            # print(f'{num} has a factor {a}')
            return False
        a += 2

    print(f'{num} is a prime number')
    return True

is_prime(131071)
