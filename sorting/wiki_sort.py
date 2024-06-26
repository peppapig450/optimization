def wikisort(array):
    def reverse_range(array, start, end):
        while start < end:
            array[start], array[end] = array[end], array[start]
