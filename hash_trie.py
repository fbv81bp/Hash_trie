import hashlib

# most likely maximum elements that will be stored in the dictionary
elements = 100000
# most likely minimum elements that will be stored in the dictionary
listSize = 10

# fields: 0:occupied 1:index 2:key 3:value 4:branches 5:linked list
list_but_not_the_composer = [[False, None, None, None, [None, None], None] for i in range(listSize)]

def testbit(x, n):
    if (x & (1<<n)):
        return 1
    else:
        return 0
        
def find(key):
    # very few collisions with a good hash function...
    #index = int('0x' + hashlib.sha256(str(key).encode('ASCII')).hexdigest(),0)
    # creating index collisons for testing linked lists:
    index = int('0x' + hashlib.sha256(str(key).encode('ASCII')).hexdigest(),0) % 10000
    pointer = list_but_not_the_composer[index % listSize]
    n = 14
    if pointer[0]:
        while True:
            if pointer[2] == key:
                break
            elif pointer[1] == index:
                if pointer[5] is not None:
                    pointer = pointer[5]
                else:
                    break
            else:
                if testbit(index, n) == 0:
                    if pointer[4][0] is not None:
                        pointer = pointer[4][0]
                        n -= 1
                    else:
                        break
                else:
                    if pointer[4][1] is not None:
                        pointer = pointer[4][1]
                        n -= 1
                    else:
                        break
    return(pointer, n)

def insert(key, value):
    pointer, n = find(key)
    # very few collisions with a good hash function...
    #index = int('0x' + hashlib.sha256(str(key).encode('ASCII')).hexdigest(),0)
    # creating index collisons for testing linked lists
    index = int('0x' + hashlib.sha256(str(key).encode('ASCII')).hexdigest(),0) % 10000
    newLinked = False
    valueUpdate = False
    if pointer[0] == False:
        pointer[0] = True
        pointer[1] = index
        pointer[2] = key
        pointer[3] = value
        pointer[4] = [None,None]
        pointer[5] = None
    else:
        if pointer[1] != index:
            if testbit(index, n) == 0:
                pointer[4][0] = [True, index, key, value, [None,None], None]
            else:
                pointer[4][1] = [True, index, key, value, [None,None], None]
        elif pointer[2] == key:
            valueUpdate = True
            pointer[3] = value
        else:
            newLinked = True
            pointer[5] = [True, index, key, value, [None,None], None]
    return(valueUpdate, newLinked)

# TESTING

print('\nINSERTING')
updatedValues = 0
addedLinkedEl = 0
for i in range(elements):
    valU, newL = insert(i, i + 1)
    if valU:
        updatedValues += 1
    if newL:
        addedLinkedEl += 1
print('updated values:', updatedValues)    
print('added linked elements:', addedLinkedEl)    

print('checking')
matches = True
faulty = 0
for i in range(elements):
    if find(i)[0][3] != i + 1:
        matches = False
        faulty += 1
print('values match:', matches, 'faulty:', faulty)

print('\nOVERWRITING')
updatedValues = 0
addedLinkedEl = 0
for i in range(elements):
    valU, newL = insert(i, i + 2)
    if valU:
        updatedValues += 1
    if newL:
        addedLinkedEl += 1
print('updated values:', updatedValues)    
print('added linked elements:', addedLinkedEl) 

print('checking')
matches = True
faulty = 0
for i in range(elements):
    if find(i)[0][3] != i + 2:
        matches = False
        faulty += 1
print('values match:', matches, 'faulty:', faulty)

print('\nBOTH')
updatedValues = 0
addedLinkedEl = 0
for i in range(elements):
    valU, newL = insert(i + 1000, i + 3)
    if valU:
        updatedValues += 1
    if newL:
        addedLinkedEl += 1
print('updated values:', updatedValues)    
print('added linked elements:', addedLinkedEl) 

print('checking')
matches = True
faulty = 0
for i in range(elements):
    if find(i + 1000)[0][3] != i + 3:
        matches = False
        faulty += 1
print('values match:', matches, 'faulty:', faulty)


