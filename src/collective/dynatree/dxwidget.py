from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone.dexterity.interfaces import IDexterityFTI
from utils import dict2dynatree
from z3c.form.widget import SequenceWidget
from zope.dottedname.resolve import resolve
from zope.schema import TextLine
from zope.schema.interfaces import IList, ISet
from zope.schema.interfaces import IVocabularyFactory
import interfaces
import json
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
        if IList.providedBy(field) or ISet.providedBy(field):
            vname = field.value_type.vocabularyName
        else:
            vname = field.vocabularyName
        factory = zope.component.getUtility(IVocabularyFactory, vname)
        tree = factory(context)
        leafsOnly = getattr(tree, 'leafsOnly', True)
        
        tree = dict2dynatree(
            self.context,
            tree,
            [],  # selected not needed here, this is done at js side
            leafsOnly,
            False
        )
        return json.dumps(tree)


class DynatreeWidget(SequenceWidget):
    """ A text field widget with a dynatree javascript vocabulary to determine
        the value.
    """
    zope.interface.implementsOnly(interfaces.IDynatreeWidget)
    klass = u'dynatree-widget'
    selectMode = 1
    minExpandLevel = 1
    autoCollapse = False
    leafsOnly = True # Not used
    showKey = False # Not used

    def _get_term(self, token):
        try:
            return self.terms.getTermByToken(token)
        except LookupError:
            return None
            
    @property
    def item_value(self):
        # XXX figure out where to get actual value from, workaround follows:
        # imo this should be self.value, but this is None. Reason?
        # anyway needs refactoring
        # also look if this method shall be named displayValue (z3cform style)
        try:
            return self.field.get(self.context) or []
        except AttributeError:
            return []

    @property
    def widget_value(self):
        # Returns the value in a form useful for the edit widget, ie with
        # items separated by |
        value = self.item_value
        if not isinstance(value, basestring):
            value = '|'.join([_ for _ in value])
        return self.request.get(self.__name__, value)
    
    def term_display_value(self, term):
        if term is None:
            return ''
        parent = getattr(term, '__parent__', None)
        if parent:
            parent_title = self.term_display_value(parent)
            return '%s / %s' % (parent_title, term.title)
        return term.title
        
    @property
    def display_value(self):
        # Returns the title of all values if the field is a string, or a list of titles otherwise.
        value = self.item_value
        if isinstance(value, basestring):
            term = self._get_term(value)
            return self.term_display_value(term)
            
        terms = [self._get_term(token) for token in value]
        return sorted(self.term_display_value(term) for term in terms)

    def extract(self, default=z3c.form.interfaces.NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        if self.name not in self.request:
            return []
        value = self.request.get(self.name, default)
        if not isinstance(value, basestring):
            raise ValueError('Expected string, got %s' % type(value))
        if value == default:
            return value
        value = value.split('|')
        for token in value:
            if token == self.noValueToken:
                continue
            try:
                self.terms.getTermByToken(token)
            except LookupError:
                # XXX TODO remove value from list instead of skipping all
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
        result = [r.replace('/', '&#47;') for r in result]
        return '/'.join(result)


@zope.component.adapter(TextLine, z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def DynatreeFieldWidget(field, request):
    """ IFieldWidget factory for DynatreeWidget
    """
    return z3c.form.widget.FieldWidget(field, DynatreeWidget(request))
