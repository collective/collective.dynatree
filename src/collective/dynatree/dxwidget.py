from Acquisition import aq_inner
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.interfaces import IDexterityFTI
from Products.Five.browser import BrowserView
from utils import dict2dynatree
from z3c.form.widget import SequenceWidget
from z3c.json.converter import JSONWriter

from zope.dottedname.resolve import resolve
from zope.schema.interfaces import IList
from zope.schema.interfaces import IVocabularyFactory

import interfaces
import z3c.form
import zope.component
import zope.interface

class FieldVocabDynatreeJsonView(BrowserView):

    def __call__(self):
        context = aq_inner(self.context)
        fieldname = self.request.get('fieldname')
        portal_type = self.request.get('portal_type')

        fti = zope.component.getUtility(IDexterityFTI, name=portal_type)
        schema = fti.lookupSchema()
        field = schema.get(fieldname)
        if field is None:
            for behaviorname in fti.behaviors:
                behavior = resolve(behaviorname)
                field = behavior.get(fieldname.split('.')[1])
                if field is not None:
                    break
        if IList.providedBy(field):
            vname = field.value_type.vocabularyName
        else:
            vname = field.vocabularyName
        factory = zope.component.getUtility(IVocabularyFactory, vname)
        tree = factory(context)
        tree = dict2dynatree(
            self.context,
            tree,
            [],  # selected not needed here, this is done at js side
            True,
            False
        )
        return JSONWriter().write(tree)


class DynatreeWidget(SequenceWidget):
    """ A text field widget with a dynatree javascript vocabulary to determine
        the value.
    """
    zope.interface.implementsOnly(interfaces.IDynatreeWidget)
    klass = u'dynatree-widget'
    selectMode = 1
    minExpandLevel = 1
    autoCollapse = False
    leafsOnly = True
    showKey = False

    @property
    def widget_value(self):
        # XXX figure out where to get actual value from, workaround follows:
        # imo this should be self.value, but this is None. Reason?
        # anyway needs refactoring
        # also look if this method shall be named displayValue (z3cform style)
        try:
            value = self.field.get(self.context) or []
        except AttributeError:
            value = []
        # end of workaround XXX
        value = '|'.join([_ for _ in value])
        return self.request.get(self.__name__, value)

    def extract(self, default=z3c.form.interfaces.NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        if self.name not in self.request:
            return []
        value = self.request.get(self.name, default)
        if not isinstance(value, basestring):
            raise ValueError('Expected string, got %s' % type(value))
        if value == default:
            return value
        if IList.providedBy(self.field):
            value = value.split('|')
            # do some kind of validation, at least only use existing values
            for token in value:
                try:
                    self.terms.getTermByToken(token)
                except LookupError:
                    # XXX TODO remove value from list instead of skipping all
                    return default
        else:
            try:
                self.terms.getTermByToken(value)
            except LookupError:
                return default
        return value

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
                                    'autoCollapse']]
        result.append('title,%s' % self.label)
        return '/'.join(result)


@zope.component.adapter(zope.schema.TextLine, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def DynatreeFieldWidget(field, request):
    """ IFieldWidget factory for DynatreeWidget
    """
    return z3c.form.widget.FieldWidget(field, DynatreeWidget(request))
