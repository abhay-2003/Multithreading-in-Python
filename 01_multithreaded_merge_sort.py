import threading
import time
import random

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left = merge_sort(arr[:middle])
    right = merge_sort(arr[middle:])
    return merge(left, right)

def threaded_merge_sort(arr, result_holder):
    if len(arr) <= 1:
        result_holder.extend(arr)
        return

    mid = len(arr) // 2
    left_holder = []
    right_holder = []

    left_thread = threading.Thread(target=threaded_merge_sort, args=(arr[:mid], left_holder))
    right_thread = threading.Thread(target=threaded_merge_sort, args=(arr[mid:], right_holder))

    left_thread.start()
    right_thread.start()

    left_thread.join()
    right_thread.join()

    result_holder.extend(merge(left_holder, right_holder))

if __name__ == "__main__":
    size = 10000
    data = [random.randint(0, 10000) for _ in range(size)]
    data_copy = data.copy()

    # Single-threaded
    start = time.time()
    sorted_single = merge_sort(data)
    print("Single-threaded Merge Sort Time:", time.time() - start, "seconds")

    # Multi-threaded
    start = time.time()
    result = []
    threaded_merge_sort(data_copy, result)
    print("Multi-threaded Merge Sort Time:", time.time() - start, "seconds")
