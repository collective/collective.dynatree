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

-----------------
Archetypes Widget
-----------------

The widget is meant to be used on a ``StringField`` (single selection) or on a 
``LinesField`` (multi selection).

Example
-------
::

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
    
Widget Parameters 
-----------------
(additional to the usal suspects of TypesWidget)

selectMode
    1=single, 2=multiple
    
minExpandLevel
    Number of levels which are not allowed to collapse; default=0.

rootVisible
    Wether a root node should be showed or not; default=False.

autoCollapse
    Automatically collapse all siblings, when a node is expanded; 
    default=False.

leafsOnly
    Wether to select only leafs or allow also to select nodes with leafs; 
    default=False.             

showKey
   To show the terms key in front of the terms value set this to a format 
   string like ``"%s: %s"``; default=None.
              
-------------------
Example-ContentType
-------------------

An example ContentType is provided, but disabled by default. To enable it add
``collective.dynatree[example]`` to both, the eggs and zcml section in your 
buildout. Rerun buildout, restart Plone and install the 
``jquery.dynatree EXAMPLE Content Types`` as an add-on product.  

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

Changes
=======

------------------
1.3.3 (2011-03-14)
------------------

- fixed JS bug with f****g IE. Ported solution used by hpeter at 
  ``yafowil.widget.dynatree`` witha regexp instead of trim, jensens 2011-03-14

------------------
1.3.2 (2011-03-08)
------------------

- fixed bug: css-registry merges css, so paths to skin were no longer relative. 
  Adding the resource part helps here. jensens 2011-03-08

------------------
1.3.1 (2011-02-18)
------------------

- fixed bug: ``required`` on multi-selection did not work. jensens 2011-02-18

- added ``showKey`` property to at-widget to show terms key in front of the 
  value. hpeter, jensens, 2010-01-18

----------------
1.3 (2011-01-19)
----------------

- upgraded jquery.dynatree from upstream to version 1.0.3. jensens 2011-01-19

- added ``showKey`` property to at-widget to show terms key in front of the value.
  hpeter, jensens, 2011-01-18

------------------
1.2.1 (2010-12-03)
------------------

- fighting with MANIFEST.in, to much was excluded and egg release broken.
  should now be better. jensens 2010-12-03

----------------
1.2 (2010-12-02)
----------------

- after submit and validation error keep the previous selected values.
  jensens, 2010-12-02

----------------
1.1 (2010-11-29)
----------------

- add MANIFEST.in, so ``*.rst`` gets included in the egg.
  jensens, 2010-11-29

- make dict2dynatree more robust after report by Rigel Di Scala, 
  jensens, 2010-11-29

----------------
1.0 (2010-11-22)
----------------

- Make it work (jensens, hpeter)
