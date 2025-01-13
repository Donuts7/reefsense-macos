
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = collect_all('pydantic')
hiddenimports += [
    'pydantic.json',
    'pydantic.dataclasses',
    'pydantic.datetime_parse',
    'pydantic.types',
    'pydantic.fields'
]
