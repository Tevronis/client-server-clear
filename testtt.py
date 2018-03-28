import sympy

with open("nastia.txt", 'w') as file:
    for item in sympy.primerange(2**10, 2**20):
        file.write(str(item) + '\n')
