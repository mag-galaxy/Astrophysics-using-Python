import argparse

parser = argparse.ArgumentParser(description = 'check if the number is a prime number or not')
parser.add_argument('n1', type = int, default = 1, help = 'number')

args = parser.parse_args()
number = args.n1

def is_prime(num):
    
    for i in range(2, num):
        if num % i == 0:
            print(f'{num} is not a prime number')
            # print(f'{num} has a factor {i}')
            return False

    print(f'{num} is a prime number')
    return True

is_prime(number)
