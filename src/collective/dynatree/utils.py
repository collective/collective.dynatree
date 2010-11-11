def dict2dynatree(input_dict, selected, leafsOnly):
    """
    Recursively parse the dictionary as we get it from the
    IVocabulary, and transform it to a a dictionary as needed for
    dynatree
    """
    if input_dict is None:
        return []
    retval = []
    for key in input_dict:
        title, children = input_dict[key]
        children = dict2dynatree(children, selected, leafsOnly)

        new_item = {} #we have to have boolItems
        new_item['title'] = title
        new_item['key'] = key
        new_item['children'] = children
        new_item['select'] = key in selected
        new_item['isFolder'] = bool(children)
        new_item['hideCheckbox'] = bool(children) and leafsOnly
        new_item['expand'] = key in selected or isSomethingSelectedInChildren(children, selected)
        retval.append(new_item)
    return retval


def isSomethingSelectedInChildren(children, selected):
    return bool(set([_['key'] for _ in children]).intersection(selected)) \
        or bool([_ for _ in children
            if _['children'] and isSomethingSelectedInChildren(_['children'], selected)])
        
        
# if isSomethingSelected in children level 1