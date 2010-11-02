def dict2dynatree(input_dict, selected, leafsOnly):
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
        children = dict2dynatree(children, selected, leafsOnly)
        new_item = {}
        new_item['title'] = title
        new_item['key'] = key
        new_item['children'] = children
        new_item['hideCheckbox'] = False
        if key in selected:
            new_item['select'] = True
        if children:
            new_item['isFolder'] = True
        if children and leafsOnly:
            new_item['hideCheckbox'] = True

        #new_item['expand'] = expanded
        retval.append(new_item)
    return retval