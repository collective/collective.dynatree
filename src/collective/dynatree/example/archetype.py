from Products.Archetypes.atapi import *
from Products.Archetypes.config import PKG_NAME
from AccessControl import ClassSecurityInfo
from Products.ATVocabularyManager import NamedVocabulary
from collective.dynatree.atwidget import DynatreeWidget

schema = BaseSchema + Schema((
    StringField('single_leafs',
        required=0,
        vocabulary=NamedVocabulary('ch.scb.disposition'),
        widget=DynatreeWidget(
            description="Select one option of tree. Only leafs allowed",
            leafsOnly=True,
            selectMode=1),
    ),
    StringField('single_all',
        required=0,
        vocabulary=NamedVocabulary('ch.scb.disposition'),
        widget=DynatreeWidget(
            description="""Select one option of tree. Nodes allowed too.
                           Autocollapse is switched on.""",
            selectMode=1,
            rootVisible=True,
            autoCollapse=True),
    ),
    LinesField('multiple_leafs',
        required=0,
        vocabulary=NamedVocabulary('ch.scb.disposition'),
        widget=DynatreeWidget(
            description="""Select multiple options of tree. Leafs only.""",
            leafsOnly=True,
            selectMode=2),
    ),
    LinesField('multiple_all',
        required=0,
        vocabulary=NamedVocabulary('ch.scb.disposition'),
        widget=DynatreeWidget(
            description="""Select multiple options of the tree. All selectable.
                           Starts with 2 levels expanded.""",
            selectMode=3,
            minExpandLevel=2),
    ),
))


class DynatreeExample(BaseContent):
    """A simple archetype"""
    schema = schema
    security = ClassSecurityInfo()
    meta_type = 'DynatreeExample'



registerType(DynatreeExample, 'collective.dynatree.example')