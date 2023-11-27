from jellyfish import damerau_levenshtein_distance # cSpell:disable-line
from natsort import natsorted #cSpell:disable-line

# string isnumeric()

def determine_sequence__(string: str) -> str:
    for x in reversed(range(1,4)):
        sequence = string[-x:]
        if (sequence.isnumeric()):
            return string[:-x]
    return string
    
def group_sequence_strings(strings):
    """
        Finds string sequences and put them in a list of lists.
    """
    strings_list = []
    first_string = ""
    first_sequence = ""
    string_list_index = 0
    organized_strings = natsorted(strings) # cSpell:disable-line
    for string in organized_strings:
        index = organized_strings.index(string)
        sequence = determine_sequence__(string)
        if (index == 0):
            first_string = string
            strings_list.append([])
            strings_list[0].append(string)
            first_sequence = sequence
            continue
        differences_strings = damerau_levenshtein_distance(first_sequence,sequence) # cSpell:disable-line
        if (differences_strings == 0):
            strings_list[string_list_index].append(string)
        else:
            first_string = string
            strings_list.append([])
            string_list_index = string_list_index + 1
            strings_list[string_list_index].append(string)
            first_sequence = sequence
            continue
    return strings_list
