from setuptools import setup
import pipext
import sys

ver = sys.version_info
ver = '.'.join(map(str,[ver.major,ver.minor]))

setup(name = 'pipext',
      version = pipext.__version__,
      description = 'Expanding the functionality of pip',
      long_description = open("README.rst").read(),
      author = 'Garry Galler',
      author_email = 'ggaller@mail.ru',
      license = 'MIT',
      keywords = 'pip extension upgrade',
      py_modules = ['pipext'],
      entry_points = {'console_scripts':['pipext = pipext:main','pipext' + ver + ' = pipext:main']},
      include_package_data = True,
      install_requires = ['pip>=10.0.0']
      )
