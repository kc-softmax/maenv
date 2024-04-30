import pytmx
from pathlib import Path
from numpy.random._generator import Generator as Generator
from maenv.core.tile_map import TileMap
from maenv.core.tile import Tile, TileState

# 현재 파일의 Path 객체 생성
current_directory = Path(__file__).resolve().parent


defulat_map = pytmx.TiledMap(f'{current_directory}/default_map.tmx')


class DefaultMap(TileMap):

    def __init__(
        self,

    ) -> None:
        super().__init__(
            defulat_map.width,
            defulat_map.height,
            defulat_map.tilewidth,
        )

    def setup(self):
        # restrict, unused
        for layer in defulat_map.layers:
            if 'unused' == layer.name:
                continue

            restrict = 'restrict' == layer.name
            for col, row, _ in layer.tiles():
                address = col + row * self.cols
                if address not in self.tile_map:
                    tile = Tile(
                        row,
                        col,
                        address,
                        self.tile_size
                    )
                    self.tile_map[address] = tile
                else:
                    tile = self.tile_map[address]

                if restrict:
                    tile.state = TileState.RESTRICT

        for address, tile in self.tile_map.items():
            if tile.state == TileState.RESTRICT:
                self.restrict_addresses.append(address)
            else:
                self.respawn_addresses.append(address)
        self.initial_respawn_addresses = set(self.respawn_addresses)
