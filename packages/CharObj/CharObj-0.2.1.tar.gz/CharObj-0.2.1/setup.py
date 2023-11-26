from setuptools import setup, find_packages

long_description=open('README.md').read()

setup(
    name='CharObj',
    version='0.2.1',
    description='A package for creating objects for a text-based RPG',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/CharObj',
    packages=find_packages(),
    install_requires=[
        'pyglet',
        'dicepy',
        'gridengine_framework'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='game development',
    license='MIT',
    python_requires='>=3.7',
    include_package_data=True,
    package_data={'CharObj': ['_dicts/*.json']}    
)