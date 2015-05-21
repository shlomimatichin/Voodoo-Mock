import contextlib
import os
import tempfile

@contextlib.contextmanager
def temporaryFile( contents ):
    #
    # From the python documentation:
    # Whether the name can be used to open the file a second time, while the
    # named temporary file is still open, varies across platforms (it can be
    # so used on Unix; it cannot  on Windows NT or later).
    #
    t = tempfile.NamedTemporaryFile( suffix = ".h", delete = False )
    t.write( contents )
    t.flush()
    t.close()
    yield t.name
    os.unlink(t.name)
