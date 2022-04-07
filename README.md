This structure was created with the following aims:
---------------------------------------------------
- easy to implement in hardware
- using less memory
- yet remaining relatively fast

Its properties as far as I can see:
-----------------------------------
- fairly constant maximal runtime
- space occupation can be adjusted according to minimum and maximum estimations
- free of reordering ie. no stack or recursion is needed
- might be implemented burst friendly for dynamic memories
- in some special cases it can be cache efficient too

The solution:
-------------
It is a mixture of hash map, binary tries and linked lists:
1) the key is hashed, and a portion of this index (mostly its modulus) is used to index a hash map;
2) if the hash map's entry doesn't contain the full index, then the other portion of the index is used to build or search the binary trees originating from the particular buckets;
3) in case of index collisions a linked list is built from the last branching origin, where the existing index is found, and the values are distinguished by the keys themselves.

The concept of a binary trie is:
--------------------------------
Hashes' randomness can not only be used to scatter data around memory, but also, to build a fairly well balanced tree, without any kind of active, intentional reordering necessary. Furthermore since the individual bits of hashes are also pretty random, they can be used one-by-one to decide which next branch to choose for storing or searching, there is no need to compare indexes of values' keys to the indexes stored at branching points. This enables a straighforward hardware implementation, because only addressing is needed to access data, yet the data structure doesn't need to consume as much space as a hasmap.

For example:
------------
If the key's hash is a 32 bit CRC, then the lower 16 bits can be used to directly address one of 65536 buckets of hash map in memory, and the MSB of the higher 16 bits can be used to decide which branch to take from the bucket, if it is taken at storage time, or if the lower 16 bits don't match the searched index at search time. Then at the next branch, MSB-1 is being used to choose which way to proceed, etc.
