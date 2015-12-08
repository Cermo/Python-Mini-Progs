def yieldAllCombos(items):
    """
        Generates all combinations of N items into two bags, whereby each 
        item is in one or zero bags.

        Yields a tuple, (bag1, bag2), where each bag is represented as a list 
        of which item(s) are in each bag.
    """
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in xrange(3**(N+):
        combo = []
        combo2 = []
        for j in xrange(N):
            # test bit jth of integer i
            if (i >> j*2) % 2 == 1 and (i >> j*2+1) % 2 == 0:
                combo.append(items[j])
            if (i >> j*2) % 2 == 0 and (i >> j*2+1) % 2 == 1:
                combo2.append(items[j])
        yield (combo, combo2)

result =  yieldAllCombos(['bag', 'walet'])
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
print result.next()
