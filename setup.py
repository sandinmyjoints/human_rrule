from distutils.core import setup

from human_rrule import get_version

setup(name='human_rrule',
      version=get_version().replace(' ', '-'),
      author="William Bert",
      author_email="william.bert@gmail.com",
      packages=['human_rrule'],
      package_dir={'human_rrule': 'human_rrule'},
      requires=['dateutil(>=1.5, <2.0)'],
      provides=['human_rrule'],
      )