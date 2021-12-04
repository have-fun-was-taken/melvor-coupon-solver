# The version where I optimize the item checks.
# The runtime is 3.5s compared to 10s of the unoptimized version. Can make a difference if more than 100k trials.

def generate_thresholds(desired_items):
    threshold_list = []
    counter = 0
    
# Adding the edge threshold of 0. It is used to make the processing of thresholds
#  uniform in the main loop.
    threshold_list.append([0, True])
    
    for i in desired_items:
        counter += i
        threshold_list.append([counter, False])
        
# Reversing the list because all thresholds are at the start of the array.
# If we reverse the list, we can check the first index and proceed only if 
#  the roll is lower than it.
    threshold_list.reverse()    
    
    return threshold_list

def reset_item_hits(threshold_list):
# Making every flag False aside from the edge flag of 0 that is always true.
    for i in range(len(threshold_list) - 1):
        if not threshold_list[i][1]:
            print('threshold_list:', threshold_list)
            print('Critiacl error. Threshold is False when hit_counter says all items were hit.', \
                'Terminating the process.')
            exit()
        threshold_list[i][1] = False
        
    return threshold_list

import random
import statistics
import numpy
import time

print ('\r\n Melvor Idle drop probability calculator\r\n')
print ('Starting the simulation with the parameters in the source file:')

# Probability base of the drop table. 
# On wiki, the chance is shown as a fraction and as percentage.
# The bottom number of the fraction is what needs to be entered here.
probability_base = 723

# The upper numbers of drop chances for the desired items.
# For instance, on wiki the chance can be 20/837. 20 is what you'd need to put here.
# Make the denominators of all desired items equal to probability_base before putting the numbers here.
desired_items = [3, 3, 2, 2]

# Number of trials to get the final average from.
number_of_trials = 10000

threshold_list = generate_thresholds(desired_items)

print ('Probability base:', probability_base)
print ('Desired items:', desired_items)
print ('Number of trials:', number_of_trials, '\r\n')
print ('Thresholds list:', threshold_list, '\r\n')

rng_value = 0
roll_counter = 0
hit_counter = 0
success_roll_numbers = []

for i in range(number_of_trials):
    while True:
        rng_value = random.uniform(0, probability_base)
        roll_counter += 1
        if rng_value <= threshold_list[0][0]:
            for i in range(len(threshold_list) - 1):
                if not threshold_list[i][1] and rng_value <= threshold_list[i][0] and rng_value > threshold_list[i+1][0]:
                    threshold_list[i][1] = True
                    hit_counter += 1
                    break
            if hit_counter == len(threshold_list) - 1:
                success_roll_numbers.append(roll_counter)
                break
                
            if hit_counter >= len(threshold_list):
                print('Critial error, hit_counter is', hit_counter, \
                    'when the number of the desired items is', len(threshold_list), \
                    '. Hit_counter should have always been less.', 'Terminating the process.')
                exit()
    
    roll_counter = 0
    hit_counter = 0
    threshold_list = reset_item_hits(threshold_list)

print('The average number of rolls to hit all desired items is', statistics.mean(success_roll_numbers),'.')
print('The median is', statistics.median(success_roll_numbers),'.')
print('Q1:', numpy.percentile(success_roll_numbers, 25))
print('Q3:', numpy.percentile(success_roll_numbers, 75))