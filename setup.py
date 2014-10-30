from setuptools import setup, find_packages
import os

version = '2.0'
shortdesc = 'jquery.dynatree.js integration for Plone'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc = open(os.path.join(os.path.dirname(__file__), 'CHANGES.rst')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.rst')).read()

setup(
    name='collective.dynatree',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='jquery dynatree Zope Plone Archetypes Dexterity Widget tree '
             'vocabulary',
    author='BlueDynamics Alliance, et al.',
    author_email='dev@bluedynamics.com',
    url=u'https://github.com/collective/collective.dynatree',
    license='GNU General Public Licence',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.schema >= 4.1dev',
        'Plone',
        'plone.behavior',
        'collective.js.jqueryui',
        'collective.js.backbone',
    ],
    extras_require=dict(
        at_example=['Products.ATVocabularyManager'],
        dx_example=['plone.app.contenttypes',
                    'collective.vdexvocabulary'],
        test=['ipdb', 'interlude', ],
    ),
    entry_points={
        'z3c.autoinclude.plugin': 'target = plone',
    },
)
