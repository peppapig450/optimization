import random
import time
import wiki_sort
from pprint import pprint


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


def generate_data(data_size, data_type):
    """
    Generates data for different sorting scenarios.

    Args:
        data_size (int): The size of the data set.
        data_type (str): The type of data to generate. Possible values are:
            - 'random': Randomly shuffled integers.
            - 'descending': Integers in descending order.
            - 'ascending': Integers in ascending order.
            - '3sort': Ascending, then 3 random exchanges.
            - '+sort': Ascending, then 10 random values appended.
            - '%sort': Ascending, then 1% elements replaced randomly.
            - '~sort': Many duplicates (randomly inserted).
            - '=sort': All elements equal.
            - '!sort': Worst case (already sorted in descending order).

    Returns:
        list: The generated data list.
    """

    if data_type == "random":
        data = list(range(data_size))
        random.shuffle(data)
    elif data_type == "descending":
        data = list(range(data_size, 0, -1))
    elif data_type == "ascending":
        data = list(range(data_size))
    elif data_type == "3sort":
        data = list(range(data_size))
        for _ in range(3):
            i, j = random.sample(range(data_size), 2)
            data[i], data[j] = data[j], data[i]
    elif data_type == "+sort":
        data = list(range(data_size))
        data.extend(random.sample(range(data_size * 2), 10))
    elif data_type == "%sort":
        data = list(range(data_size))
        num_replacements = int(data_size * 0.01)
        for _ in range(num_replacements):
            i = random.randint(0, data_size - 1)
            data[i] = random.randint(0, data_size)
    elif data_type == "~sort":
        data = list(range(data_size))
        for _ in range(data_size // 2):
            i = random.randint(0, data_size - 1)
            data.insert(i, data[random.randint(0, data_size - 1)])
    elif data_type == "=sort":
        data = [data_size] * data_size
    elif data_type == "!sort":
        data = list(range(data_size, 0, -1))
    else:
        raise ValueError(f"Invalid data type: {data_type}")

    return data


def benchmark(sort_function, data):
    start_time = time.perf_counter_ns()
    sort_function(data)
    end_time = time.perf_counter_ns()
    return end_time - start_time


if __name__ == "__main__":
    data_sizes = [100, 1000, 10000, 100000]
    data_types_to_benchmark = [
        "random",
        "descending",
        "ascending",
        "3sort",
        "+sort",
        "%sort",
        "~sort",
        "=sort",
        "!sort",
    ]
    for size in data_sizes:
        for data_type in data_types_to_benchmark:
            data = generate_data(size, data_type)
            wikisort_time = benchmark(wiki_sort.wikisort, data)
            sorted_time = benchmark(sorted, data)

            print(f"Data Size: {size}, Data Type: {data_type}")
            print(f"Wikisort Time: {wikisort_time} seconds")
            print(f"Built-in sorted Time: {sorted_time} seconds")
            print()
            fastest_sort = (
                "Built-in sorted" if sorted_time < wikisort_time else "Wikisort"
            )
            fastest_time = min(wikisort_time, sorted_time)
            print(
                f"{fastest_sort} achieved the fastest time: {fastest_time} nanoseconds"
            )
            print("-" * 30)  # Optional separator for readability
