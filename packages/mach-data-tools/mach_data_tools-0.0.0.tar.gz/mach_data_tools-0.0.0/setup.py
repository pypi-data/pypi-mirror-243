from setuptools import setup, find_packages


VERSION = "0.0.0"
DESCRIPTION = "MACH Data Tools"
LONG_DESCRIPTION = "A package that provides functionality for common tasks performed in MACH D&A"

# Setting up
setup(
    name="mach_data_tools",
    version=VERSION,
    author="sfgarcia",
    author_email="<sfgarcia@uc.cl>",
    description=DESCRIPTION,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=[
        "awswrangler>=3.0.0",
        "matplotlib>=3.6.0",
        "numpy>=1.24.0",
        "pandas>=1.5.0",
        "plotly>=5.11.0",
        "scikit-learn>=1.2.0",
        "scipy>=1.9.0",
        "shap>=0.41.0",
        "tqdm==4.66.1",
        "xgboost==2.0.0",
    ],
    keywords=["python", "analytics", "data"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
