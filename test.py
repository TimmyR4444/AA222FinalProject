from Gavl_code import Gavl
import numpy as np
from numpy import random
import time
import matplotlib.pyplot as plt

ga = Gavl.Gavl() # Initialize

start_time = time.time()
# Attractions
# 
# 0: Astro Orbiter
# 1: Barnstormer
# 2: Big Thunder
# 3: Buzz
# 4: Dumbo
# 5: Tales with Belle
# 6: Haunted Mansion
# 7: Small World
# 8: Jungle Cruise
# 9: Mad Tea Party
# 10: Magic Carpets
# 11: Winnie the Pooh
# 12: Philharmagic
# 13: Laugh Floor
# 14: Peter Pan
# 15: Pirates
# 16: Seven Dwarves
# 17: Space Mountain
# 18: Tomorrowland Speedway
# 19: PeopleMover
# 20: Under the Sea
# 21: Carousel of Progress
# 22: Hall of Presidents
# 23: Treehouse
# 24: Tom Sawyer
# 25: Splash Mountain / Tiana's Bayou Adventure
# 26: Lunch
# 27: Dinner
# 28: Snack
# 29: Dessert

# Ride times (in minutes)
ride_times = [2, 2, 7, 5, 2, 20, 10, 14, 8, 2, 2, 4, 3, 15, 3, 8, 3, 3, 4, 10, 7, 21, 23, 13, 40, 11]

# Nominal wait time at each hour (in minutes)
wait_time = {
    0: (10,20,35,35,30,30,30,30,35,25,35,30,25),
    1: (5,10,15,20,15,20,20,20,20,25,25,20,10),
    2: (15,20,35,45,40,35,35,40,30,30,30,30,20),
    3: (10,20,40,40,55,45,40,35,35,40,35,25,15),
    4: (10,10,10,15,10,15,15,15,15,25,20,15,15),
    5: (15,15,15,15,20,25,30,25,25,20,25,20,15),
    6: (15,20,45,50,45,45,50,45,45,45,40,35,30),
    7: (10,10,25,30,30,30,30,30,25,20,20,20,5),
    8: (25,35,55,55,40,35,40,60,50,50,50,40,25),
    9: (5,5,10,15,10,10,15,15,15,10,10,10,10),
    10: (10,10,15,15,15,20,20,30,30,20,15,10,10),
    11: (15,30,30,35,40,35,40,40,40,40,40,40,25),
    12: (10,15,15,15,15,15,15,15,15,15,15,15,15),
    13: (15,10,10,10,10,10,15,20,15,15,10,10,10),
    14: (45,45,60,65,70,75,70,75,70,70,70,60,60),
    15: (5,20,45,50,45,40,40,40,40,35,30,25,15),
    16: (35,45,85,80,85,120,120,120,80,80,80,80,70),
    17: (20,60,65,80,55,75,75,70,65,60,60,70,60),
    18: (10,20,20,20,15,20,20,20,20,25,20,20,5),
    19: (10,5,10,15,15,25,20,15,15,20,20,10,10),
    20: (10,5,15,30,30,25,25,25,35,30,30,20,10),
    21: (5,5,5,5,5,5,5,5,5,5,5,5,5),
    22: (10,10,10,10,10,10,10,10,10,10,10,10,10),
    23: (0,0,0,0,0,0,0,0,0,0,0,0,0),
    24: (10,10,10,10,10,10,10,10,10,10,10,10,10),
    25: (25,35,55,55,40,35,40,60,50,50,50,40,25)
}

# Wait times sampled from normal distribution centered at nominal time
for j in range(len(wait_time)):
    new_waits = []
    for i in range(len(wait_time[j])):
        original_wait = wait_time[j][i]
        new_wait_std_dev = original_wait / 10
        new_wait = np.random.normal(original_wait, new_wait_std_dev)

        new_waits.append(new_wait)
    wait_time[j] = new_waits


# Land Categories
adventure_frontier = [8,10,15,23,2,24,25]
liberty_fantasy = [1,4,5,6,7,9,11,12,14,16,20,22]
tomorrow = [0,3,13,17,18,19,21]

# Ride scores
scores_nominal = [5.6,6.3,9.36,7.54,7.37,7.63,9.3,7.3,7.83,7.4,5.6,8.37,8.14,8.45,8.4,9.0,8.49,9.13,5.3,9,8.22,8.37,7.24,6.1,6.73,9.7]

# Normalized ride scores
low_score = min(scores_nominal)
high_score = max(scores_nominal)
new_min = 1
new_max = 10
scores = []
for score in scores_nominal:
    new_score = (score-low_score)/(high_score-low_score) * (new_max-new_min) + new_min
    scores.append(new_score)

