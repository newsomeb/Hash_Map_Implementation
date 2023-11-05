# Name: Benjamin Alex Newsome
# OSU Email: newsomeb@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/2023
# Description: Implementation of SC hash map


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
        Updates key/value pair in hash  map. If given key already exists, its value must be replaced with the new value.
        Otherwise the value is added
        """
        # finds hash value for key
        hash = self._hash_function(key)
        # finds index of new key
        index = hash % self._capacity

        bucket = self._buckets[index]
        node = bucket._head

        # check to see if there's a key that matches current key
        while node is not None:
            if node.key == key:
                # updates node's value
                node.value = value
                return
            node = node.next

        # attach key, value to bucket
        bucket.insert(key, value)
        self._size += 1

        # double capacity if load is greater than 1
        if self.table_load() > 1.0:
            self.resize_table(self._capacity * 2)

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table
        """
        count = 0

        # counts one for every empty bucket
        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            if bucket._head is None:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns current hash table load factor
        """
        load_factor = self._size / self._capacity
        return load_factor

    def clear(self) -> None:
        """
        Clears contents of hash map while retaining underlying has table capacity
        """
        # store current capacity
        new_capacity = self._capacity

        self._buckets = DynamicArray()

        # create and append empty linked lists to new array
        for _ in range(new_capacity):
            self._buckets.append(LinkedList())

        # reset size to zero
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        changes capacity of internal hash table while keeping existing key/value pairs
        """

        # ends method if new capacity is less than 1
        if new_capacity < 1:
            return

        # check if prime, if not prime set next prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create new buckets with new capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        old_buckets = self._buckets

        # rehash keys and values into new buckets
        for i in range(old_buckets.length()):
            bucket = old_buckets[i]
            node = bucket._head

            while node is not None:
                # find hash and index for resized table
                hash = self._hash_function(node.key)
                index = hash % new_capacity
                new_bucket = new_buckets[index]
                # put key, value into bucket
                new_bucket.insert(node.key, node.value)

                node = node.next

        # update buckets and capacity
        self._buckets = new_buckets
        self._capacity = new_capacity


    def get(self, key: str):
        """
        Gets value of associated key. Returns None if value not found
        """
        # calculates index
        index = self._hash_function(key) % self._capacity
        # retrieves bucket at calculated index
        bucket = self._buckets.get_at_index(index)

        node = bucket._head

        # iterate through nodes looking for key
        while node is not None:
            if node.key == key:
                # return key if found
                return node.value
            node = node.next
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False
        """
        # calculates index
        index = self._hash_function(key) % self._capacity
        # retrieves bucket at calculated index
        bucket = self._buckets.get_at_index(index)

        node = bucket.contains(key)
        return node is not None

    def remove(self, key: str) -> None:
        """
        Removes given key and associated value. Method does nothing if value not found.
        """
        # calculates index
        index = self._hash_function(key) % self._capacity
        # retrieves bucket at calculated index
        bucket = self._buckets.get_at_index(index)

        # if keys exist, remove key
        if bucket.contains(key):
            bucket.remove(key)
            # hash map size decreases by 1
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns dynamic array where each index contains a tuple of a key/value pair
        """
        array = DynamicArray()

        # iterates through buckets
        for i in range(self._buckets.length()):
            bucket = self._buckets.get_at_index(i)
            node = bucket._head

            # appends each node to new array
            while node is not None:
                array.append((node.key, node.value))
                node = node.next

        return array

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives unsorted (maybe sorted) dynamic array. Return tuple containing
    dyanmic array comprising mode and the frequency of the mode.
    """

    length = da.length()
    map = HashMap()

    # loop through dynamic array, add it with a frequency of 1
    # if already added to map add 1 to frequency
    for i in range(length):
        number = da.get_at_index(i)
        if map.contains_key(number):
            map.put(number, map.get(number) + 1)
        else:
            map.put(number, 1)

    # get key / values from map
    key_value = map.get_keys_and_values()

    mode = DynamicArray()
    mode_frequency = 0

    # loop over key/value to find the mode, if the value being looped over is > than mode_frequency
    # value becomes new mode_frequency
    for i in range(key_value.length()):
        key, value = key_value.get_at_index(i)
        if value > mode_frequency:
            mode_frequency = value
            mode = DynamicArray()
            mode.append(key)
            # add key if value matches mode frequency
        elif value == mode_frequency:
            mode.append(key)

    return mode, mode_frequency


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
