from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.utils import OrderedDict

def dict2dynatree(input_dict, selected, only_leaves, showKey=False):
    """
    Recursively parse the dictionary as we get it from the
    IVocabulary, and transform it to a a dictionary as needed for
    dynatree
    input_dict:
        dictionary as provided by getVocabularyDict from 
        Products.ATVocabularyManager
    selected:
        List of keys that should be preselected
    only_leaves:
        Whether only leafes should be selectable or also tree nodes
    showKey:
        Whether the title should start with the key or not
    """
    if not input_dict:
        return []
    retval = []
    for key in input_dict.keys():
        children = dict2dynatree(input_dict[key], selected, only_leaves, showKey)

        new_item = {}  # we have to have boolItems
        new_item['title'] = key.value
        new_item['key'] = key.token
        new_item['children'] = children
        new_item['select'] = key.token in selected
        new_item['isFolder'] = bool(children)
        new_item['hideCheckbox'] = bool(children) and only_leaves
        new_item['expand'] = (key.token in selected or
                              isSomethingSelectedInChildren(children,
                                                            selected))
        retval.append(new_item)
    return retval

def atvocabularydict2dynatree(input_dict, selected, leafsOnly, showKey=False):
    """
    Recursively parse the dictionary as we get it from the
    IVocabulary, and transform it to a a dictionary as needed for
    dynatree
    input_dict:
        dictionary as provided by getVocabularyDict from 
        Products.ATVocabularyManager
    selected:
        List of keys that should be preselected
    leafsOnly:
        Whether only leafes should be selectable or also tree nodes
    showKey:
        Whether the title should start with the key or not
    """
    if not input_dict:
        return []
    retval = []
    for key in input_dict.keys():
        title, children = input_dict[key]
        children = atvocabularydict2dynatree(children, selected, leafsOnly, showKey)

        new_item = {}  # we have to have boolItems
        if showKey:
            title = "(%s) %s" % (key, title)
        new_item['title'] = title
        new_item['key'] = key
        new_item['children'] = children
        new_item['select'] = key in selected
        new_item['isFolder'] = bool(children)
        new_item['hideCheckbox'] = bool(children) and leafsOnly
        new_item['expand'] = (key in selected or
                              isSomethingSelectedInChildren(children,
                                                            selected))
        retval.append(new_item)
    return retval


def isSomethingSelectedInChildren(children, selected):
    return bool(set([_['key'] for _ in children]).intersection(selected)) \
        or bool([_ for _ in children
            if _['children'] and isSomethingSelectedInChildren(
                    _['children'], selected)])


def lookupVocabulary(context, field):
    if IVocabulary.providedBy(field.vocabulary):
        return field.vocabulary.getVocabularyDict(context)
    else:
        vocab = field.Vocabulary(context)
        tree = OrderedDict()
        for key in vocab:
            tree[key] = vocab.getValue(key)
        return tree
