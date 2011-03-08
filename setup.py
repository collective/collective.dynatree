from setuptools import setup, find_packages
import os

version = "1.3.2"
shortdesc = 'jquery.dynatree.js integration for Plone'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(name='collective.dynatree',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
      ],
      keywords='jquery dynatree Zope Plone Archetypes Widget tree vocabulary',
      author='BlueDynamics Alliance, et al.',
      author_email='dev@bluedynamics.com',
      url=u'https://github.com/collective/collective.dynatree',
      license='GNU General Public Licence',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'collective.js.jqueryui',
          'z3c.json',          
      ],
      extras_require = dict(
          example=['Products.ATVocabularyManager'],
      ),
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """      
)
