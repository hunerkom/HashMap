# Name: Mason Hunerkoch
# Description: Implement a hash map via chaining and open addressing.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        First this method will check if the load factor is 0.5 or greater and resize if so.
        Next, adds a new key value pair to the hash map. If the key already exists, it overwrites the existing value.
        """
        # Check table load is less than 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash_index = self._hash_function(key) % self._capacity

        if self._buckets[hash_index] is not None:
            if self._buckets[hash_index].key != key:
                hash_index = self.quadratic_prob(hash_index, key)

        if self._buckets[hash_index] is None:
            self._size += 1
        elif self._buckets[hash_index].is_tombstone is True:
            self._size += 1

        self._buckets[hash_index] = HashEntry(key, value)

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table if the size passed is > 1. The function will verify the size is a prime number and if not,
        resize the table to the next prime number.
        """
        # Verify new_capacity is a valid prime number.
        if new_capacity < self._size:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create an array of the data to be transferred over and clear the list.
        data_transfer = self.get_keys_and_values()
        self.clear()

        # Upsize or downsize the map as required.
        if new_capacity > self._capacity:
            for index in range(self._capacity, new_capacity):
                self._buckets.append(None)
        else:
            for index in range(self._capacity, new_capacity, - 1):
                self._buckets.pop()
        self._capacity = new_capacity

        # Add the data to the new map.
        for index in range(data_transfer.length()):
            self.put(data_transfer[index][0], data_transfer[index][1])

    def table_load(self) -> float:
        """
        Returns the load factor the map.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets within the map.
        """
        """count = 0
        for index in range(self._capacity):
            if self._buckets[index] is None or self._buckets[index].is_tombstone is True:
                count += 1"""
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the key or None if the key is not in the map.
        """
        hash_index = self._hash_function(key) % self._capacity
        if self._buckets[hash_index] is None or self._buckets[hash_index].is_tombstone is True:
            return None
        elif self._buckets[hash_index].key == key:
            return self._buckets[hash_index].value
        else:
            hash_index = self.quadratic_prob(hash_index, key)
            if self._buckets[hash_index] is None or self._buckets[hash_index].is_tombstone is True:
                return None
            elif self._buckets[hash_index].key == key:
                return self._buckets[hash_index].value

    def contains_key(self, key: str) -> bool:
        """
        Returns True or False based on whether or not the key is in the map.
        """
        hash_index = self._hash_function(key) % self._capacity
        if self._buckets[hash_index] is None or self._buckets[hash_index].is_tombstone is True:
            return False
        elif self._buckets[hash_index].key == key:
            return True
        else:
            hash_index = self.quadratic_prob(hash_index, key)
            if self._buckets[hash_index]is None:
                return False
            else:
                return True

    def remove(self, key: str) -> None:
        """
        Removes a key from the map.
        """
        hash_index = self._hash_function(key) % self._capacity
        if self._buckets[hash_index] is None:
            return
        elif self._buckets[hash_index].key == key and self._buckets[hash_index].is_tombstone is False:
            self._buckets[hash_index].is_tombstone = True
            self._size -= 1
        else:
            hash_index = self.quadratic_prob(hash_index, key)
            if self._buckets[hash_index] is None:
                return
            elif self._buckets[hash_index].key == key and self._buckets[hash_index].is_tombstone is False:
                self._buckets[hash_index].is_tombstone = True
                self._size -= 1
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each element is a tuple of the key value pairs in the map.
        """
        our_array = DynamicArray()
        for index in range(self._capacity):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                our_array.append((self._buckets[index].key, self._buckets[index].value))

        return our_array

    def clear(self) -> None:
        """
        Clears the hash map.
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def __iter__(self):
        """
        Iterator for loop
        """
        self._index = 0
        while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone is True:
            self._index += 1
        return self

    def __next__(self):
        """
        Finds next value and advances iter
        """
        try:
            value = self._buckets[self._index]
        except IndexError:
            raise StopIteration

        if value is None or value.is_tombstone is True:
            raise StopIteration
        self._index = self._index + 1
        return value

    def quadratic_prob(self, index: int, key: str) -> int:
        """Finds the next index via quadratic probing"""
        counter = 0
        original_index = index
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                return index
            counter += 1
            index = (original_index + (counter ** 2)) % self._capacity
        return index



# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
