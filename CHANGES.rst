Changes
=======

----------------
2.0 (2014-10-30)
----------------

- Several enhancements and minor bug fixes.
  [regebro]

- Bunch of fixes for z3cform widget, example types for dx, integration with
  fixed tree vocabularies of ``collective.vdexvocabulary`` and more polishing.
  Updated to latest ``jquery.dynatree``. Some renamings (attention, imports are
  changing slightly).
  [jensens, bennyboy, 2014-01-27]

- Add a z3c.form dynatree widget.
  [jbeyers, thomas_w, jcbrand 2012-02-08]

------------------
1.3.4 (2011-03-31)
------------------

- for some cases we need to explicit iterate over .keys() - thanks to Jess Hix
  for the patch, jensens 2011-03-31

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
