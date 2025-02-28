import copy
import random
import time
import matplotlib.pyplot as plt
import multiprocessing as mp
#Generating the sizes of the used
def generate_sizes(lower_bound: int = 125, upper_bound:int = 128000, coefficient:float = 2) -> list:
    values = []
    while lower_bound <= upper_bound:
        values.append(lower_bound)
        lower_bound *= coefficient
    return values

def generate_arrays(values:list, size:int = 5) -> list:
    arrays = []
    for value in values:
        for _ in range(size):
            arrays.append(random.sample(range(1, 1000001), value))
    return arrays

def selection_sort(arr):
    # Get array length
    n = len(arr)
    # Start the timer
    start_time = time.time()
    # Traverse through all array elements
    for i in range(0, n - 1):
        # Find the minimum element in the remaining unsorted array
        min_idx = i
        # Traverse through the unsorted array
        for curr_idx in range(i+1, n):
            # Update the index of the minimum element
            if arr[curr_idx] < arr[min_idx]:
                min_idx = curr_idx
        if min_idx != i:
            # Swap the found minimum element with the first element
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    elapsed_time = time.time() - start_time
    print(f"Total time taken by selection sort for {n} elements: {elapsed_time}")
    return arr, elapsed_time

# Insertion Sort Algorithm
def insertion_sort(arr):
    # Get array length
    n = len(arr)
    # Start the timer
    start_time = time.time()
    # Traverse through all array elements
    for i in range(1, n):
        # Get the previous index and current element
        prev_idx = i-1
        current = arr[i]
        while prev_idx >= 0 and arr[prev_idx] > current:
            # Shift the elements if the previous element is greater
            arr[prev_idx+1] = arr[prev_idx]
            # Decrement prev_index
            prev_idx -= 1
        # Insert the current element at the correct position
        arr[prev_idx+1] = current
    elapsed_time = time.time() - start_time
    print(f"Total time taken by insertion sort for {n} elements: {elapsed_time}")
    return arr, elapsed_time

def bubble_sort(arr):
    # Get the array length
    n = len(arr)
    #Start the timer
    start_time = time.time()
    # Traverse through all array elements
    for i in range(1,n):
        # Flag to check when the array is sorted
        is_sorted = True
        # Iterate through the remaining indices to find the largest element
        for curr_idx in range(n-i):
            # Swap the elements if the current element is greater than the next element
            if arr[curr_idx] > arr[curr_idx+1]:
                arr[curr_idx], arr[curr_idx + 1] = arr[curr_idx + 1], arr[curr_idx]
                # Set the flag to false to indicate that swapping took place
                is_sorted = False
        # Break the loop if the array is sorted
        if is_sorted is True:
            break
    elapsed_time = time.time() - start_time
    print(f"Total time taken by bubble sort for {n} elements: {elapsed_time}")
    return arr, elapsed_time

# Sorting all arrays using the specified algorithm
def sort_arrays(arrays, values, algorithm, size, queue):
    sorted_arrays = []
    time_dic = {value: 0 for value in values}
    for arr in arrays:
        sorted_array, execution_time = algorithm(arr)
        sorted_arrays.append(sorted_array)
        time_dic[len(arr)] += execution_time / size
    queue.put((sorted_arrays, time_dic))
    print(f"Finished sorting {len(arrays)} arrays using {algorithm.__name__}")

# Method to check if an array id sorted or not
def _is_array_sorted(arr:list) -> bool:
    return all(arr[i] <= arr[i+1] for i in range (len(arr) - 1))

# Method to test if all arrays are well sorted
def test_arrays(arrays:list[list]) -> int:
    correct_arrays = 0
    for arr in arrays:
        if _is_array_sorted(arr):
            correct_arrays += 1
    print(f"{correct_arrays}/{len(arrays)}")
    return correct_arrays

# Printing average time of execution per array size
def print_average_time(time_dict:dict):
    for size, execution_time in time_dict.items():
        print(f"Average time for size {size} is {execution_time} seconds")

#Plotting Array size versus time for each sorting algorithm
def plot_time(bubble_sort_time_dict:dict, insertion_sort_time_dict:dict, selection_sort_time_dict:dict)->None:
    x = list(bubble_sort_time_dict.keys())
    y_bubble = list(bubble_sort_time_dict.values())
    y_insertion = list(insertion_sort_time_dict.values())
    y_selection = list(selection_sort_time_dict.values())

    plt.plot(x, y_bubble, color = 'r', label = 'bubble sort')
    plt.plot(x, y_insertion, color = 'g', label = 'insertion sort')
    plt.plot(x, y_selection, color = 'b', label = 'selection sort')

    plt.xlabel('Array size')
    plt.ylabel('Time(seconds)')
    plt.title('Array size vs Time')

    plt.legend()
    plt.show()





def main():
    size = 5
    values = generate_sizes()
    arrays = generate_arrays(values, 5)
    
    # Create a queue for each sorting algorithm to store the results
    bubble_sort_queue = mp.Queue()
    insertion_sort_queue = mp.Queue()
    selection_sort_queue = mp.Queue()
    
    # Create a process for each sorting algortihm
    bubble_sort_process = mp.Process(target=sort_arrays, args=(copy.deepcopy(arrays), values, bubble_sort, size, bubble_sort_queue))
    insertion_sort_process = mp.Process(target=sort_arrays, args=(copy.deepcopy(arrays), values, insertion_sort, size, insertion_sort_queue))
    selection_sort_process = mp.Process(target=sort_arrays, args=(copy.deepcopy(arrays), values, selection_sort, size, selection_sort_queue))

    # Start the processes
    bubble_sort_process.start()
    insertion_sort_process.start()
    selection_sort_process.start()
    
    # Get the results from the queues
    bubble_sort_lists, bubble_sort_time_dict = bubble_sort_queue.get()
    insertion_sort_lists, insertion_sort_time_dict = insertion_sort_queue.get()
    selection_sort_lists, selection_sort_time_dict = selection_sort_queue.get()

    print("All results have been retrieved")
    

    
    # Wait for the processes to finish
    bubble_sort_process.join()
    insertion_sort_process.join()
    selection_sort_process.join()

    print("All processes have finished")

    
    # Test and print the results
    test_arrays(bubble_sort_lists)
    print_average_time(bubble_sort_time_dict)

    test_arrays(insertion_sort_lists)
    print_average_time(insertion_sort_time_dict)

    test_arrays(selection_sort_lists)
    print_average_time(selection_sort_time_dict)

    plot_time(bubble_sort_time_dict, insertion_sort_time_dict, selection_sort_time_dict)



if __name__ == "__main__":
    main()