def dict2dynatree(input_dict, selected, keyFilter=None, fullTextFilter=None, 
                  sortkey=None, expanded=False, invert_key_limiter=False, 
                  display_ids=False):
    """
    Recursively parse the dictionary as we get it from the
    IVocabulary, and transform it to a a dictionary as needed for
    dynatree
    """
    if input_dict is None:
        return None
    retval = []
    input_list = input_dict.items()

    if sortkey:
        input_list = sorted(input_list, key=sortkey)
    for key, (title, children) in input_list:
        # if we inverted the key limiter, we dont want a node to appear if
        # he is filtered, even if he has children!
        if invert_key_limiter \
           and keyFilter \
           and not keyFilter(key):
            continue
        children = dict2dynatree(children, keyFilter, fullTextFilter, sortkey,
                                 expanded, invert_key_limiter, display_ids)
        if not children \
           and keyFilter \
           and not keyFilter(key):
            continue
        if not children \
           and fullTextFilter \
           and not fullTextFilter(title):
            continue
        new_item = {}
        if display_ids:
            title = '%s (%s)' % (title, key)
        else:
            title = title
        new_item['title'] = title
        new_item['key'] = key
        new_item['children'] = children
        new_item['expand'] = expanded
        retval.append(new_item)
    return retval