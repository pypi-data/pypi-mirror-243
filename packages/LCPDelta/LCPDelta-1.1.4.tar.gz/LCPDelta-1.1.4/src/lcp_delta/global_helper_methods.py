def is_list_of_strings(lst):
    if not isinstance(lst, list):
        return False
    return all(isinstance(item, str) for item in lst)
