# Name: Mason Hunerkoch
# Description: Implement a hash map via chaining and open addressing.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        First this method will check if the load factor is 1.0 or greater and resize if so.
        Next, adds a new key value pair to the hash map. If the key already exists, it overwrites the existing value.
        """
        # Check table load is less than 1.0
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hash_index = self._hash_function(key) % self._capacity
        if self.contains_key(key):
            self._buckets[hash_index].remove(key)
            self._buckets[hash_index].insert(key, value)
        else:
            self._buckets[hash_index].insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table if the size passed is > 1. The function will verify the size is a prime number and if not,
        resize the table to the next prime number.
        """
        # Verify new_capacity is a valid prime number.
        if new_capacity < 1:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create an array of the data to be transferred over and clear the list.
        data_transfer = self.get_keys_and_values()
        self.clear()

        # Upsize or downsize the map as required.
        if new_capacity > self._capacity:
            for index in range(self._capacity, new_capacity):
                self._buckets.append(LinkedList())
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
        count = 0
        for index in range(self._capacity):
            if self.is_bucket_empty(index):
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key or none if the key does not exist.
        """
        index = self._hash_function(key) % self._capacity
        element = self._buckets[index].contains(key)
        if element is None:
            return None
        else:
            return element.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map.
        """
        hash_index = self._hash_function(key) % self._capacity
        if self._buckets[hash_index].contains(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key from the map if applicable.
        """
        index = self._hash_function(key) % self._capacity
        if self._buckets[index].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each element is a tuple of the key value pairs in the map.
        """
        our_array = DynamicArray()
        for index in range(self._capacity):
            if not self.is_bucket_empty(index):
                for node in self._buckets[index]:
                    our_array.append((node.key, node.value))
        return our_array

    def clear(self) -> None:
        """
        Clears the hash map.
        """
        for index in range(self._capacity):
            self._buckets[index] = LinkedList()
        self._size = 0

    def is_bucket_empty(self, index: int) -> bool:
        """Returns true or false based on whether or not the bucket is empty."""
        if self._buckets[index].length() == 0:
            return True
        else:
            return False

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a tuple that contains a dynamic array of the value(s) that occur most and then an integer of the total
    occurrence.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    mode_nums = DynamicArray()
    mode_occurrence = 0

    # Map each item if it is not already in the map. If it is in the map, increment the value object by 1.
    for index in range(da.length()):
        if map.contains_key(da[index]) is False:
            map.put(da[index], 1)
        else:
            counter = str(map.get(da[index]))
            map.put(da[index], int(counter) + 1)

    # Get a list of each unique object in the list and the count.
    data = map.get_keys_and_values()

    for index in range(data.length()):
        if data[index][1] > mode_occurrence:
            mode_occurrence = data[index][1]
            mode_nums = DynamicArray()
            mode_nums.append(data[index][0])
        elif data[index][1] == mode_occurrence:
            mode_nums.append(data[index][0])

    return (mode_nums, mode_occurrence)


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
