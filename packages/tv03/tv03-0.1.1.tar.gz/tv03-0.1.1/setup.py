from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='tv03',
  version='0.1.1',
  author='fertic',
  author_email='foxmine852@gmail.com',
  description='This is the simplest module for quick work with files. v2',
  long_description=readme(),
  long_description_content_type='text/markdown',
  # url='your_url',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  # project_urls={
  #   'GitHub': 'your_github'
  # },
  # python_requires='>=3.6'
)