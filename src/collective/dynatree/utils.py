from Acquisition import aq_acquire
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.utils import OrderedDict
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import ITokenizedTerm
from zope.schema.interfaces import ITreeVocabulary

def _translate(context, msg):
    """helper to translate a term if its a messageid
    """
    if not isinstance(msg, Message):
        return msg
    if not IBrowserRequest.providedBy(context):
        context = aq_acquire(context, 'REQUEST')
    msg = translate(msg, context=context).strip()
    msg = '\n'.join([_.strip() for _ in msg.split('\n')])  # needed if vdex
    return msg


def dict2dynatree(context, source, selected, only_leaves, show_key=False):
    """
    Recursively parse the dictionary as we get it from the IVocabulary,
    and transform it to a a dictionary as needed for dynatree.

    source:
        dictionary as provided by getVocabularyDict from
        Products.ATVocabularyManager or a zope.schema.interfaces.ITreeVocabulary
    selected:
        List of keys that should be preselected
    only_leaves:
        Whether only leaves should be selectable or also tree nodes
    """
    if not source:
        return []

    if not ITreeVocabulary.providedBy(source) and not isinstance(source, dict):
        raise ValueError("Source must either be dict or treevocabulary")

    retval = []
    for key in source:
        description = None
        if ITokenizedTerm.providedBy(key):
            subtree = source[key]
            title = key.title or key.value
            if hasattr(key, 'description'):
                description = key.description
            key = key.token
        else:  # dict
            title, subtree = source[key]

        title = _translate(context, title)
        description = _translate(context, description)

        children = dict2dynatree(
            context,
            subtree,
            selected,
            only_leaves,
            show_key
        )

        if show_key:
            title = "(%s) %s" % (key, title)

        record = {}
        record['title'] = title
        if description is not None:
            record['tooltip'] = description
        record['key'] = key
        record['children'] = children
        record['select'] = key in selected
        record['isFolder'] = bool(children)
        record['hideCheckbox'] = bool(children) and only_leaves
        record['expand'] = key in selected or \
                           isSomethingSelectedInChildren(children, selected)
        retval.append(record)
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
