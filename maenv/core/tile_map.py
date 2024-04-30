import math
import numpy as np
from warnings import warn
from maenv.core.tile import Tile, TileState


class TileMap:

    def __init__(
        self,
        cols: int,
        rows: int,
        tile_size: int,
    ) -> None:
        self.map_width = cols * tile_size
        self.map_height = rows * tile_size
        self.cols = cols
        self.rows = rows
        self.tile_size = tile_size
        self.tile_map: dict[int: Tile] = {}

        self.restrict_addresses: list[int] = []
        self.respawn_addresses: list[int] = []
        self.setup()

    def setup(self):
        initial_respawn_addresses: list[int] = []
        for col in range(self.cols):
            for row in range(self.rows):
                address = col + row * self.cols
                tile = Tile(
                    row,
                    col,
                    address,
                    self.tile_size
                )
                if tile.state != TileState.RESTRICT:
                    initial_respawn_addresses.append(address)
                    self.respawn_addresses.append(address)
                self.tile_map[address] = tile

        self.initial_respawn_addresses = set(initial_respawn_addresses)

    def get_respawn_positions(
        self,
        np_random: np.random.Generator,
        num_of_positions: int
    ) -> list[tuple[int, int]]:
        if len(self.respawn_addresses) < 1:
            return
        respawn_count = len(self.respawn_addresses) - num_of_positions
        if respawn_count < 1:
            addresses_count = len(self.respawn_addresses)
        else:
            addresses_count = num_of_positions
        addresses = np_random.choice(
            self.respawn_addresses,
            addresses_count,
            replace=False)
        return [
            self.get_tile_position(address)
            for address in addresses
        ]

    def get_tile_address(self, x: int, y: int):
        col = math.floor(x / self.tile_size)
        row = math.floor(y / self.tile_size)
        return col + row * self.cols

    def get_neighbor_addresses(self, x: int, y: int, area_range=1) -> list[int]:
        return [
            tile.address
            for tile in self.get_tiles(x, y, area_range)
        ]

    def get_tile_position(self, address: int) -> tuple[int, int]:
        if address not in self.tile_map:
            raise Exception('get_tile_position')
        return self.tile_map[address].center

    def get_tile(self, x: int, y: int) -> Tile:
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.map_width - 1:
            x = self.map_width - 1
        if y > self.map_height - 1:
            y = self.map_height - 1
        col = math.floor(x / self.tile_size)
        row = math.floor(y / self.tile_size)
        address = col + row * self.cols
        if address not in self.tile_map:
            warn(
                'address is invalid, check coords')
            return None
        return self.tile_map[address]

    def get_tiles(self, x: int, y: int, area_range: int = 1) -> list[Tile]:
        center_col = math.floor(x / self.tile_size)
        center_row = math.floor(y / self.tile_size)

        # Calculate the range of rows and columns within the specified area
        start_row = max(0, center_row - area_range)
        end_row = min(self.rows, center_row + area_range + 1)
        start_col = max(0, center_col - area_range)
        end_col = min(self.cols, center_col + area_range + 1)
        # Get the tiles within the specified area
        tiles = []
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                address = col + row * self.cols
                if address not in self.tile_map:
                    continue
                tiles.append(self.tile_map[address])
        return tiles

    def reset(self):
        for tile in self.tile_map.values:
            tile.reset()

    def update_tile_state(self, address: int, state: TileState):
        if address not in self.tile_map:
            return
        tile = self.tile_map[address]
        tile.state = state
        match state:
            case TileState.NORMAL:
                self.initial_respawn_addresses.add(address)
            case TileState.RESTRICT:
                if address in self.initial_respawn_addresses:
                    self.initial_respawn_addresses.remove(address)

    def update_respawn_addresses(self, used_addresses: list[int]):
        # 매번 갱신해줘야한다. 그렇다는 말은? 리스폰 되야 하는 것은 한번에 모아서 처리해야 한다.
        self.respawn_addresses = list(
            self.initial_respawn_addresses - set(used_addresses))
