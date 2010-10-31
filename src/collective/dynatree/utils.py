def dict2dynatree(input_dict, selected):
    """
    Recursively parse the dictionary as we get it from the
    IVocabulary, and transform it to a a dictionary as needed for
    dynatree
    """
    if input_dict is None:
        return None
    retval = []
    for key in input_dict:
        title, children = input_dict[key]
        children = dict2dynatree(children, selected)
        new_item = {}
        new_item['title'] = title
        new_item['key'] = key
        new_item['children'] = children
        #new_item['expand'] = expanded
        retval.append(new_item)
    return retval