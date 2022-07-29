import pathlib
from pytz import VERSION
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.2b' #
PACKAGE_NAME = 'ProbabilityLib' #Ojo es el nombre de la libreria y de la carpeta
AUTHOR = 'L Felipe Guerrero'
AUTHOR_EMAIL = 'felipe.guerrero@correounivalle.edu.co' 
URL = '' 

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para leer ficheros PDFs y extraer la información en formato str' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"


#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
      'pandas',
      'matplotlib',
      'pymc3',
      'numpy',
      'seaborn',
      'scipy',
      ]
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)