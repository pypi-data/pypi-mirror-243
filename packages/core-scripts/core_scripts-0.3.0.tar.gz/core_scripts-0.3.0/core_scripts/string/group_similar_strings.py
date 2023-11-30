from jellyfish import damerau_levenshtein_distance # cSpell:disable-line
from natsort import natsorted #cSpell:disable-line

def group_similar_strings(strings,differences_number):
    """
        Finds similar strings and put it in a list of lists.
    """
    strings_list = []
    first_string = ""
    string_list_index = 0
    organized_strings = natsorted(strings) # cSpell:disable-line
    for string in organized_strings:
        index = organized_strings.index(string)
        if (index == 0):
            first_string = string
            strings_list.append([])
            strings_list[0].append(string)
            continue
        differences_strings = damerau_levenshtein_distance(first_string,string) # cSpell:disable-line
        if (differences_strings < differences_number):
            strings_list[string_list_index].append(string)
        else:
            first_string = string
            strings_list.append([])
            string_list_index = string_list_index + 1
            strings_list[string_list_index].append(string)
            continue
    return strings_list
