from setuptools import setup, find_packages

setup(
    name='anidbcli',
    version='1',
    keywords='Anidb UDP API CLI client ed2k rename mylist',
    description='Simple CLI for managing your anime collection using AniDB UDP API.',
    long_description="",
    author='Štěpán Adámek',
    author_email='suchama4@fit.cvut.cz',
    license='MIT',
    url='https://github.com/adameste/anidbcli',
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'anidbcli = anidbcli:main',
        ]
    },
    install_requires=[
        'click',
        'pycryptodome',
        'colorama',
        'pyperclip',
        'joblib'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)