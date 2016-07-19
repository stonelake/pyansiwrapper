#!/usr/bin/env python

from setuptools import setup
from pip import req

install_reqs = req.parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]


setup(name='pyansiwrapper',
      author='Oleksii Baranov',
      author_email='aleksey.baranov@gmail.com',
      description='Simple python wrapper fot Ansible API',
      license='MIT',
      version='1.0.0',
      packages=['pyansiwrapper'],
      install_requires=reqs,
      )
