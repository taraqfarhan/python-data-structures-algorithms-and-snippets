import ctypes    # for low-level arrays

class DynamicArray:
    """A dynamic array class akin to a simplified Python List"""

    def __init__(self, array=None):
        """Create a Dynamic Array Object"""
        if array is None:
            # creating an empty array
            self._n = 0  # count actual elements
            self._capacity = 1  # default array capacity
            self._array = self._make_array(self._capacity) # get a low-level array with default capacity
        else:
            # creating the array from a given list as parameter
            self._n = self._capacity = len(array)
            self._array = self._make_array(self._n)
            for i in range(self._n):
                self._array[i] = array[i]


    def append(self, value):
        """Append one item to the end of the array"""
        if self._n == self._capacity:   # if the array is full, then resize it to it's double capacity
            self._resize(2 * self._capacity)
        self._array[self._n] = value
        self._n += 1


    def extend(self, array):
        """Extend current array with the values of another array"""
        for val in array:
            self.append(val)


    def count(self, value):
        """Return the total number of occurrences of value"""
        return sum(1 for v in self if v == value)


    def insert(self, index, value):
        """Insert a value in the given index"""
        if index >= self._n:  # if the index is greater or equal than the total num of elements in the array
            self.append(value)
        elif 0 <= index < self._n:
            if self._n + 1 > self._capacity:  # resize as we will need more space to store the new value
                self._resize(2 * self._capacity)
            for i in range(self._n, index, -1):
                self._array[i] = self._array[i - 1]
            self._array[index] = value
            self._n += 1
        else:
            raise IndexError("Invalid Index")   # else raise an exception


    def index(self, value):
        """Return the index of the first occurrence of value"""
        for i, val in enumerate(self):
            if val == value:
                return i
        raise ValueError("Value not in list")


    def remove(self, value):
        """Remove the first item from the array where array[i] == value"""
        try:
            # if total num of elements in the array is less than one forth of the capacity,
            # reduce the capacity by half
            if 4 * self._n <= self._capacity:
                self._resize(self._capacity // 2)

            index = self.index(value)
            for i in range(index, self._n - 1):
                self._array[i] = self._array[i + 1]   # left shift all the elements
            self._n -= 1
        except ValueError:
            raise ValueError("Value not in list")


    def pop(self, index=None):
        """Pop an item from the array"""
        # if total num of elements in the array is less than one forth of the capacity,
        # reduce the capacity by half
        if 4 * self._n <= self._capacity:
            self._resize(self._capacity // 2)

        if index is None:
            index = self._n - 1    # pop the last element by default

        if self._n == 0:
            raise IndexError("pop from empty list")
        if index < 0:
            index += self._n # handle negative indexing
        if index < 0 or index >= self._n:
            raise IndexError("Index out of range")

        value = self._array[index]
        for i in range(index, self._n - 1):
            self._array[i] = self._array[i + 1]   # left shift all the elements

        self._n -= 1
        return value


    def clear(self):
        """Clear the array"""
        self._n = 0
        self._resize(1)


    def __add__(self, other):
        """Adding two Dynamic Array objects"""
        ans = self._make_array(len(self) + len(other))

        for i in range(len(self)):
            ans[i] = self[i]
        for i in range(len(other)):
            ans[i + len(self)] = other[i]

        return DynamicArray(ans)


    def __iadd__(self, other):
        """Adding in place"""
        self.extend(other)
        return self


    def __mul__(self, const):
        """Getting [1,2,3] * 3 = [1,2,3,1,2,3,1,2,3] like behavior"""
        if not isinstance(const, int):
            raise ValueError("The constant must be an positive integer")

        result = self._make_array(const * self._capacity)
        for j in range(const):
            for i in range(self._n):
                result[i + self._n * j] = self[i]
        return DynamicArray(result)


    def __rmul__(self, const):
        """This handles 'int * array' by redirecting to 'array * int'"""
        return self.__mul__(const)


    def __len__(self):
        """Return number of elements stored in the array"""
        return self._n


    def __repr__(self):
        """Representation of the DynamicArray Object"""
        return f"DynamicArray({list(self)})"


    def __iter__(self):
        """Iterator for the DynamicArray object"""
        for i in range(self._n):
            yield self[i]


    def __getitem__(self, key):
        """Return an element or a slice object"""
        if isinstance(key, int):  # handle indexing
            if key < 0:  # handle negative indexing
                key += self._n
            if key < 0 or key >= self._n:
                raise IndexError("Index out of range")
            return self._array[key]
        elif isinstance(key, slice):  # handle slicing
            start, stop, step = key.indices(len(self))
            return self._array[start:stop:step]
        else:
            raise TypeError(f"Invalid key type: {type(key).__name__}")


    def __setitem__(self, key, value):
        """Modify the index or slice with the given value(s)"""
        if isinstance(key, (int, slice)): # handle both indexing and slicing
            self._array[key] = value
        else:
            raise TypeError(f"Invalid key type: {type(key).__name__}")


    def _resize(self, capacity):
        aux = self._make_array(capacity)  # new auxiliary array
        for i in range(self._n):  # copy the elements from the previous array
            aux[i] = self._array[i]
        self._array = aux    # set the resized array as the new array
        self._capacity = capacity   # updating capacity


    def _make_array(self, capacity):
        """Return a low-level new array with given capacity"""
        return (capacity * ctypes.py_object)()   # get low-level array with exact capacity
