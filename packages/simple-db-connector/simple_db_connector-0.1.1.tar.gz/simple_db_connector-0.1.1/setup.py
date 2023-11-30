from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.1.1' 
DESCRIPTION = 'Simple database connector for python'
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="simple_db_connector", 
        version=VERSION,
        author="Rene Schwertfeger",
        author_email="<mail@reneschwertfeger.de>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=["mysql-connector"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'database', 'connector', 'simple', 'mysql', 'mariadb', 'sqlite', 'sql', 'connector', 'db', 'database-connector'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)