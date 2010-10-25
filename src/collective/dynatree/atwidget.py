from z3c.json.converter import JSONWriter
from Products.Five.browser import BrowserView
from Products.Archetypes import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.utils import OrderedDict

class ATFieldVocabDynatreeJsonView(BrowserView):
    
    def __call__(self):
        fieldname = self.request.get('fieldname')
        field = self.context.Schema()[fieldname]
        if IVocabulary.providedBy(field.vocabulary):
            tree = field.vocabulary.getVocabularyDict(self.context)
        else:
            vocab = field.Vocabulary(self.context)
            tree = OrderedDict()
            for key in vocab:
                tree[key] = vocab.getValue(key)
        return JSONWriter().write(dict2dynatree(tree, selected, ))
    
class DynatreeWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({'macro' : 'at_widget_dynatree',
                        'select': 'leafs', # 'leafs' or 'all'
                        'minExpandLevel': 1,
                        'rootvisible': False,
                        'autocollapse': False})

registerWidget(DynatreeWidget,
               title='Dynatree',
               description=('Renders a tree with selected items '
                            'Allows selection of more items via pop up'),
               used_for=('Products.Archetypes.Field.LinesField',)
)