# Name: Benjamin Alex Newsome
# OSU Email: newsomeb@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/2023
# Description: Implementation of OA hash map

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
        Updates key/value pair in hash  map. If given key already exists, its value must be replaced with the new value.
        Otherwise the value/key is added
        """
        # double capacity if load is greater than or equal to .5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # keep track of probe count
        probe_count = 0

        # calculate hash value  for key
        hash_value = self._hash_function(key)

        # initial slot for key
        index = hash_value % self._capacity

        # enter loop to find empty slot or max probe reached
        while probe_count < self._capacity:
            slot = self._buckets.get_at_index(index)

            # if slot is empty or a tombstone then key and value is placed here
            if slot is None:
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return

            elif slot.is_tombstone:
                self._buckets.set_at_index(index, HashEntry(key, value))
                return

            # if slot key matches given key, replace value in the slot
            elif slot.key == key:
                self._buckets.set_at_index(index, HashEntry(key, value))
                return

            # quadratic probing for collisions
            probe_count += 1
            index = (hash_value + probe_count**2) % self._capacity

    def table_load(self) -> float:
        """
        Returns current hash table load factor
        """
        # calculate load factor
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        changes capacity of internal hash table while keeping existing key/value pairs
        """

        # ends method if new capacity is less than or equal to 1 or new_capacity is less than size
        if new_capacity <= 1 or new_capacity < self._size:
            return

        # check if prime, if not prime set next prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        old_buckets = self._buckets

        # create empty buckets with new capacity
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(None)

        # reset map size
        self._size = 0

        # update capacity to new capacity
        self._capacity = new_capacity

        # iterate through each slot in old bucket
        for i in range(old_buckets.length()):
            slot = old_buckets[i]
            # rehash and add key/value to new size
            if slot is not None and not slot.is_tombstone:
                self.put(slot.key, slot.value)


    def get(self, key: str) -> object:
        """
        Gets value of associated key. Returns None if value not found
        """

        probe_count = 0

        # calculate hash value  for key
        hash_value = self._hash_function(key)

        # initial slot for key
        index = hash_value % self._capacity
        # retrieve slot at the calculated index in array
        slot = self._buckets.get_at_index(index)

        # iterate through slot looking for key while we have not probed the entire table
        while slot is not None and not slot.is_tombstone:
            if slot.key == key:
                # return key if found
                return slot.value

            # quadratic probing
            probe_count += 1
            index = (hash_value + probe_count**2) % self._capacity
            slot = self._buckets.get_at_index(index)

        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False
        """
        # keep track of probe count
        probe_count = 0

        # calculate hash value  for key
        hash_value = self._hash_function(key)

        # initial slot for key
        index = hash_value % self._capacity
        # retrieve slot at the calculated index in array
        slot = self._buckets.get_at_index(index)

        while slot is not None and not slot.is_tombstone:
            if slot.key == key:
                return True

            # increase probe count by one if current slot did not match
            probe_count += 1
            index = (hash_value + probe_count ** 2) % self._capacity
            # find next slot
            slot = self._buckets.get_at_index(index)

        # if loop completes without finding key, return false
        return False

    def remove(self, key: str) -> None:
        """
        Removes given key and associated value. Method does nothing if value not found.
        """

        probe_count = 0
        # calculate hash value  for key
        hash_value = self._hash_function(key)

        # initial slot for key
        index = hash_value % self._capacity

        # quadratic probe until empty lot or key is found
        while probe_count < self._capacity:
            slot = self._buckets.get_at_index(index)

            # if slot is none then key doesn't exist, method ends
            if slot is None:
                return

            # if slot isn't a tombstone and slot contains key being searched
            if not slot.is_tombstone and slot.key == key:
                # slot becomes tombstone since value has been found
                slot.is_tombstone = True
                self._size -= 1
                return

            # quadratic probing
            probe_count += 1
            index = (hash_value + probe_count ** 2) % self._capacity


    def clear(self) -> None:
        """
        Clears contents of hash map while retaining underlying has table capacity
        """
        self._buckets = DynamicArray()

        # create and append empty slots to new hash table
        for _ in range(self._capacity):
            self._buckets.append(None)

        # reset size to zero
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns dynamic array where each index contains a tuple of a key/value pair
        """
        array = DynamicArray()

        # iterates through buckets
        for i in range(self._buckets.length()):
            slot = self._buckets.get_at_index(i)

            # appends each slot to new array
            # check to make sure not none and not tombstone
            if slot is not None and not slot.is_tombstone:
                array.append((slot.key, slot.value))

        return array

    def __iter__(self):
        """
        Enables hash map to iterate across itself
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns next item in hash map based on current location of iterator
        """

        # iterate through buckets startings from current index
        while self._index < self._buckets.length():
            slot = self._buckets.get_at_index(self._index)
            self._index += 1
            if slot is not None and not slot.is_tombstone:
                # return slot if not none and not tombstone
                return slot
        raise StopIteration


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
