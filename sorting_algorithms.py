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
        # Traverse through the unsorted part of the array
        for curr_idx in range(i+1, n):
            # Update the index of the minimum element
            if arr[curr_idx] < arr[min_idx]:
                min_idx = curr_idx
        if min_idx != i:
            # Swap the found minimum element with the current element
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

####################################### Part 2 #######################################
# Method to partition the array using a random pivot
def partition_random_pivot(arr, low, high):
    # Choose a random pivot
    pivot = arr[random.randint(low, high)]
    #  Left and right pointers
    left = low
    right = high
    # While the left values are smaller than the right values, keep shifting the pointers
    while (left <= right):
        # Move the left pointer to a larger value
        while(arr[left] < pivot):
            left += 1
        # Move the right pointer to a smaller value
        while(arr[right] > pivot):
            right -= 1
        # If arr[left] > pivot and arr[right] < pivot
        # Then left <= right, swap the values
        if left <= right:
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1
    # Left is now the first index of the right partition (left > right)
    return left
# Recursive quick sort method
def _quick_sort_recursion(arr,low,high):
    if low < high:
        # Find the pivot index
        pivot_idx = partition_random_pivot(arr, low, high)
        # Sort the elements before and after the pivot
        _quick_sort_recursion(arr, low, pivot_idx - 1)
        _quick_sort_recursion(arr, pivot_idx, high)
# Quick sort caller method to calculate the elapsed time
def quick_sort(arr):
    # Get the array length
    n = len(arr)
    # Start the timer
    start_time = time.time()
    # Call the recursive quick sort method
    _quick_sort_recursion(arr, 0, n-1)
    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Total time taken by quick sort for {n} elements: {elapsed_time}")
    return arr, elapsed_time

# Method to find the kth greatest element in an unsorted array
def find_kth_greatest(arr, k, low, high):
    if not (1 <= k <= len(arr)):
        return None
    # Convert k-th greatest to index in ascending order
    k_index = len(arr) - k 
    # Get the pivot index
    pivot_idx = partition_random_pivot(arr, low, high)

    if low <= high:
        # If the pivot index is the k-th greatest element, return the element
        if pivot_idx == k_index:
            return arr[pivot_idx]
        # If the pivot index is greater than the k-th greatest element
        # Search the left partition
        elif pivot_idx > k_index:
            return find_kth_greatest(arr, k, low, pivot_idx - 1)
        # If the pivot index is less than the k-th greatest element
        # Search the right partition
        else:
            return find_kth_greatest(arr, k, pivot_idx, high)

def _merge(arr1, arr2):
    arr = []
    while arr1 and arr2:
        if arr1[0] <  arr2[0]:
            arr.append(arr1.pop(0))
        else:
            arr.append(arr2.pop(0))
    while arr1:
        arr.append(arr1.pop(0))
    while arr2:
        arr.append(arr2.pop(0))
    return arr


def merge_sort(arr):
    n = len(arr)
    start_time = time.time()
    if len(arr) > 1:
        mid = len(arr)//2
        arr1, _ = merge_sort(arr[:mid])
        arr2, _ = merge_sort(arr[mid:])
        arr = _merge(arr1, arr2)
    elapsed_time = time.time() - start_time
    print(f"Total time taken by merge sort for {n} elements: {elapsed_time}")
    return arr, elapsed_time

def tim_sort(arr, threshold = 32):
    n = len(arr)
    start_time = time.time()
    if len(arr) <= threshold:
        return insertion_sort(arr)
    else:
        mid = len(arr)//2
        arr1, _ = tim_sort(arr[:mid])
        arr2, _ = tim_sort(arr[mid:])
        arr = _merge(arr1, arr2)
    elapsed_time = time.time() - start_time
    print(f"Total time taken by tim sort for {n} elements: {elapsed_time}")
    return arr, elapsed_time

