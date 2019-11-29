from setuptools import setup

setup(name='advancedpwn',
      version='0.1',
      description='Extensions for pwntools',
      url='http://github.com/galli-leo/advancedpwn',
      author='Leonardo Galli',
      author_email='TODO',
      license='MIT',
      packages=['advancedpwn'],
      install_requires=[
          'pwntools',
      ],
      zip_safe=False)