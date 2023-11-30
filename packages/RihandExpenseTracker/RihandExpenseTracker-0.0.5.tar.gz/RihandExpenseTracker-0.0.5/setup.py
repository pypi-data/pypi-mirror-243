from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='convertcurrency',
  version='0.0.5',
  description='A basic currency converter',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Rihand Parde',
  author_email='rihand.parde@gmail.com',
  classifiers=classifiers,
  keywords='currency converter', 
  packages=find_packages(),
  install_requires=[''] 
)