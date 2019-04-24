from setuptools import setup

setup_deps = [
    'pytest-runner',
]

test_deps = [
    'pytest',
    'pytest-cov',
    'coveralls',
]

extras = {
    'test': test_deps,
}

setup(
    name='parameters-validation',
    version='1.0.0',
    packages=['parameters_validation'],
    url='https://github.com/allrod5/parameters-validation',
    license='MIT',
    author='Rodrigo Martins de Oliveira',
    author_email='allrod5@hotmail.com',
    description='Easy & clean function parameters validation',
    keywords=('validation parameter parameters param params'
              ' validate check argument arguments arg args'
              ' type hint'),
    setup_requires=setup_deps,
    tests_require=test_deps,
    extras_require=extras,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
