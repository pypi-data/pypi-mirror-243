from setuptools import setup, find_packages

setup(
    name='anodot-monitor',
    version="0.9",
    description='Anodot Monitoring',
    author='Alexander Shereshevsky',
    author_email='shereshevsky@gmail.com',
    packages=["anodot_monitor"],
    install_requires=[
      line.strip() for line in open("requirements.txt").readlines()
    ]
)
