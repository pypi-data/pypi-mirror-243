import setuptools
#with open("README.md", "r") as fh:
#    long_description = fh.read()
setuptools.setup(
     name='pyapimr',  
     version='1.0.1',
     scripts=['pyapimrdemo'] ,
     author="Mr Moorgh",
     author_email="vboxvm512@gmail.com",
#     long_description=long_description,
   long_description_content_type="text/markdown",
#     url="https://github.com/",
     packages=setuptools.find_packages(),
 )
