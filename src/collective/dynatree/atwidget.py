from z3c.json.converter import JSONWriter
from AccessControl import ClassSecurityInfo
from Products.Five.browser import BrowserView
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.utils import OrderedDict

class DynatreeWidgetMacros(BrowserView):
    """
    A little view class just for ajax calls
    """
    @property
    def macros(self):
        return self.index.macros


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
    
    security = ClassSecurityInfo()
    
    def dynatreeParameters(self):
        result = [('%s,%s' % (_, self._properties[_])) 
                  for _ in ['select', 'minExpandLevel', 'rootvisible', 
                            'autocollapse']]        
        return ';'.join(result)

registerWidget(DynatreeWidget,
               title='Dynatree',
               description=('Renders a tree with selected items '
                            'Allows selection of more items via pop up'),
               used_for=('Products.Archetypes.Field.StringField',
                         'Products.Archetypes.Field.LinesField')
)