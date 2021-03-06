from setuptools import setup, find_packages
from os.path import join

name = 'sd.imaging'
path = name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()
readme = open("README.txt").read()
history = open(join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

setup(name = name,
      version = version,
      description = 'Structured Document Imaging Module',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'plone portlet zope structureddocument',
      author = 'Souheil Chelfouh',
      author_email = 'souheil@chelfouh.com',
      url = 'http://tracker.trollfot.org/wiki/StructuredDocument',
      download_url = 'http://pypi.python.org/pypi/sd.imaging',
      license = 'GPL',
      packages = find_packages(),
      namespace_packages = ['sd'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires=[
          'sd.common >= 0.6',
          'setuptools',
          'zope.annotation',
          'zope.component',
          'zope.event',
          'zope.formlib',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.publisher',
          'zope.schema',
      ],
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
