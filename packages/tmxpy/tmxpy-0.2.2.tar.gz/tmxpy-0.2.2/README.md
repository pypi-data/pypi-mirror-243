# TMXpy

A Python library for reading and writing TMX files.

This library is fairly computer intensive, especially when rendering large maps. It is recommended to use a computer with decent specs when using this library.

**Please note**: This library only supports files saved with the CSV encoding, though XML-encoded files can be converted with `tmxpy.XMLtoCSV`

## Features

- Rendering of TMX files to images
- Replacing specific warps with other warps
- Changing tiles of a TMX file
- Adding tilesets to a TMX file

## Installation

```bash
pip install tmxpy
```

## Usage and Examples

```python
from tmxpy import TMXpy
from pathlib import Path

tmx = TMXpy(sheets=[Path("path/to/tilesheet/directory")], path=Path("path/to/tmx/file"))
tmx.generateGIDDict()
tmx.renderAllLayers().save("path/to/output/image.png")

tmx.parseWarps()
tmx.replace_warp(0, {
    "map_x": 23,
    "map_y": 17,
    "destination": "Town",
    "dest_x": 10,
    "dest_y": 8,
})

tmx.setTile(23, 17, "129", layerName="Buildings")

```

Further examples can be found in the [tests](https://github.com/AnotherPillow/tmxpy/tree/main/tests) directory.

## Development/Testing

- Install dependencies with `pip install -r requirements.txt`
- Tests can be added to tests/name_of_test.py and run with `py -m tests.name_of_test`
- It can be built with `py -m build`
