import numpy as np

start = 0
end = 50
num_slices = 11

# def distribute_sum_centrally_even(m, n):
#     quotient, remainder = divmod(m, n)
#     result = [quotient] * n
    
#     # Calculate the starting index for distributing the remainder
#     start_index = (n - remainder) // 2
    
#     # Distribute the remainder centrally and evenly
#     for i in range(remainder):
#         result[start_index + i * 2 % n] += 1
    
#     return result

# def distribute_sum_centrally_even(m, n):
#     quotient, remainder = divmod(m, n)
#     result = [quotient] * n
    
#     # Calculate the center position
#     center_start = (n - remainder) // 2
    
#     # Distribute the remainder evenly around the center
#     for i in range(remainder):
#         result[center_start + i] += 1
    
#     return result

def distribute_sum_centrally_even(m, n):
    quotient, remainder = divmod(m, n)
    result = [quotient] * n
    
    # Calculate the intervals for distributing the remainder
    interval = n / (remainder + 1)
    
    # Distribute the remainder values
    for i in range(remainder):
        # Calculate the position to add the extra value
        pos = int(round(interval * (i + 1))) - 1
        result[pos] += 1
    
    return result

numlist = distribute_sum_centrally_even(end-start,num_slices)
print(numlist, sum(numlist))