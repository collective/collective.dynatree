import zope.component
import zope.interface
import z3c.form
from z3c.json.converter import JSONWriter
from Products.Five.browser import BrowserView
from utils import dict2dynatree
import interfaces

from Products.ATVocabularyManager import NamedVocabulary

class FieldVocabDynatreeJsonView(BrowserView):

    def __call__(self):
        fieldname = self.request.get('fieldname')
        #field = self.context.schema[fieldname]
        # TODO: This is hardcoded, Incredibly stupid, needs to change.
        from staralliance.types.config import PRODUCTCATEGORIES
        atv = NamedVocabulary(PRODUCTCATEGORIES)
        tree = atv.getVocabularyDict(self.context)
        selected = self.request.get('selected', []).split('|')
        return JSONWriter().write(dict2dynatree(tree, selected,
                                                True,
                                                False))

class DynatreeWidget(z3c.form.browser.text.TextWidget):
    """ A text field widget with a dynatree javascript vocabulary to determine 
        the value.
    """
    zope.interface.implementsOnly(interfaces.IDynatreeWidget)
    klass = u'dynatree-widget'
    selectMode = 1
    minExpandLevel = 0
    rootVisible = False
    autoCollapse = False
    leafsOnly = True
    showKey = False
    atvocabulary = None

    def dynatree_parameters(self):
        result = [('%s,%s' % (parameter, getattr(self, parameter)))
                  for parameter in ['selectMode',
                                    'minExpandLevel',
                                    'rootVisible',
                                    'autoCollapse']]
        result.append('title,%s' % self.label)
        return '/'.join(result)

    def dynatree_value(self, value):
        if isinstance(value, basestring):
            return value
        if isinstance(value, (tuple, list)):
            return '|'.join(value)
        return ''

@zope.component.adapter(zope.schema.TextLine, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def DynatreeFieldWidget(field, request):
    """ IFieldWidget factory for DynatreeWidget
    """
    return z3c.form.widget.FieldWidget(field, DynatreeWidget(request))

