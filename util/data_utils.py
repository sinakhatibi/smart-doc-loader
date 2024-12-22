from collections import defaultdict

# a function to merge a dictionary to another dictionary
# if the key exists in the original dictionary, the values are appended to the list
# if the key does not exist in the original dictionary, the key and value are added to the dictionary
# the function returns the merged dictionary
# the function takes two dictionaries as arguments
# the function returns a dictionary
# the function uses the defaultdict class from the collections module to create a dictionary with default values as lists
# the function loops over the items in the first dictionar
def merge_dictionaries(dict1, dict2):
    merged_dict = defaultdict(list)
    
    for key, value in dict1.items():
        merged_dict[key].extend(value if isinstance(value, list) else [value])
    
    for key, value in dict2.items():
        merged_dict[key].extend(value if isinstance(value, list) else [value])
    
    return dict(merged_dict)

# a function to append a dictionary to another dictionary 
def append_dictionaries(dict1, dict2):
    new_dict = merge_dictionaries(dict1, dict2)
    dict1.clear()
    dict1.update(new_dict)
