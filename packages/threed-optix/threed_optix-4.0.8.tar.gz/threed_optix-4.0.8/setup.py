from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()


setup(
    name='threed_optix',
    version= '4.0.8',
    license='MIT',
    author="3DOptix",
    author_email='ereztep@3doptix.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://3doptix.com',
    keywords=["Optics", "Optical Design", "Optical Simulation", "Optical Design Software", "3DOptix"],
    install_requires=[
        'requests',
        'pandas',
        'matplotlib',
        'plotly==5.17.0',
        'colorama',
        'nbformat',
        'numpy',
        'scikit-image',
        'dill',
    ]
)
