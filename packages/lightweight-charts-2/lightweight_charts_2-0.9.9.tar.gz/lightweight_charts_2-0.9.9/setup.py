from setuptools import setup, find_packages

setup(
    name='lightweight_charts_2', 
    version='0.9.9',  
    author='Jimmy Fallon',
    author_email='ashzarz.56@gmail.com',
    description='Lightweight charts but you can have optional parameters of naming each popup window',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/lightweight_charts_2',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pandas',
        'pywebview>=4.3',
    ],
    package_data={
        'lightweight_charts': ['js/*.js'],
    },
)

