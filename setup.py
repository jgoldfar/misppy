from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='misppy',
      version='1.0.0',
      description='Multiphase Stefan Problem Solver in Python',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      url='http://github.com/jgoldfar/misppy',
      keywords='differential equations stefan problem multiphase',
      author='Jonathan Goldfarb',
      author_email='jgoldfar@gmail.com',
      license='MIT',
      packages=['misppy','misppy.tests'],
      install_requires=['julia>=0.2'],
      include_package_data=True,
      zip_safe=False)
