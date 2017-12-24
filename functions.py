def convert_to_list(dictionary):
    """
    Takes a dictionary and converts it to 
    a 2d list with key in index 0 and value
    in index 1.

    :param dictionary: any dictionary
    :return: lst[lst[]]
    """

    lst = []
    for key in dictionary:
        lst.append([key, dictionary[key]])

    return lst 