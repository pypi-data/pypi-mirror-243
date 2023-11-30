import bs4
from pathlib import Path
from PIL import Image
import os
import re
from collections.abc import Sequence
from typing import cast, Literal

# def hello(string: str) -> str:
#     """Returns a string with a greeting."""
#     return f"Hello, {string}!"

def XMLtoCSV(inPath: str, outPath: str | None, outputType: Literal['file', 'text'] = 'file') -> None | str:  
    """Converts an XML-encoded TMX file to CSV formatting."""
    soup = bs4.BeautifulSoup(open(inPath), "xml")
    
    for layer in soup.find_all('layer'):
        layer = cast(bs4.Tag, layer)
        props = cast(bs4.Tag, layer.find('properties'))
        
        if props != None:
            if props.attrs == None:
                props.clear()
            elif len(props.attrs) == 1:
                props.clear()

        width = int(layer.attrs['width'])
        
        data = cast(bs4.Tag, layer.find('data'))

        tiles = layer.findAll('tile')
        csv_oneline = ''
        for tile in tiles:
            tile = str(tile)
            sub = re.sub(r'<tile gid="(\d+)" ?/>', r'\1,', tile)
            csv_oneline += sub

        csv_oneline_split = csv_oneline.split(',')
        for i, _el in enumerate(csv_oneline_split):
            if i % width == 0 and not i >= len(csv_oneline_split) - 1 and i > 2:
                csv_oneline_split[i + 1] = '\n' + csv_oneline_split[i + 1]

        csv = ','.join(csv_oneline_split)

        data.string = csv
        data.attrs['encoding'] = 'csv'

    if outputType == 'file':
        if outPath:
            open(outPath, 'w').write(str(soup))
            return None
        else:
            raise ValueError('outPath must be non-null with file outputType.')
    else:
        return str(soup)
            


def convertMapNameToFile(name: str) -> str:
    match name:
        case "IslandSouth":
            return "Island_S"
        case "IslandWest":
            return "Island_W"
        case "IslandNorth":
            return "Island_N"
        case "IslandEast":
            return "Island_E"
        case "IslandFarmCave":
            return "Island_FarmCave"
        case "CaptainRoom":
            return "Island_CaptainRoom"
        case "IslandSouthEast":
            return "Island_SE"
        case "IslandFieldOffice":
            return "Island_FieldOffice"
        case "IslandHut":
            return "Island_Hut"
        case "IslandShrine":
            return "Island_Shrine"
        case _:
            return name

