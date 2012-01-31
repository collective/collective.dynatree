import zope.component
import zope.interface
from zope.schema.interfaces import IVocabularyFactory

from Acquisition import aq_inner

import z3c.form
from z3c.form.widget import SequenceWidget
from z3c.json.converter import JSONWriter

from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.interfaces import IDexterityFTI

from Products.Five.browser import BrowserView

from utils import dict2dynatree
import interfaces

class FieldVocabDynatreeJsonView(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        fieldname = self.request.get('fieldname')
        portal_type = self.request.get('portal_type')
        
        fti = zope.component.getUtility(IDexterityFTI, name=portal_type)
        schema = fti.lookupSchema()

        field = schema.get(fieldname)
        if field is None:
            # The field might be defined in a behavior schema
            behavior_assignable = IBehaviorAssignable(context, None)
            for behavior_reg in behavior_assignable.enumerateBehaviors():
                behavior_schema = IFormFieldProvider(behavior_reg.interface, None)
                if behavior_schema is not None:
                    field = behavior_schema.get(fieldname)
                    if field is not None:
                        break

        vname = field.vocabularyName
        factory = zope.component.getUtility(IVocabularyFactory, vname)
        tree = factory(context)
        # XXX: "selected" is not set in input.pt, so does it make sense to check
        # for it here? Only if this json view is called elsewhere, which
        # doesn't seem to be the case...
        selected = self.request.get('selected', '').split('|')
        return JSONWriter().write(dict2dynatree(tree, selected, True, False))


class DynatreeWidget(z3c.form.browser.widget.HTMLInputWidget, SequenceWidget):
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

    @property
    def widget_value(self):
        return self.request.get(self.__name__, '|'.join(v for v in self.value))

    @property
    def field_name(self):
        return self.__name__

    @property
    def portal_type(self):
        return self.form.portal_type

    def dynatree_parameters(self):
        result = [('%s,%s' % (parameter, getattr(self, parameter)))
                  for parameter in ['selectMode',
                                    'minExpandLevel',
                                    'rootVisible',
                                    'autoCollapse']]
        result.append('title,%s' % self.label)
        return '/'.join(result)


@zope.component.adapter(zope.schema.TextLine, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def DynatreeFieldWidget(field, request):
    """ IFieldWidget factory for DynatreeWidget
    """
    return z3c.form.widget.FieldWidget(field, DynatreeWidget(request))



