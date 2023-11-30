from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='espmega',
    version='1.5',
    license='Apache 2.0',
    author="Siwat Sirichai",
    author_email='siwat@siwatinc.com',
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/SiwatINC/pyespmega',
    keywords='mqtt esp32',
    install_requires=[
          'paho-mqtt',
          'wheel'
      ],

)