# Definition of the fitness:
# The fitness function receives the chromosome, which is a list with the genes. It must return the fitness value (number).
def fun_fitness(chromosome):
    fitness = 0  # Cumulative fitness
    prev_land = 0
    count = 0
    walk_coefficient = 2
    if (isValidDay(chromosome)):
        for ride in chromosome:
            if (ride == 26 or ride == 27):
                fitness += 10
            elif (ride == 28 or ride == 29):
                fitness += 7
            else:
                curr_land = land(ride)

                if (count == 0):
                    walk_penalty = 0
                else:
                    walk_penalty = walk_coefficient * abs(curr_land - prev_land)
                
                fitness += (scores[ride] - walk_penalty)
                prev_land = curr_land
            
            count += 1
    else:
        fitness = 0
    return fitness

def land(ride):
    if (ride in adventure_frontier):
        return 0
    if (ride in liberty_fantasy):
        return 1
    elif (ride in tomorrow):
        return 2

# Function that checks if all of the rides fit in one day
def isValidDay(chromosome):
    max_time = 720      #last ride must start by the max time (12 hours)
    curr_time = 0
    last_land = 0
    count = 0
    lunch = 0
    dinner = 0
    for ride in chromosome:
        if (ride == 26):
            if (curr_time < 120 or curr_time > 300):
                return False
            lunch += 1
            curr_time += 45
        elif (ride == 27):
            if (curr_time < 480 or curr_time > 630):
                return False
            dinner += 1
            curr_time += 60
        elif (ride == 28):
            if (lunch == 0 or dinner == 1):
                return False
            curr_time += 20
        elif (ride == 29):
            if (dinner == 0):
                return False
            curr_time += 20
        else:
            # Wait time
            curr_ride = ride
            curr_hour = round(curr_time/60)
            curr_wait= wait_time[curr_ride][curr_hour]
            
            # Walking time
            curr_land = land(ride)
            if (count == 0):
                walk_time = 7       # Takes about 7 minutes to walk to each land from entrance
            else:
                land_diff = abs(curr_land - last_land)
                if (land_diff == 0):
                    walk_time = 3
                elif (land_diff == 1):
                    walk_time = 7
                else:
                    walk_time = 10

            # Ride time
            ride_time = ride_times[ride]

            curr_time += (curr_wait + walk_time + ride_time)
            if (curr_time >= max_time):
                return False
            last_land = curr_land
        
        count += 1
    
    if (lunch == 1 and dinner == 1):
        return True
    else:
        return False

pop_size = 20000
min_length = 15
max_length = len(ride_times) + 4
max_generations = 10
fitness_goal = 128

ga.set_hyperparameter('size_population', pop_size)  # Set the size of the population
ga.set_hyperparameter('min_length_chromosome', min_length)  # Set the minimum length of the itinerary
ga.set_hyperparameter('max_length_chromosome', max_length)  # Set the maximum length of the itinerary to the total number of rides


ga.set_hyperparameter('fitness', fun_fitness)  # Set the fitness function

# Definition of the values that the genes can take
possible_genes = [i for i in range(max_length)]

ga.set_hyperparameter('possible_genes',
                      possible_genes)  # The possible values that the genes can take are the items' names

# Set other parameters
#ga.set_hyperparameter('termination_criteria', {'max_num_generation_reached': max_generations})  # Set the termination criteria to maximum number of generations (in this case 30 generations).
ga.set_hyperparameter('termination_criteria', {'goal_fitness_reached': fitness_goal}) # Set the termination criteria to fitness goal
ga.set_hyperparameter('repeated_genes_allowed',
                      0)  # In this case the repeated genes are NOT allowed ---> Each item can be taken only once
ga.set_hyperparameter('minimize', 0)  # In this case the goal is to maximize the fitness
ga.set_hyperparameter('elitism_rate', 0.1)  # Set an elitism rate of 0.1
ga.set_hyperparameter('mutation_rate', 0.4)  # Set a mutation rate of 0.15
ga.set_hyperparameter('mutation_type', 'both')  # Set the mutation type
# ga.set_hyperparameter('keep_diversity', 10)  # Set a mechanism to keep the diversity every 5 generations
ga.set_hyperparameter('show_progress',
                      1)  # Show progress of the genetic algorithm (this will print the generation number)

best_individual = ga.optimize()  # Launch optimization

best_individual, population, historic_fitness = ga.get_results()  # Get other results


end_time = time.time()
elapsed_time = end_time - start_time

print(best_individual)
print(elapsed_time)

# Iteration numbers (1 through 5)
iterations = range(1, (len(historic_fitness))+1)

# Create the plot
plt.plot(iterations, historic_fitness, marker='o')

# Add title and labels
plt.title('Fitness vs. Generation Number')
plt.xlabel('Generation Number')
plt.ylabel('Fitness')

# Show grid
plt.grid(True)

# Display the plot
plt.show()