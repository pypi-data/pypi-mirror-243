from distutils.core import setup
from setuptools import find_packages


version = '0.2.6rc4'

CLASSIFIERS = [
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
]

install_requires = [
    'Django>=1.11',
    # 'django-appconf',
]


def read(f):
    return open(f, 'r').read()


setup(
    name="django-cookie-consent-pax",
    description="Django cookie consent application",
    version=version,
    author="Informatika Mihelac",
    author_email="bmihelac@mihelac.org",
    url="https://gitlab.com/paxsolutions/django-cookie-consent",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
)
