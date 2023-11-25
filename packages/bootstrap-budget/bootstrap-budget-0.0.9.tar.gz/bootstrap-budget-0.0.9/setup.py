from setuptools import setup


# Use README file as long description
with open("README.md") as f:
    long_description = f.read()


setup(
    name='bootstrap-budget',
    version='0.0.9',
    author='forgineer',
    description='A simple financial application to help you pull your budget up by its bootstraps.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/forgineer/bootstrap-budget',
    license='MIT License',
    packages=['bootstrap_budget'],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'blinker==1.7.0',
        'click==8.1.7',
        'colorama==0.4.6',
        'Flask==2.3.3',
        'Flask-SQLAlchemy==3.1.1',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'MarkupSafe==2.1.3',
        'waitress==2.1.2',
        'Werkzeug==3.0.1'
    ],
    extras_require={  # pip install -e .[pypi_packaging]
        'deployment': [
            'build',
            'twine'
        ]
    },
    entry_points={
        'console_scripts': [
            'bootstrap = bootstrap_budget.cli:bootstrap',
            'bootstrap-test = bootstrap_budget.cli:bootstrap_test'
        ]
    },
    keywords='personal budget,budgeting,web app',
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Flask',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial'
    ]
)

"""
Build and deploy steps:
    - python -m build
    - twine check dist/*
    - twine upload -r testpypi dist/*
    - twine upload dist/*
"""
