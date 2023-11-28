from setuptools import find_packages, setup
from toml import load

with open('README.md', 'r') as f:
    long_description = f.read()

pyproject = load('pyproject.toml')

setup(
    name=pyproject['project'].get('name', 'django_rest_token_expiry'),
    version=pyproject['project'].get('version', '0'),
    description=pyproject['project'].get('description'),
    author=pyproject['project'].get('authors')[0].get('name'),
    package_dir={'': '.'},
    package_data={'django_rest_exception_handler': ['exception_handlers.py']},
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=pyproject['project'].get('urls').get('Homepage'),
    license='MIT License',
    author_email=pyproject['project'].get('authors')[0].get('email'),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=pyproject['build-system'].get('requires')
)
