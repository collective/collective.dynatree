from Products.Archetypes import listTypes
from Products.Archetypes.atapi import process_types
from Products.CMFCore.utils import ContentInit

def initialize(context):
    """initialize product (called by zope)"""
    import archetype

    # Initialize portal content
    content_types, constructors, ftis = process_types(
        listTypes('collective.dynatree.example'),
        'collective.dynatree.example')

    ci = ContentInit(
        'collective.dynatree.example content',
        content_types      = content_types,
        permission         = "Add portal content",
        extra_constructors = constructors,
        fti                = ftis,
    )
    ci.initialize(context)