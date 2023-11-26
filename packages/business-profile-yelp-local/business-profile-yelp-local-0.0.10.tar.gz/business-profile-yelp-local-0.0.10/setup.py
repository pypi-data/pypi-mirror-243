import setuptools

PACKAGE_NAME = "business-profile-yelp-local"
package_dir = "LocalYelpPython"

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/business-profile-yelp-local
    version='0.0.10',
    author="Circles",
    author_email="info@circles.life",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    long_description="This package is used to import business profiles from Yelp.com.",
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "gql>=3.4.0",
        "requests>=2.29.0",
        "requests-toolbelt>=0.10.1",
        # "database-mysql-local>=0.0.116",
        "logger-local>=0.0.71"]
)
