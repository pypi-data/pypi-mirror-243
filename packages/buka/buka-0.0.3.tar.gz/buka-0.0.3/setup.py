from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='buka',
    version='0.0.3',
    description='Aboubakar',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Boo4kin',
    author_email='bkolyabu@gmail.com',
    classifiers=classifiers,
    license='MIT',
    keywords='test',
    packages=find_packages(),
    install_requiers=['']

)
