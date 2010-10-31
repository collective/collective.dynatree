from z3c.json.converter import JSONWriter
from AccessControl import ClassSecurityInfo
from Products.Five.browser import BrowserView
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.interfaces import IVocabulary
from Products.Archetypes.utils import OrderedDict
from utils import dict2dynatree

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
        selected = []
        if tree is None:
            import pdb;pdb.set_trace()
        return JSONWriter().write(dict2dynatree(tree, selected))
    
class DynatreeWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({'macro' : 'at_widget_dynatree',
                        'selectMode': 1, # 1=single, 2=multi, 3=multi-hier(?)                      
                        'minExpandLevel': 1,
                        'rootVisible': False,
                        'autoCollapse': False,
                        'minExpandLevel': 0})
    
    security = ClassSecurityInfo()
    
    security.declarePublic('dynatreeParameters')
    def dynatreeParameters(self):
        result = [('%s,%s' % (_, getattr(self, _))) 
                  for _ in ['selectMode', 'minExpandLevel', 'rootVisible', 
                            'autoCollapse']]
        result.append('title,%s' % self.label)
        return '/'.join(result)
    
    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """get values from form field"""
        value = form.get(field.getName(), empty_marker)
        if value is empty_marker:
            return empty_marker
        if emptyReturnsMarker and value == '':
            return empty_marker
        if value == '()':
            return empty_marker
        value = value.strip("|")
        if self.selectMode > 1:
            value = value.split('|')
        return value, {}
    
registerWidget(DynatreeWidget,
               title='Dynatree',
               description=('Renders a tree with selected items '
                            'Allows selection of more items via pop up'),
               used_for=('Products.Archetypes.Field.StringField',
                         'Products.Archetypes.Field.LinesField')
)