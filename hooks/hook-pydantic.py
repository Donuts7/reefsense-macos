<<<<<<< HEAD

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('pydantic')
hiddenimports += [
    'pydantic.json',
    'pydantic.dataclasses',
    'pydantic.datetime_parse',
    'pydantic.types',
    'pydantic.fields'
]
=======

from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('pydantic')
hiddenimports += [
    'pydantic.json',
    'pydantic.dataclasses',
    'pydantic.datetime_parse',
    'pydantic.types',
    'pydantic.fields'
]
>>>>>>> 0ec55ee4c559eccff77b783a2b56c20f2512182b
