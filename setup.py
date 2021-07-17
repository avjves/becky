from distutils.core import setup

setup(name='Becky',
      version='0.1',
      description='Becky backupper',
      author='Aleksi Vesanto',
      author_email='avjves@gmail.com',
      packages=['becky_cli'],
      entry_points={
        'console_scripts': [
            'becky=run:main',
        ],
      },
)
