from setuptools import setup, find_packages

version = '2.0.0a'

long_description = (
    open('README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='dexterity.localrolesfield',
    version=version,
    description="z3c.form local role field for dexterity",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 6.0",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='Plone Python',
    author='IMIO',
    author_email='support@imio.be',
    url="https://github.com/collective/dexterity.localrolesfield",
    project_urls={
        "PyPI": "https://pypi.python.org/pypi/dexterity.localrolesfield",
        "Source": "https://github.com/collective/dexterity.localrolesfield",
        # "Tracker": (
        #     "https://github.com/collective/dexterity.localroles/issues"
        # ),
    },
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['dexterity', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.CMFCore',
        'collective.z3cform.datagridfield',
        'dexterity.localroles>=2.0.0.dev0',
        'plone.api',
        'plone.app.dexterity',
        'setuptools',
        'z3c.unconfigure',
    ],
    extras_require={
        'test': [
            'plone.api',
            'plone.app.testing',
            'plone.app.robotframework',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    """,
)
