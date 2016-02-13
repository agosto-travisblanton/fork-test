from itertools import chain


def create_merged_dictionary(array_of_dictionaries_to_merge):
    return dict(chain.from_iterable(d.iteritems() for d in array_of_dictionaries_to_merge))


def order_dictionary_with_datetimes_as_keys(the_dict):
    ordered_array = []
    for item in sorted(the_dict):
        ordered_array.append(item)
    return ordered_array


def join_array_of_strings(array_of_strings):
    to_return = ''
    for item in array_of_strings:
        to_return = to_return + item + ";"
    return to_return


# final notes
# change from player to display
# take out all columns where no data (channel count)
# , instead of ; in header
# Tabs ####
# content reports
# location reports
# display reports
# MULTI-SELECT FOR ALL
# for multi-select for location, content on the left, display, serial in that order


