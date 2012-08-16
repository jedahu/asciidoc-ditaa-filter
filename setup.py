from distutils.core import setup

setup(
    name='asciidoc-ditaa-filter',
    version='1.2-jedahu',
    author='Jeremy Hughes',
    author_email='jed@jedatwork.com',
    packages=['asciidoc_ditaa_filter'],
    url='https://github.com/jedahu/asciidoc-ditaa-filter',
    license='GPL2',
    description='In-process ditaa filter for AsciiDoc-jedahu.',
    long_description=open('README').read(),
    package_data={'asciidoc_ditaa_filter': ['filter.conf','ditaa0_9.jar']},
    include_package_data=True
    )
