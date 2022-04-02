from math import cos, sin
import random


def generate_population():
    return [[random.randint(0,1) for _ in range(ukuran_kromosom)] for _ in range (ukuran_populasi)]


def function(x,y):
    return (cos(x)+ sin(y))**2  / (x**2 + y**2)


def decode_process(kromosom, limit):
    sum_kali = 0
    sum_pembagi = 0
    for i in range(len(kromosom)):
        binary = kromosom[i]
        sum_kali += (binary * (2**-(i+1)))
        sum_pembagi += (2**-(i+1))

    return limit[0] + (((limit[1]-limit[0]) / sum_pembagi) * sum_kali)


def split_kromosom(kromosom):
    split = len(kromosom) // 2
    kromosom_1 = kromosom[:split]
    kromosom_2 = kromosom[split:]

    return kromosom_1, kromosom_2


def best_kromosom_selection(population):
    min_fitness = 999
    
    for kromosom in population: 
        kromosom_1, kromosom_2 = split_kromosom(kromosom)
        x = decode_process(kromosom_1, limit_x)
        y = decode_process(kromosom_2, limit_y)
        fitness = 1/(function(x, y)+0.1)

        if fitness < min_fitness: 
            min_fitness = fitness
            min_kromosom = kromosom
            x1 = x
            y1 = y 

    return min_kromosom, min_fitness, x1, y1


def roulette_wheel(population, fitness, fitness_total):
    r = random.random()
    i = 0
    while r > 0:
        r -= fitness[i]/fitness_total
        i += 1
        if i == len(population) - 1:
            break

    return population[i]


def crossover(parent1, parent2):
    child_1 = []
    child_2 = []
    children = []
    pc = random.random()

    if pc < prob_crossover:
        child_1[:1] = parent1[:1]
        child_1[1:] = parent2[1:]

        child_2[:1] = parent2[:1]
        child_2[1:] = parent1[1:]

        children.append(child_1)
        children.append(child_2)
    else: 
        children.append(parent1)
        children.append(parent2)

    return children


def mutation(child_1, child_2):
    for i in range(len(child_1)):
        pm = random.random()
        if pm < prob_mutasi:
            child_1[i] = random.randint(0,1)

        pm = random.random()
        if pm < prob_mutasi:
            child_2[i] = random.randint(0,1)

    return child_1, child_2


def elitisme(population, best_kromosom_generation, bad_kromosom, fitness_total):
    if best_kromosom_generation[1] < bad_kromosom[0] and best_kromosom_generation[0] not in population:
        population[bad_kromosom[2]] = best_kromosom_generation[0]
        fitness_total = fitness_total - bad_kromosom[0] + best_kromosom_generation[1]

        print("\nProses Elitisme")
        print(f"Kromosom Ke-{bad_kromosom[2]+1}: {bad_kromosom[1]}, fitness: {bad_kromosom[0]}")
        print(f"diubah ke {best_kromosom_generation[0]}, fitness: {best_kromosom_generation[1]}\n")

    return population, fitness_total

# inisialisasi variabel global
prob_mutasi = 0.2
prob_crossover = 0.8

limit_x = [-5, 5]
limit_y = [-5, 5]

ukuran_kromosom = 20
ukuran_populasi = 25
generasi = 100

# driver code
populasi = generate_population()
print("Populasi Awal:", populasi)

best_kromosom_generation = []

for gen in range(generasi):
    best_kromosom, bad_kromosom, fitness_data, new_population = [], [], [], [] 
    fitness_total, count_kromosom, index = 0, -999, 0

    print("Generasi", gen+1)

    for i, kromosom in enumerate(populasi): 
        kromosom_1, kromosom_2 = split_kromosom(kromosom)
        x = decode_process(kromosom_1, limit_x)
        y = decode_process(kromosom_2, limit_y)

        fitness_value = 1/(function(x, y)+0.1)  
        fitness_data.append(fitness_value)
        fitness_total += fitness_value  

        if gen != 0 and fitness_value > count_kromosom:
            count_kromosom = fitness_value 
            bad_kromosom = [fitness_value, kromosom, i]

    best_kromosom = best_kromosom_selection(populasi)

    print("Kromosom Terbaik:", best_kromosom[0])
    print("Fitness Terbaik:", best_kromosom[1])
    print()

    if gen != 0:
        best = sorted(best_kromosom_generation, key=lambda x: x[1])[0]
        populasi, fitness_total = elitisme(populasi, best, bad_kromosom, fitness_total)

    best_kromosom_generation.append(best_kromosom)  

    if gen != generasi-1:
        for i in range(ukuran_populasi // 2):
            parent_1 = roulette_wheel(populasi, fitness_data, fitness_total)
            parent_2 = roulette_wheel(populasi, fitness_data, fitness_total)

            children = crossover(parent_1, parent_2)
            child_1, child_2 = mutation(children[0], children[1])

            new_population.append(child_1)            
            new_population.append(child_2)            

        populasi = new_population

print() 
print('Kromosom Terbaik = ', best[0])
print('Phenotype x      = ', best[2])
print('Phenotype y      = ', best[3])
print('Nilai Fitness    = ', best[1])