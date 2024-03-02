import argparse

parser = argparse.ArgumentParser(description = 'check if the number is prime or not')
parser.add_argument('n1', type = int, default = 1, help = 'number')

args = parser.parse_args()
number = args.n1

def is_prime(num):
    #even number
    if num % 2 == 0:
        print(f'{num} is not a prime')
        return False
    a = 3
    for i in range(num//2 - 1):
        if num % a == 0:
            print(f'{num} is not a prime')
            # print(f'{num} has a factor {a}')
            return False
        a += 2

    print(f'{num} is a prime')
    return True

is_prime(number)