from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.utils import OrderedDict

def dict2dynatree(input_dict, selected, leafsOnly, showKey):
    """
    Recursively parse the dictionary as we get it from the
    IVocabulary, and transform it to a a dictionary as needed for
    dynatree
    """
    if not input_dict:
        return []
    retval = []
    for key in input_dict.keys():
        title, children = input_dict[key]
        children = dict2dynatree(children, selected, leafsOnly, showKey)

        new_item = {} #we have to have boolItems
        if showKey:
            title = "%s %s" % (key, title)
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
        
def lookupVocabulary(context, field):
    if IVocabulary.providedBy(field.vocabulary):
        return field.vocabulary.getVocabularyDict(context)
    else:
        vocab = field.Vocabulary(context)
        tree = OrderedDict()
        for key in vocab:
            tree[key] = vocab.getValue(key)
        return tree
