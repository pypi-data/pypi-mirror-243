import os
import re
from setuptools import setup
requires = ["pycryptodome==3.16.0","websocket_client","requests","rubiran==2.1.0","Pillow==9.4.0"]
_long_description = """

## An example:
``` python
from libraryshad import robo_shad

bot = robo_shad("Auth Account")

gap = "guids"

bot.sendMessage(gap,"mamadcodrr")
```


### How to import the shad's library

``` bash
from libraryshad import robo_shad
```

### How to install the library

``` bash
pip install libraryshad==1.0.6
```

### My ID in Rubika

``` bash
@mamadcoder1
```
## And My ID Channel in Rubika

``` bash
@python_java_source 
```
"""

setup(
    name = "libraryshad",
    version = "1.0.6",
    author = "mamadcoder",
    author_email = "mamadcoder@gmail.com",
    description = ("Another example of the library making the shad's robot"),
    license = "MIT",
    keywords = ["rubika","bot","robot","library","rubikalib","rubikalib.ml","rubikalib.ir","rubika.ir","Rubika","Python","rubiran","pyrubika","shad","telebot","twine"],
    url = "https://rubika.ir/python_java_source",
    packages=['libraryshad'],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    install_requires=requires,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
)
