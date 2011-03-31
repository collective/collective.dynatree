from z3c.json.converter import JSONWriter
from AccessControl import ClassSecurityInfo
from Products.Five.browser import BrowserView
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
#from Products.Archetypes.interfaces import IVocabulary
#from Products.Archetypes.utils import OrderedDict
from utils import dict2dynatree
from utils import isSomethingSelectedInChildren
from utils import lookupVocabulary

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
        tree = lookupVocabulary(self.context, field)        
        selected = self.request.get('selected', []).split('|')
        return JSONWriter().write(dict2dynatree(tree, selected, 
                                                field.widget.leafsOnly,
                                                field.widget.showKey))
    
class DynatreeWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({'macro' : 'at_widget_dynatree',
                        'selectMode': 1, # 1=single, 2=multi, 3=multi-hier(?)                      
                        'minExpandLevel': 0,
                        'rootVisible': False,
                        'autoCollapse': False,
                        'leafsOnly': False,
                        'showKey': False})

    
    security = ClassSecurityInfo()
    
    security.declarePublic('dynatreeParameters')
    def dynatreeParameters(self, instance, field):
        if getattr(self, 'rootVisible') == True \
               and getattr(self, 'minExpandLevel') == 0 \
               and field.get(instance):
            self.minExpandLevel = 1
            
        result = [('%s,%s' % (_, getattr(self, _))) 
                  for _ in ['selectMode', 'minExpandLevel', 'rootVisible', 
                            'autoCollapse']]
        result.append('title,%s' % self.label)
        return '/'.join(result)
    
    security.declarePublic('dynatreeValue')
    def dynatreeValue(self, value):
        if isinstance(value, basestring):
            return value
        if isinstance(value, (tuple, list)):
            return '|'.join(value)
        return ''     

    security.declarePublic('vocabLookup')
    def vocabLookup(self, instance, field, value):
        tree = lookupVocabulary(instance, field)
        def find(treepart):
            if treepart is None:
                return None
            if value in treepart:
                return treepart[value][0]
            for key in treepart.keys():
                result = find(treepart[key][1])
                if result is not None:
                    return result
            return None
        result = find(tree)
        if result is None:
             return u'NOT FOUND'
        return result
        
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
            value = [_ for _ in value.split('|') if _.strip()]
            if not value:
                return empty_marker
        return value, {}
    
registerWidget(DynatreeWidget,
               title='Dynatree',
               description=('Renders a tree with selected items '
                            'Allows selection of more items via pop up'),
               used_for=('Products.Archetypes.Field.StringField',
                         'Products.Archetypes.Field.LinesField')
)