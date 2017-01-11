import codecs
import tempfile
import os


def create_tempfile(suffix="", prefix="tmp", dir=None):
    """
    Creates a temporary file with a closed stream
    The user is expected to clean up after use.

    :return: filepath of a temporary file.
    """
    temporary = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    os.close(temporary[0])
    return temporary[1]


def detect_encoding(filename, default='utf-8'):
    """
    Detects the file encoding by reading out the BOM.

    Given a file with a BOM signature:

    >>> import os, tempfile
    >>> text = 'ä'
    >>> encoded = codecs.encode(text, encoding='utf-16-le')
    >>> fhandle, filename = tempfile.mkstemp()
    >>> os.write(fhandle, codecs.BOM_UTF16_LE + encoded)
    4
    >>> os.close(fhandle)

    This will detect the encoding from the first bytes in the file:

    >>> detect_encoding(filename)
    'utf-16'

    You can now open the file easily with the right encoding:

    >>> with open(filename, encoding=detect_encoding(filename)) as f:
    ...     print(f.read())
    ä

    If you have a normal file without BOM, it returns the default (which you
    can give as an argument and is UTF 8 by default) so you can read them
    just as easy:

    >>> detect_encoding(__file__)
    'utf-8'

    This code is mainly taken from
    http://stackoverflow.com/a/24370596/3212182.

    :param filename: The file to detect the encoding of.
    :param default:  The default encoding to use if no BOM is present.
    :return:         A string representing the encoding.
    """
    with open(filename, 'rb') as f:
        raw = f.read(4)  # will read less if the file is smaller

    for enc, boms in [
        ('utf-8-sig', (codecs.BOM_UTF8,)),
        ('utf-16', (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)),
        ('utf-32', (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE))
    ]:
        if any(raw.startswith(bom) for bom in boms):
            return enc

    return default
