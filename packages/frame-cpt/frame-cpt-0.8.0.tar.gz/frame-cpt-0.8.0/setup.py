
from setuptools import setup
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name = 'frame-cpt',
    version = '0.8.0',
    author = 'Framework',
    author_email = 'frameworkcptec@gmail.com',
    packages = ['framecpt'],
    install_requires = ['numpy','pandas','matplotlib', 'pycurl==7.45.2', 'cfgrib', 'netCDF4',  'xarray', 'dask', 'scipy', 'xesmf'],
    description = 'Módulo para distribuição de Modelos Numéricos.',
    long_description="""Framework

Descrição
É um pacote in Python para a distribuição de dados brutos dos Modelos Numéricos de forma segmentada/particionada. Com esse pacote o usuário não necessita fazer o Download de todo o volume bruto o pacote auxilia a manipular somente a sua necessidade.

support Python >= 3.10.

Instalação
conda create -n  python=3.10

conda activate 

conda install -c conda-forge matplotlib pycurl cfgrib netCDF4 pynio xarray dask esmpy scipy mpi4py xesmf

conda install -c anaconda ipykernel

pip install -i https://test.pypi.org/simple/ 

Como Usar
import cptecmodel.CPTEC_BAM as BAM

bam = BAM.model()

date = '2023010800'

vars = ['t', 'u10m']

levels = [1000, 850]

steps = 1

f = bam.load(date=date, var=vars,level=levels, steps=steps)

    \n""",
    long_description_content_type='text/markdown',
    url = 'https://github.com/framework-CPTEC/',
    project_urls = {
        'Código fonte': 'https://github.com/framework-CPTEC/',
        'Download': 'https://github.com/framework-CPTEC/'
    },
    license = 'MIT',
    keywords = 'recuperação de dados climáticos',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    python_requires='>=3.10',
)
