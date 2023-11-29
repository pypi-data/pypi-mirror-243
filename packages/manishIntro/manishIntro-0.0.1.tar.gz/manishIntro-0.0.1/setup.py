from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: POSIX :: Linux',
  'Operating System :: MacOS :: MacOS X',
  'License :: OSI Approved :: GNU General Public License (GPL)',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='manishIntro',
  version='0.0.1',
  description='A python module for Intorducing Manish', 
  author='Manish Kumar',
  author_email='officialmanishkr98@gmail.com',
  license='GNU', 
  classifiers=classifiers,
  keywords=['manish','sayHi'], 
  packages=find_packages(),
  install_requires=[] 
)