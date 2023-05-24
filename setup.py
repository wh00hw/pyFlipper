
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    readme = fh.read()

setuptools.setup(
  name = 'pyflipper',      
  package_dir={'': 'src'},
  packages=setuptools.find_packages(where='src'),
  version = '0.17',
  license='MIT',
  long_description=readme,
  long_description_content_type='text/markdown',
  description = 'Unoffical Flipper Zero cli wrapper',
  author = 'wh00hw',
  author_email = 'white_rabbit@autistici.org',
  url = 'https://github.com/wh00hw/pyFlipper',
  project_urls={
    'Documentation': 'https://github.com/wh00hw/pyFlipper/blob/master/README.md',
    'Bug Reports':
    'https://github.com/wh00hw/pyFlipper/issues',
    'Source Code': 'https://github.com/wh00hw/pyFlipper',
  },
  keywords = ['flipper', 'wrapper', 'module'],
  install_requires=[
          'pyserial',
          'websocket-client',
      ],
  classifiers=[
    # see https://pypi.org/classifiers/
    'Development Status :: 4 - Beta',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
 ],
  python_requires='>=3.8',
)