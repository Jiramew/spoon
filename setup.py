from setuptools import setup, find_packages

setup(
    name='spoonproxy',
    version='git.latest',
    description='A package for building specific Proxy Pool for different Sites.',
    packages=find_packages(),
    url='https://github.com/Jiramew/spoon',
    license='BSD License',
    author='Jiramew',
    author_email='hanbingflying@sina.com',
    maintainer='Jiramew',
    maintainer_email='hanbingflying@sina.com',
    platforms=["all"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'requests>=2.18.1',
        'lxml>=3.8.0',
        'redis>=2.10.5',
        'schedule>=0.4.3',
        'PyExecJS>=1.4.0',
    ]
)
