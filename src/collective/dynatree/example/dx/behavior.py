from plone.supermodel import model
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from collective.dynatree.dxwidget import DynatreeWidget
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IDynatreeExampleBehavior(model.Schema):

    widget(
        'multiple_leafs',
        DynatreeWidget,
        selectMode=2
    )
    single_leafs = schema.Choice(
        title=u"Singe Leafs",
        required=False,
        vocabulary="ch.scb.disposition",
    )

    widget(
        'single_leafs',
        DynatreeWidget,
        selectMode=2
    )
    multiple_leafs = schema.List(
        title=u"Multiple Leafs",
        required=False,
        value_type=schema.Choice(
            vocabulary="ch.scb.disposition",
        )
    )
