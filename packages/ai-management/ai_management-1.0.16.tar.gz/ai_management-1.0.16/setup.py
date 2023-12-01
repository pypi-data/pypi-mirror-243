import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
print(setuptools.find_packages())

setuptools.setup(
    name='ai_management',                           # should match the package folder
    packages=['ai_management', 'examples'],
    #py_modules=['model_evaluation', 'constants', '__init__'],
    package_data={
        'examples': ['usage_examples.ipynb'], 
        # 'ai_management': ['model_evaluation', 'constants', '__init__'],
    },
    install_requires=[
        'pandas==1.3.5', 
        'numpy==1.21.6', 
        'scikit-learn==1.0.2', 
        'google-cloud-bigquery==3.10.0', 
        'google-colab==1.0.0', 
        ],                  # list all packages that your package uses
    #packages=['C:\\Users\\51028915\\Documents\\GitHub\\ai_management'], # should match the package folder
    version='1.0.16',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='This is a toolbox to help AI & ML teams to have a better management of their metrics.',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Leroy Merlin Brazil',
    author_email='chapter_inteligencia_artificia@leroymerlin.com.br',
    url='https://github.com/adeo/aim', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/adeo/aim/issues"
    },
    
    keywords=["management", "toolbox", "lmbr", "ai"], #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)