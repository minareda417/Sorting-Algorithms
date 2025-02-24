import random
import time
# Selection Sort Algorithm
def selection_sort(arr):
    # Get array length
    n = len(arr)
    # Start the timer
    start_time = time.time()
    # Traverse through all array elements
    for i in range(n):
        # Find the minimum element in the remaining unsorted array
        min_idx = i
        # Traverse through the unsorted array
        for j in range(i + 1, n):
            # Update the index of the minimum element
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    elapsed_time = time.time() - start_time
    print(f"Total time taken by selection sort for {n} elements: {elapsed_time}")
    return arr

# Insertion Sort Algorithm
def insertion_sort(arr):
    # Get array length
    n = len(arr)
    # Start the timer
    start_time = time.time()
    # Traverse through all array elements
    for i in range(1, n):
        # Get the current index and element
        current_idx = i
        current = arr[i]
        while current_idx > 0 and arr[current_idx - 1] > current:
            # Swap the elements if the previous element is greater
            arr[current_idx] = arr[current_idx - 1]
            # Decrement current_idx to the previous index
            current_idx -= 1
        # Insert the current element at the correct position
        arr[current_idx] = current
    elapsed_time = time.time() - start_time
    print(f"Total time taken by insertion sort for {n} elements: {elapsed_time}")
    return arr

def main():
    # Test selection sort
    arr = random.sample(range(1, 1000001), 25000)
    # sorted_arr = selection_sort(arr)
    # print(f"Selection Sort: {selection_sort}", selection_sort(arr))
    # Test insertion sort
    # print(f"Insertion Sort: ", insertion_sort(arr))
    sorted_arr = insertion_sort(arr)
if __name__ == "__main__":
    main()