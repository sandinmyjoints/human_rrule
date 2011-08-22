from distutils.core import setup

from rrule2text import get_version

setup(name='rrule2text',
      version=get_version().replace(' ', '-'),
      author="William Bert",
      author_email="william.bert@gmail.com",
      packages=['rrule2text'],
      package_dir={'rrule2text': 'rrule2text'},
      requires=['dateutil(>=1.5, <2.0)'],
      provides=['rrule2text'],
      )