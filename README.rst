Dynamic Tree-Widget for Plone
=============================

collective.dynatree provides the basic integration of the jQuery plugin
`jquery.dynatree.js <http://wwwendt.de/tech/dynatree/index.html>`_ (at
`google-code <http://code.google.com/p/dynatree/>`_).

Optional it also provides a full-featured Archetypes Widget with full
ATVocabularyManager support, including hierachical VDEX-vocabularies.

.. image:: http://bluedynamics.com/collective.dynatree.png

Installation
============

Just depend in your buildout on the egg ``collective.dynatree``. ZCML is loaded
automagically if z3c.autoinclude is available (default since Plone >=3.3).

Install it as an addon in Plone control-panel or portal_setup.

Usage
=====

--------------
Plain Dynatree
--------------

This package only provides and registers the javascript in the site. Addon
developers can use it then in their own templates. Please refer to the
`original documentation <http://wwwendt.de/tech/dynatree/doc/dynatree-doc.html>`_
for usage of ``jquery.dynatree.js``.

--------------------------
Dexterity/ z3c.form Widget
--------------------------

The widget is meant to be used on a ``Choice`` (single selection) or on a
``List`` or ``Set`` (multi selection).

Example dexterity behavior::

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
        multiple_leafs = schema.List(
            title=u"Multiple Leafs",
            required=False,
            value_type=schema.Choice(
                vocabulary="ch.scb.disposition",
            )
        )

For a complete example look at the code in folder
``src/collective/dynatree/example/dx``.


-----------------
Archetypes Widget
-----------------

The widget is meant to be used on a ``StringField`` (single selection) or on a
``LinesField`` (multi selection).

Example::

    StringField('single_leafs',
        required=0,
        vocabulary=NamedVocabulary('some_atvm_tree_vocabulary'),
        widget=DynatreeWidget(
            description="Select one option of tree. Only leafs allowed",
            leafsOnly=True,
            selectMode=1),
    ),
    LinesField('multiple_all',
        required=0,
        vocabulary=NamedVocabulary('another_atvm_tree_vocabulary'),
        widget=DynatreeWidget(
            description="""Select multiple options of the tree. All selectable.
                           Starts with 2 levels expanded.""",
            selectMode=3,
            minExpandLevel=2),
    ),

For a complete example look at the code in folder
``src/collective/dynatree/example/at``.


Widget Parameters
-----------------
(additional to the usal suspects of TypesWidget)

selectMode
    1=single, 2=multiple

minExpandLevel
    Number of levels which are not allowed to collapse; default=0.

autoCollapse
    Automatically collapse all siblings, when a node is expanded;
    default=False.

leafsOnly
    Wether to select only leafs or allow also to select nodes with leafs;
    default=False.

showKey
   To show the terms key in front of the terms value set this to a format
   string like ``"%s: %s"``; default=None. You can put HTML inside, ie.
   ``<span class="dynatree-key">%s</span>&ndash;<span class="dynatree-value">%s<span>``.
   Thus you can apply custom formats.

-------------------
Example-ContentType
-------------------

Example content-types are provided, but disabled by default. To enable it add
``collective.dynatree[at_example]`` and/or ``collective.dynatree[dx_example]``
to both, the eggs and zcml section in your buildout. Rerun buildout, restart
Plone and install the ``jquery.dynatree AT EXAMPLE Content Type`` and/or
``jquery.dynatree DX EXAMPLE Content Type`` as an add-on product.

Source Code and Contributions
=============================

If you want to help with the development (improvement, update, bug-fixing, ...)
of ``collective.dynatree`` this is a great idea!

The code is located in the
`github collective <https://github.com/collective/collective.dynatree>`_.

You can clone it or `get access to the github-collective
<http://collective.github.com/>`_ and work directly on the project.

Maintainers of collective.dynatree are Jens Klein and Peter Holzer. We
appreciate any contribution and if a release is needed to be done on pypi,
please just contact one of us.

Contributors
============

- Jens W. Klein <jens@bluedynamics.com>

- Peter Holzer <hpeter@agitator.com>

- Patrick Gerken provided initial idea+code with his package slc.treecategories

- Lennart Regebro

- and much more, see change-log for details.
