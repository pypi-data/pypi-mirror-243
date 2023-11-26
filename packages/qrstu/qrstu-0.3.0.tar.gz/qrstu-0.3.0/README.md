# Q – Rainer Schwarzbach’s Text Utilities

_Test conversion and transcoding utilities_


## Installation from PyPI

```
pip install qrstu
```

Installation in a virtual environment is strongly recommended.


## Usage

### guess

The **guess** module can be used to automatically detect and repair encoding errors
(duplicate UTF-8 encoding of an already UTF-8 encoded text by misreading
the bytes as another 8-bit encoding, eg. 'Ã¤Ã¶Ã¼'),
but as the name says, it mostly works on the basis of an educated guess.


### reduce

The **reduce** module can be used to reduce Unicode text
in Latin script to ASCII encodable Unicode text,
similar to **[Unidecode](https://pypi.org/project/Unidecode/)**
but taking a different approach
(ie. mostly wrapping functionality from the standard library module
**[unicodedata](https://docs.python.org/3/library/unicodedata.html)**).
Unlike **Unidecode** which also transliterates characters from non-Latin scripts,
**reduce** stubbornly refuses to handle these.

You can, however, specify an optional `errors=` argument in the
**reduce.reduce_text()** call, which is passed to the internally used
**[codecs.encode()](https://docs.python.org/3/library/codecs.html#codecs.encode)**
function, thus taking advance of the codecs module errors handling.


### transcode

The **transcode** module provides various functions for decoding
and encoding byte sequences to/from Unicode text.


## Further reading

Please see the documentation at <https://blackstream-x.gitlab.io/qrstu>
for detailed usage information.

If you found a bug or have a feature suggestion,
please open an issue [here](https://gitlab.com/blackstream-x/qrstu/-/issues)

