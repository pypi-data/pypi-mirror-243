from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name="hitips",
    version="0.1.8",
    author="keikhosravi",
    author_email="adib.keikhosravi@nih.gov",
    description="HiTIPS: High-Throughput Image Processing Software for FISH data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CBIIT/HiTIPS",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python-headless',
        'scikit-image',
        'scipy',
        'Pillow',
        'pandas',
        'matplotlib',
        'btrack',  
        'imageio',
        'tifffile',
        'aicsimageio',
        'deepcell',  
        'scikit-learn',
        'hmmlearn',
        'PyQt5',
        'cellpose',
        'tensorflow',
        'joblib',
        'dask',
        'nd2reader',
        'imaris_ims_file_reader',
        'qimage2ndarray',
        'spatial_efd',
        'pydantic==1.10.9',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Processing',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'hitips=hitips.HiTIPS:main',
        ],
    },
    license="MIT",
    keywords="high-throughput imaging FISH analysis cell segmentation signal quantification",
)

