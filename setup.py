from distutils.core import setup
import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='Becky',
      version='0.7',
      description='Becky backupper',
      author='Aleksi Vesanto',
      author_email='avjves@gmail.com',
      packages=['becky_cli'],
      # include_package_data=True,
      entry_points={
        'console_scripts': [
            'becky=becky_cli.run:main',
        ],
      },
      license='MIT',
      long_description=README,
      long_description_content_type='text/markdown',
)
