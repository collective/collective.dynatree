from zope.interface.declarations import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary

class TreeVocabulary(SimpleVocabulary):
    """ Vocabulary that has a tree (i.e nested) structure.
    """

    def __init__(self, terms, *interfaces):
        """Initialize the vocabulary given a dict of terms.

        All keys and values (including nested ones) must be unique.

        gne or more interfaces may also be provided so that alternate
        widgets may be bound without subclassing.
        """
        self._terms = terms

        def by_attr(terms, _dict, attr, structure='flat'):
            """ A recursing method to construct either a flat dict where the 
            keys are all the nodes in the tree, or a nested dict that mirrors 
            the original tree.

            _dict:      The dictionary that will contain the data.
            attr:       Specifies the ISimpleTerm attribute that will be the 
                        keys of the _dict 
            structure: 'flat' or 'nested'
            """
            for term in terms.keys():
                if structure == 'nested':
                    _dict[getattr(term, attr)] = \
                            by_attr(terms[term], {}, attr, structure)
                elif structure == 'flat':
                    attrval = getattr(term, attr)
                    if attrval in _dict:
                        raise ValueError(
                            'term %ss must be unique: %s' \
                                % (attr, repr(attrval)))

                    _dict[attrval] = term
                    by_attr(terms[term], _dict, attr, structure)
            return _dict

        self.dict_by_value = by_attr(terms, {}, 'value', 'nested')
        self.by_value = by_attr(terms, {}, 'value', 'flat')
        self.by_token = by_attr(terms, {}, 'token', 'flat')

        if interfaces:
            directlyProvides(self, *interfaces)
             
    @classmethod
    def fromDict(cls, _dict, *interfaces):
        """Constructs a vocabulary from a dictionary with tuples as keys.
        The tuples can have 2 or three values, i.e: 
        (token, value, title) or (token, value)
        
        For example, a dict with 2-valued tuples:  

        _dict = {
            ('exampleregions', 'Regions used in ATVocabExample'): {
                ('aut', 'Austria'): {
                    ('tyr', 'Tyrol'): {
                        ('auss', 'Ausserfern'): {},
                    }
                },
                ('ger', 'Germany'): {
                    ('bav', 'Bavaria'):{}
                },
            }
        }
        One or more interfaces may also be provided so that alternate
        widgets may be bound without subclassing.
        """
        def createTree(tree, token, value, title, branch):
            """ """
            key = cls.createTerm(value, token, title)
            tree[key] = {}
            for _key in branch.keys():
                createTree(tree[key], _key[0], _key[1], _key[-1], branch[_key])

        tree = {}
        for key in _dict.keys():
            createTree(tree, key[0], key[1], key[-1], _dict[key])
        return cls(tree, *interfaces)

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        try:
            return self.by_value[value]
        except KeyError:
            raise LookupError(value)

    def getTermPath(self, value): 
        def recurse(_dict, value):
            if value in _dict.keys():
                return [value]
            path = []
            for key in _dict.keys():
                path = recurse(_dict[key], value)
                if path:
                    path.append(key)
                    break
            return path
        path = recurse(self.dict_by_value, value)
        path.reverse()
        return path


