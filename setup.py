import os
import sys

from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


meta = {}
exec(read('sanic_scheduler/__meta__.py'), meta)

if sys.argv[-1] == 'publish':
    os.system("rm dist/*.gz dist/*.whl")
    os.system("git tag -a %s -m 'v%s'" % (meta['__version__'], meta['__version__']))
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    os.system("git push --tags")
    sys.exit()


setup(
    name=meta['__title__'],
    version=meta['__version__'],
    url=meta['__url__'],
    license=meta['__license__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    description=meta['__summary__'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    platforms='all',
    packages=['sanic_scheduler'],
    # install_requires=['sanic'],
    # tests_require=['pytest'],
    # test_suite="tests.get_tests",
    keywords='sanic schedule',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
