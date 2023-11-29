#  Copyright 2020 Reid Swanson.
#
#  This file is part of scrachy.
#
#  scrachy is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  scrachy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with scrachy.  If not, see <https://www.gnu.org/licenses/>.

# Python Modules
import pathlib

from setuptools import find_packages, setup

# 3rd Party Modules

# Project Modules


current_dir = pathlib.Path(__file__).parent
readme = (current_dir / "README.md").read_text()

extras = {
    'content_extraction': ['beautifulsoup4', 'boilerpy3'],
    'html_parsing': ['html5lib', 'lxml'],
    'mysql': ['pymysql'],
    'postgresql': ['psycopg2'],
    'testing': ['pytest', 'pytest-twisted', 'python-dotenv', 'pyyaml']
}
all_extras = [package_name for extra_list in extras.values() for package_name in extra_list]


if __name__ == '__main__':
    setup(
        name='scrachy',
        version='0.5.1',
        description='Enhanced caching modules for scrapy.',
        long_description=readme,
        long_description_content_type='text/markdown',
        install_requires=[
            'cron-converter',
            'msgspec',
            'scrapy',
            'selenium',
            'sqlalchemy',
            'twisted',
            'w3lib',
            'pywin32; os_name=="nt"'
        ],
        extras_require={'all': all_extras} | extras,
        author='Reid Swanson',
        maintainer='Reid Swanson',
        author_email='reid@reidswanson.com',
        maintainer_email='reid@reidswanson.com',
        zip_safe=False,
        packages=find_packages(),
        include_package_data=True,
        license='lgpl-v3',
        url='https://bitbucket.org/reidswanson/scrachy',
        classifiers=['Development Status :: 4 - Beta',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
                     'Natural Language :: English',
                     'Operating System :: MacOS',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: POSIX',
                     'Operating System :: Unix',
                     'Programming Language :: Python :: 3.11'])
