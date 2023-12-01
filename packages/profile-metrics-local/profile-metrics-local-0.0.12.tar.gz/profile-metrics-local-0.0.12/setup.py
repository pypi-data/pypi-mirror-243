import setuptools
# Each Python project should have pyproject.toml or setup.py (if both exist, we use the setup.py)
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have
#  moved away from needing to generate a setup.py file to enable editable installs - We might
#  able to delete this file in the near future

PACKAGE_NAME = "profile-metrics-local"
# Since all PACAKGE_NAMEs are with an underscore, we don't need this. Why do we need it?
package_dir = PACKAGE_NAME.replace("-", "_")

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.12',  # update only the minor version each time # https://pypi.org/project/profile-metrics-local/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles profile-metrics-local Python",
    long_description="This Package implements CRUD operation of profile-metrics",
    long_description_content_type='text/markdown',
    url="https://github.com/circles/profile-metrics-local-python-package",  # https://pypi.org/project/profile-metrics-local/
    # packages=setuptools.find_packages(),
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    # TODO: Update which packages to include with this package
    install_requires=[
        'PyMySQL>=1.0.2',
        'pytest>=7.4.0',
        'mysql-connector>=2.2.9',
        'logzio-python-handler>= 4.1.0',
        'user-context-remote>=0.0.17',
        'python-sdk-local>=0.0.27',
        'multipledispatch>=1.0.0'
    ],
)
