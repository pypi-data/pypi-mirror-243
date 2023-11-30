import contextlib
import os
import tempfile
import typing


@contextlib.contextmanager
def NamedTemporaryFifo() -> typing.Generator[str, None, None]:
    while True:
        try:
            filename = tempfile.mktemp()
            os.mkfifo(filename, 0o600)
            break
        except FileExistsError:
            continue

    try:
        yield filename
    finally:
        os.remove(filename)
