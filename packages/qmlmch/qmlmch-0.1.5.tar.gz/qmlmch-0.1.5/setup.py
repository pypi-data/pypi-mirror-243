from setuptools import setup, find_packages
with open('README.md',"r") as fh:
    description = fh.read() 

setup(
    name='qmlmch',
    version='0.1.5',
    #packages=find_packages(exclude=['testsumm']),
    packages=find_packages(),
    description='library ML',
    long_description=description,
    long_description_content_type="text/markdown",
    author='Luciano M', 
    license='MIT',
    install_requires=["numpy","plotly","scipy","matplotlib"],
    python_requires='>=3.10.12',
    author_email='luciano.munoz1@udea.edu.co',
    #url = 'https://gitlab.com/LucianoMCH/hydrogen_atom'
)

#como crear el archivo requirements.txt
#pip freeze > requirements.txt
    
    
