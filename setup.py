from distutils.core import setup
import os

pkg_path = os.path.dirname(__file__)

README = os.path.join(pkg_path, 'README.md')
rm = open(README)
lines = rm.readlines()
description = ''.join(lines[:3])
long_description = ''.join(lines[:4])
rm.close()

vh = open('version', 'r')
lines = vh.readlines()
version = lines[-1].rstrip('\n').rstrip('\r')
vh.close()

setup(
    name='PyHRV',
    version=version,
    url='https://github.com/MPBA/pyHRV',
    description=description,
    long_description=long_description,
    keywords='HRV, heart, rate, variability, analysis, galaxy, project',
    author='FBK - MPBA',
    author_email='albattisti@fbk.eu',
    license='GNU GPL version 3',
    download_url='https://github.com/MPBA/pyHRV/archive/master.zip',
    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    requires=[
        'pandas (>= 0.13.1)',
        'numpy (>= 1.7.1)',
        'scipy (>= 0.12.0)'
    ],

    package_dir={'pyHRV': 'pyHRV'},
    packages=['pyHRV', 'pyHRV.indexes', 'pyHRV.windowing', 'pyHRV.galaxy']
)
