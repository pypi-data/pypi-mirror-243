import contextlib  # NOQA: D104
import os
import tempfile
from pathlib import Path

import cffi
import simpledbf


class BlastError(Exception):
    '''
    Exception raised for errors raised by blast lib.

    Attributes
    ----------
    code: int
    message: str
    '''

    def __init__(self: 'BlastError', code: int, message: str) -> 'BlastError':
        self.code = code
        self.message = message
        super().__init__(f'{code=}    {message=}')


def dbc2dbf(src: [str, Path], dest: [str, Path] = None, /) -> None:
    '''
    Convert a source .dbc file to a .dbf destination file.

    Attributes
    ----------
    src: str, Path
        the file to read the .dbc from.
    dest: str, Path [optional]
        the file to write the .dbf to.
        if missing, then it will infer the same dir and filename as src

    Raises
    ------
    BlastError
        if the input file can't be processed by blast-dbf decompression tool
    '''

    try:
        import readdbc.blast.blastpy as blastpy  # NOQA: PLR0402
    except ModuleNotFoundError:
        _build_blast()
        import readdbc.blast.blastpy as blastpy  # NOQA: PLR0402

    src = Path(src)
    _check_file(name=src, extension='dbc')

    if dest is None:
        dest = str(src).replace('.dbc', '.dbf')
    dest = Path(dest)

    with open(src, 'rb') as src_fp, open(dest, 'wb') as dest_fp:
        ret_code = blastpy.lib.dbc2dbf(src_fp, dest_fp)
    if ret_code != 0:
        dest.unlink()
        raise BlastError(code=ret_code, message='')


def _check_file(*, name: Path, extension: str) -> None:
    expected_end = '.' + extension.lower()
    if not str(name).lower().endswith(expected_end):
        msg = f'file "{name}" is expected to have {extension=}'
        raise ValueError(msg)


def dbc2csv(src: [str, Path], dest: [str, Path] = None, /) -> None:
    '''
    Convert a source .dbc file to a .csv destination file.

    Attributes
    ----------
    src: str, Path
        the file to read the .dbf from.
    dest: str, Path [optional]
        the file to write the .csv to.
        if missing, then it will infer the same dir and filename as src
    '''
    src = Path(src)
    _check_file(name=src, extension='dbc')

    if dest is None:
        dest = str(src).replace('.dbc', '.csv')
    dest = Path(dest)

    file = tempfile.NamedTemporaryFile()
    try:
        dbc2dbf(src, file.name)
        simpledbf.Dbf5(file.name).to_csv(dest)
    finally:
        with contextlib.suppress(FileNotFoundError):
            file.close()


def _build_blast() -> None:
    ffibuilder = cffi.FFI()

    ffibuilder.cdef(csource='int dbc2dbf(FILE* input, FILE* output);')

    build_folder = Path(os.path.realpath(__file__)).parent / 'blast'
    code_file = build_folder / 'blast-dbf.c'
    with open(code_file) as f:
        code = f.read()
    ffibuilder.set_source(
        module_name='blastpy', source=code, sources=['blast.c'],
    )

    ffibuilder.compile(tmpdir=build_folder)
