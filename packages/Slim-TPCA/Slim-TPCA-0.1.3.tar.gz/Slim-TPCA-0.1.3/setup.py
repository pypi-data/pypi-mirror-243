from setuptools import setup, find_packages

setup(
    name='Slim_TPCA',
    version='0.1.1',
    description='Slim-TPCA package is a python package which requires python version higher than 3.7 to work. Slim-TPCA has been optimised based on the TPCA method published in 2018. By using fewer temperature points, Slim-TPCA can reduce the volume of samples required, eliminate the batch effect in multiplex mass spectrometry experiments, and greatly shorten the calculation time required. In the Slim-TPCA package, users can perform data pre-processing, graph ROC plots to determine the ability of the data to predict protein interactions, calculate the TPCA signatures of the complexes and dynamic modulations of the complexes',
    url='https://github.com/wangjun258/Slim_TPCA',
    author='Siyuan Sun, Jun Wang',
    author_email='11930100@mail.sustech.edu.cn',
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        'numpy>=1.22.4',
        'pandas>=1.4.3',
        'matplotlib>=3.4.3',
        'scipy>=1.7.1',
        'scikit-learn>=1.2.2',
        'seaborn>=0.11.2'
    ],
)
