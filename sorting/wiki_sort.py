import random
import time
import wiki_sort


def wikisort(array):
    def reverse_range(array, start, end):
        while start < end:
            array[start], array[end] = array[end], array[start]
            start += 1
            end -= 1

    def rotate(array, start, mid, end):
        reverse_range(array, start, mid - 1)
        reverse_range(array, mid, end - 1)
        reverse_range(array, start, end - 1)

    def binary_search_left(array, value, start, end):
        while start < end:
            mid = (start + end) // 2
            if array[mid] < value:
                start = mid + 1
            else:
                end = mid
        return start

    def merge(array, start, mid, end):
        left = array[start:mid]
        left_length = len(left)
        left_index = 0
        right_index = mid

        for k in range(start, end):
            if left_index < left_length and (
                right_index >= end or left[left_index] <= array[right_index]
            ):
                array[k] = left[left_index]
                left_index += 1
            else:
                array[k] = array[right_index]
                right_index += 1

    def merge_sort(array, start, end):
        if end - start < 2:
            return

        mid = (start + end) // 2
        merge_sort(array, start, mid)
        merge_sort(array, mid, end)
        merge(array, start, mid, end)

    merge_sort(array, 0, len(array))


def benchmark(func, data_sizes):
    results = {}
    for size in data_sizes:
        data = random.sample(range(1, size + 1), size)
        start_time = time.time()
        func(data.copy())
        end_time = time.time()
        results[size] = end_time - start_time
    return results


if __name__ == "__main__":
    data_sizes = [100, 1000, 10000, 100000, 1000000]
    wikisort_results = benchmark(wiki_sort.wikisort, data_sizes)
    sorted_results = benchmark(sorted, data_sizes)

    print("Wikisort results:")
    for k, v in wikisort_results.items():
        print(f"Size: {k}\nTime: {v}")

    print("Built-in sorted results:")
    for k, v in sorted_results.items():
        print(f"Size: {k}\nTime: {v}")
