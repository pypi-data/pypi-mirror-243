from setuptools import setup, find_packages

__version__ = "0.0.2"
__build__ = '0'

with open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()

setup(
  name="tbw",
  version=__version__,
  build=__build__,
  author="Ramy Mounir",
  url="https://ramymounir.com/docs/tbw",
  description=r"""A wrapper to facilitate tensorboard logging""",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: Free for non-commercial use",
  ],
  python_requires='>=3.11',
  install_requires=[
      'torch>=2.0.0',
      'tensorboard',
      'packaging',
      'moviepy',
      ]
)
