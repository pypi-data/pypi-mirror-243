from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='statman',
      version='1.3.2',
      author='Mighty Pulpo',
      author_email='jayray.net@gmail.com',
      description='Collection of metrics collection tools, including a simple stopwatch',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      python_requires='>=3.6',
      keywords='stats, metrics, stopwatch, timing, performance, monitoring')