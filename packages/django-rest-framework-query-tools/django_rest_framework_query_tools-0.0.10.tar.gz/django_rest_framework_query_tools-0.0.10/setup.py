from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='django_rest_framework_query_tools',
    version='0.0.10',
    description='A Django app that provides tools for querying',
    author='Joe Philip',
    package_dir={'': 'libname'},
    package_data={'libname': ['django_rest_framework_query_tools.py']},
    packages=find_packages(where='libname'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/joe-philip/django-query-tools.git',
    license='MIT License',
    author_email='joe.philip@hotmail.co.in',
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
    install_requires=["djangorestframework>=3.14.0"]
)