def _heapify(arr, n, i):
    largest = i
    l = 2*i+1 # left child
    r = 2*i+2 # right child
    
    if l<n and arr[l] > arr[largest]:
        largest = l
    if r<n and arr[r] > arr[largest]:
        largest = r
    if i!=largest:
        arr[largest], arr[i] = arr[i], arr[largest]
        _heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    start_time = time.time()
    for i in range(len(arr)//2-1, -1, -1):
        _heapify(arr, len(arr), i)
    for i in range(len(arr)-1, -1, -1):
        arr[i], arr[0] = arr[0], arr[i]
        _heapify(arr, i, 0)
    elapsed_time = time.time() - start_time
    print(f"Total time taken by heap sort for {n} elements: {elapsed_time}")
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
def plot_time(quick_sort_time_dict:dict, insertion_sort_time_dict:dict, selection_sort_time_dict:dict)->None:
    x = list(quick_sort_time_dict.keys())
    y_bubble = list(quick_sort_time_dict.values())
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
#Plotting Array size versus time for each sorting algorithm  
def plot_time_part2(quick_sort_time_dict:dict, merge_sort_time_dict:dict, tim_sort_time_dict:dict, heap_sort_time_dict:dict)->None:
    x = list(quick_sort_time_dict.keys())
    y_quick = list(quick_sort_time_dict.values())
    y_merge = list(merge_sort_time_dict.values())
    y_selection = list(tim_sort_time_dict.values())
    y_heap = list(heap_sort_time_dict.values())

    plt.plot(x, y_quick, color = 'r', label = 'quick sort')
    plt.plot(x, y_merge, color = 'g', label = 'merge sort')
    plt.plot(x, y_selection, color = 'b', label = 'tim sort')
    plt.plot(x, y_heap, color = 'y', label = 'heap sort')

    plt.xlabel('Array size')
    plt.ylabel('Time(seconds)')
    plt.title('Array size vs Time')

    plt.legend()
    plt.show()





def main():
    size = 5
    values = generate_sizes()
    arrays = generate_arrays(values, size)
    
    # Create a queue for each sorting algorithm to store the results
    # bubble_sort_queue = mp.Queue()
    # insertion_sort_queue = mp.Queue()
    # selection_sort_queue = mp.Queue()
    quick_sort_queue = mp.Queue()
    merge_sort_queue = mp.Queue()
    tim_sort_queue = mp.Queue()
    heap_sort_queue = mp.Queue()

    # Create a process for each sorting algortihm
    # bubble_sort_process = mp.Process(target=sort_arrays, args=(copy.deepcopy(arrays), values, bubble_sort, size, bubble_sort_queue))
    # insertion_sort_process = mp.Process(target=sort_arrays, args=(copy.deepcopy(arrays), values, insertion_sort, size, insertion_sort_queue))
    # selection_sort_process = mp.Process(target=sort_arrays, args=(copy.deepcopy(arrays), values, selection_sort, size, selection_sort_queue))
    quick_sort_process = mp.Process(target=sort_arrays, args=(copy.deepcopy(arrays), values, quick_sort, size, quick_sort_queue))
    merge_sort_process =  mp.Process(target = sort_arrays, args = (copy.deepcopy(arrays), values, merge_sort, size, merge_sort_queue))
    tim_sort_process = mp.Process(target = sort_arrays, args = (copy.deepcopy(arrays), values, tim_sort, size, tim_sort_queue))
    heap_sort_process = mp.Process(target = sort_arrays, args = (copy.deepcopy(arrays), values, heap_sort, size, heap_sort_queue))

    # Start the processes
    # bubble_sort_process.start()
    # insertion_sort_process.start()
    # selection_sort_process.start()
    merge_sort_process.start()
    tim_sort_process.start()
    quick_sort_process.start()
    heap_sort_process.start()

    # Get the results from the queues
    # bubble_sort_lists, quick_sort_time_dict = bubble_sort_queue.get()
    # insertion_sort_lists, insertion_sort_time_dict = insertion_sort_queue.get()
    # selection_sort_lists, selection_sort_time_dict = selection_sort_queue.get()
    quick_sort_lists, quick_sort_time_dict = quick_sort_queue.get()
    merge_sort_lists, merge_sort_time_dict = merge_sort_queue.get()
    tim_sort_lists, tim_sort_time_dict = tim_sort_queue.get()
    heap_sort_lists, heap_sort_time_dict = heap_sort_queue.get()

    print("All results have been retrieved")



    # Wait for the processes to finish
    # bubble_sort_process.join()
    # insertion_sort_process.join()
    # selection_sort_process.join()
    quick_sort_process.join()
    merge_sort_process.join()
    tim_sort_process.join()
    heap_sort_process.join()

    print("All processes have finished")


    # Test and print the results
    # test_arrays(bubble_sort_lists)
    # print_average_time(quick_sort_time_dict)

    # test_arrays(insertion_sort_lists)
    # print_average_time(insertion_sort_time_dict)

    # test_arrays(selection_sort_lists)
    # print_average_time(selection_sort_time_dict)

    test_arrays(merge_sort_lists)
    print_average_time(merge_sort_time_dict)

    test_arrays(tim_sort_lists)
    print_average_time(tim_sort_time_dict)

    test_arrays(quick_sort_lists)
    print_average_time(quick_sort_time_dict)

    test_arrays(heap_sort_lists)
    print_average_time(heap_sort_time_dict)

    # plot_time(quick_sort_time_dict, insertion_sort_time_dict, selection_sort_time_dict)
    plot_time_part2(quick_sort_time_dict, merge_sort_time_dict, tim_sort_time_dict, heap_sort_time_dict)
    x = list(quick_sort_time_dict.keys())
    y_quick = list(quick_sort_time_dict.values())
    plt.plot(x, y_quick, color = 'r', label = 'quick sort')
    plt.xlabel('Array size')
    plt.ylabel('Time(seconds)')
    plt.title('Array size vs Time')
    plt.legend()
    plt.show()
    arr = random.sample(range(1, 20), 12)
    k = 3
    print("Array:", arr)
    for i in range(1, len(arr)):
        print(f"The {i}th greatest element is {find_kth_greatest(arr, i,0 , len(arr) - 1)}")



if __name__ == "__main__":
    main()
