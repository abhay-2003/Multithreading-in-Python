import threading
import time
import random

MAX_THREADS = 4
active_threads = 0
thread_lock = threading.Lock()

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = quicksort([x for x in arr[1:] if x < pivot])
    right = quicksort([x for x in arr[1:] if x >= pivot])
    return left + [pivot] + right

def threaded_quicksort(arr, result_holder):
    global active_threads

    if len(arr) <= 1:
        result_holder.extend(arr)
        return

    pivot = arr[0]
    left_part = [x for x in arr[1:] if x < pivot]
    right_part = [x for x in arr[1:] if x >= pivot]

    left_result = []
    right_result = []

    threads = []

    with thread_lock:
        if active_threads < MAX_THREADS:
            active_threads += 1
            t1 = threading.Thread(target=threaded_quicksort, args=(left_part, left_result))
            threads.append(t1)
            t1.start()
        else:
            left_result.extend(quicksort(left_part))

        if active_threads < MAX_THREADS:
            active_threads += 1
            t2 = threading.Thread(target=threaded_quicksort, args=(right_part, right_result))
            threads.append(t2)
            t2.start()
        else:
            right_result.extend(quicksort(right_part))

    for t in threads:
        t.join()
        with thread_lock:
            active_threads -= 1

    result_holder.extend(left_result + [pivot] + right_result)

if __name__ == "__main__":
    size = 100000
    data = [random.randint(0, 1000000) for _ in range(size)]
    data_copy = data.copy()

    # Single-threaded
    start = time.time()
    sorted_single = quicksort(data)
    print("Single-threaded Quicksort Time:", time.time() - start, "seconds")

    # Multi-threaded
    start = time.time()
    result = []
    threaded_quicksort(data_copy, result)
    print("Multi-threaded Quicksort Time:", time.time() - start, "seconds")
