from itertools import cycle, islice


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    chunk([1,2,3], 2) --> [[1,2][3]]
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def flatten(sequence):
    """
    Takes an irregular sequence of sequences and scalars and flattens them into one sequence:
    eg, [1,[2,3,4],5] becomes [1,2,3,4,5].

    NOTE: Consider only keys of dicts will be resolved into the return list!
    :param x:
    :return: flattened list
    """
    result = []
    for element in sequence:
        if hasattr(element, "__iter__") and not isinstance(element, basestring):
            result.extend(flatten(element))
        else:
            result.append(element)
    return result


def flatten_funcs(sequence, *functions):
    """
    Takes an irregular iterable 'sequence' of iterables and scalars and flattens them into one sequence:
    eg, [1,[2,3,4],5] becomes [1,2,3,4,5]. It then applies each function of 'functions' to each item in the list.

    NOTE: Consider only keys of dicts will be resolved into the return list!
    :param x:
    :return: flattened list
    """
    result = flatten(sequence)
    for func in functions:
        result = map(func, result)
    return result


def partition(sequence, partition_size):
    """
    Lazily break a sequence into 'partition_size' chunks
    :param sequence:
    :param partition_size:
    :return: a new lazy sequence containing the original elements in 'partition_sized' number of sequences.
    """
    part = []
    for p in sequence:
        part.append(p)
        if len(part) >= partition_size:
            yield part
            part = []
    if len(part): yield part


def interleave(*iterables):
    """
    Creates a new sequence from each successive element of each collection
    interleave([1,2,3], [4,5,6]) --> [1,4,2,5,3,6]
    interleave('ABC', 'D', 'EF') --> A D E B F C
    """
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def index_of(f, seq, start=0):
    """Return index of first item in sequence where f(item) == True."""
    if start > 0:
        seq = seq[start:]
    for i, item in enumerate(seq, start=start):
        if f(item) == True:
            return i


def listable(might_be_listable):
    """
    Returns whether something is truly a sequence and not merely a string or  some other kind of scalar.
    :param might_be_listable:
    :return: whether something is a list-like object
    """
    return hasattr(might_be_listable, "__len__") and (not isinstance(might_be_listable, basestring))


def comma_delimited_string_to_list(comma_delimited_string):
    if comma_delimited_string is None or comma_delimited_string == '':
        item_list = []
    else:
        item_list = [x.strip() for x in comma_delimited_string.split(',')]
    return item_list
