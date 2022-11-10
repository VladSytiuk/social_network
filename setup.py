from setuptools import setup
from datetime import date

setup(
    name='samplepackage',
    version=date.today().strftime('%y.%m.%d'),
    packages=['posts'],
    include_package_data=True,
    zip_safe=False
)