class TMXpy:
    spriteSheetFolderPaths: Sequence[Path|str] = []
    inputFile: bs4.BeautifulSoup
    tileDimensions: tuple[int, int] = (0, 0)
    tmxDimensions: tuple[int, int] = (0, 0)
    trueGIDDict: dict = {}
    tiles: dict = {}
    maxGID: int = 0
    warps: list[dict[str, int | str]] = []
    path: str | Path = ''

    properties: dict[str, str] = {}

    def __init__(self, sheets: Sequence[Path|str], path: str | Path = '', xml: str = ''):
        """Initializes the TMXpy class"""
        
        if path != '':
            self.path = path
            self.inputFile = bs4.BeautifulSoup(open(path), "xml")
        elif xml != '':
            self.inputFile = bs4.BeautifulSoup(xml, "xml")
        else:
            raise Exception("TMXpy: No path or xml given")
        
        map = self.inputFile.find("map")
        if map is None:
            raise Exception("TMXpy: No map element found")
        
        map = cast(dict, map)

        self.tmxDimensions = (int(map['width']), int(map['height']))

        self.spriteSheetFolderPaths = sheets

    
    def generateGIDDict(self) -> None:
        """Generates a dictionary of GIDs to tile information"""
        tilesets = self.inputFile.find_all("tileset")


        for tileset in tilesets:
            self.tileDimensions = (int(tileset["tilewidth"]), int(tileset["tileheight"]))
            src = tileset.find("image")["source"]

            for i in range(int(tileset["firstgid"]), int(tileset["tilecount"]) + int(tileset["firstgid"])):
                self.tiles[str(i)] = {
                    "src": src,
                    "x": int((i - int(tileset["firstgid"])) % int(tileset["columns"])),
                    "y": int((i - int(tileset["firstgid"])) / int(tileset["columns"])),
                    "width": int(tileset["tilewidth"]),
                    "height": int(tileset["tileheight"])
                }
                self.trueGIDDict[f'{src}@{i}'] = {
                    "tile": self.tiles[str(i)],
                    "gid": i,
                }

        self.maxGID = len(self.tiles)

    def generateMapPropertiesDict(self) -> None:
        """Generates a dictionary map properties"""
        properties = self.inputFile.find('properties') # There are multiple <properties />, but the first will always be map properties.
        for property in properties.find_all('property'): # type: ignore
            property = cast(bs4.Tag, property)

            self.properties[property.attrs['name']] = property.attrs['value']


    def findPathOfTileSheet(self, sheet: str, ext: str = '') -> str:
        """Finds the folder containing the given sheet"""
        for path in self.spriteSheetFolderPaths:
            fullpath = self.addExtIfNeeded(os.path.join(path, sheet), ext)
            if os.path.exists(fullpath):
                return str(fullpath)
        else:
            raise Exception(f"TMXpy: Could not find tileset {sheet} in any of the given paths {self.spriteSheetFolderPaths}")
        
    def addExtIfNeeded(self, path: str, ext: str) -> str:
        """Adds an extension to a path if it doesn't have it"""
        if not path.endswith(ext):
            path += ext
        return path
        

    def renderTile(self, gid: str) -> Image.Image:
        """Renders a tile from the TMX file"""
        try:
            tile = self.tiles[gid]
        except KeyError:
            if str(gid) == "0":
                return Image.new("RGBA", self.tileDimensions)
            
            raise Exception(f"TMXpy: Tile {gid} not found in tileset")
        
        path = self.findPathOfTileSheet(tile["src"], ".png")
        tilesheet = Image.open(path)
        
        tile = tilesheet.crop((tile["x"] * tile["width"], tile["y"] * tile["height"], tile["x"] * tile["width"] + tile["width"], tile["y"] * tile["height"] + tile["height"]))
        return tile

    def renderLayer(self, layerID: int) -> Image.Image:
        """Renders a layer in the TMX file"""
        
        layers = self.inputFile.find_all("layer")
        layer = layers[layerID]
        tiles = layer.text.split(",")

        img = Image.new("RGBA", 
            (int(layer['width']) * int(self.tileDimensions[0]),
                int(layer['height']) * int(self.tileDimensions[1])))

        for i, tile in enumerate(tiles):
            tile = tile.strip()
            if tile == "0":
                continue
            if '\n' in tile:
                tile = tile.split('\n')[0].strip()
            
            render = self.renderTile(tile)
            alpha = render.getchannel('A')
            
            img.paste(
                self.renderTile(tile), 
                (
                    int(i % int(layer['width'])) * int(self.tileDimensions[0]),
                    int(i / int(layer['width'])) * int(self.tileDimensions[1])
                ),
                alpha
            )

        return img
    
    def renderAllLayers(self, blocked: list[str] = []) -> Image.Image:
        """Renders all layers in the TMX file, except for the ones in the blocked list"""
        width = int(self.tmxDimensions[0]) * int(self.tileDimensions[0])
        height = int(self.tmxDimensions[1]) * int(self.tileDimensions[1])
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))



        
        for i, layer in enumerate(self.inputFile.find_all("layer")):
            if layer['name'] in blocked or str(i) in blocked or i in blocked:
                # print(f'Skipping layer {layer["name"]} - {i}')
                continue
            # print(f'Rendering layer {layer["name"]} - {i}')
            layer = self.renderLayer(i)
            #stick it on top of the last layer, and not overwriting the transparent pixels
            img.paste(layer, (0, 0), layer.getchannel('A'))
            # print(f'Layer {i} rendered, layer width: {layer.width}, layer height: {layer.height} - img width: {width}, img height: {height}')
        return img
    
    def parseWarps(self) -> list[dict]:
        #extract property[name="Warp"]
        prop = cast(dict, self.inputFile.find("property", {"name": "Warp"}))
        if prop is None or prop == {}:
            return []
        
        value = prop["value"].split(" ")

        warps_list = [value[i:i + 5] for i in range(0, len(value), 5)]

        warps = []
        for warp in warps_list:
            warps.append({
                "map_x": int(warp[0]),
                "map_y": int(warp[1]),
                "destination": warp[2],
                "dest_x": int(warp[3]),
                "dest_y": int(warp[4]),
            })

        self.warps = warps

        return warps
    
    def replace_warp(self, index: int, warp: dict):
        if 'warps' not in self.__dict__:
            self.parseWarps()
        self.warps[index] = warp

    def setTile(self, x: int, y: int, tile: str, layerID: int = -1, layerName: str = "") -> None:
        """Sets a tile in the TMX file"""
        if layerID > -1:
            layer = self.inputFile.find("layer", {"id": str(layerID)})
        elif layerName != "":
            layer = self.inputFile.find("layer", {"name": layerName})
        else:
            raise Exception("TMXpy: No layerID or layerName given")
        if layer is None:
            raise Exception("TMXpy: Layer not found")
        
        rows = [x for x in layer.text.split("\n") if str(x) not in ["", " ", [], [""], [" "]]]
        columns = rows[y].split(",")
        
        columns[x] = tile
        rows[y] = ",".join(columns)
        output = "\n".join(rows)
        
        layer.contents[0].replace_with(output) # type: ignore <-- like wtf pylint why what is this

    def addTilesheet(self, filename: str, setname: str, tileproperties: dict[str, list]) -> None:
        #loop through the sheet dirs, check if filename exists in any of them
        imgpath = self.findPathOfTileSheet(filename, ".png")
        img = Image.open(imgpath)
        
        width_tiles = img.width // 16
        height_tiles = img.height // 16

        elm = self.inputFile.new_tag("tileset", 
            attrs={
                "name": setname,
                "tilewidth": "16",
                "tileheight": "16",
                "tilecount": str(width_tiles * height_tiles),
                "columns": str(width_tiles),
                "firstgid": str(self.maxGID + 1)
            })
        
        imgelm = self.inputFile.new_tag("image",
            attrs={
                "source": filename,
                "width": str(img.width),
                "height": str(img.height)
            }
        )

        elm.append(imgelm)
        
        for tile in tileproperties: #iter through dict
            tileelm = self.inputFile.new_tag("tile", id=tile)
            propselm = self.inputFile.new_tag("properties")

            for prop in tileproperties[tile]: #iter through list in dict (key for list is tile id)
                propelm = self.inputFile.new_tag("property",
                    attrs={
                        "name": prop['name'],
                        "value": tileproperties[tile][prop]['value'],
                        "type": tileproperties[tile][prop]['type']
                    }
                )
                propselm.append(propelm)

            tileelm.append(propselm)
            elm.append(tileelm)

        map = self.inputFile.map
        if map is None:
            raise Exception("TMXpy: No map element found")
        
        map.append(elm)


    def save(self, path: str or Path):

        if 'warps' in self.__dict__:
            self.inputFile.find("property", {"name": "Warp"})['value'] = " ".join([f"{w['map_x']} {w['map_y']} {w['destination']} {w['dest_x']} {w['dest_y']}" for w in self.warps]) # type: ignore

        if {} != self.properties:
            og_properties = cast(bs4.Tag, self.inputFile.find('properties'))

            new_properties = self.inputFile.new_tag('properties')
            for key, value in self.properties.items():
                # Create a <property> tag for each key-value pair in the dictionary
                property_tag = self.inputFile.new_tag("property", attrs={
                    "name": key,
                    "type": 'string',
                    "value": value
                })
                new_properties.append(property_tag)

            # Replace the original element with the new one
            og_properties.replace_with(new_properties)


        with open(path, "w") as f:
            f.write(self.inputFile.prettify())


