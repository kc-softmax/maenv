import math
from uuid import UUID


class IDManager:
    def __init__(self):
        self.uuid_to_short_id: dict[UUID: int] = {}
        self.short_id_to_uuid: dict[int: UUID] = {}
        self.next_short_id = 1  # Start with 1 for simplicity

    def assign_short_id(self, uuid: UUID):
        first_short_id = self.next_short_id
        short_id = first_short_id
        while short_id in self.short_id_to_uuid:
            short_id += 1
            if short_id == first_short_id:
                # assign failed
                return -1
        self.uuid_to_short_id[uuid] = short_id
        self.short_id_to_uuid[short_id] = uuid
        self.next_short_id = short_id + 1
        return short_id

    def release_id(self, uuid: UUID, short_id: int):
        del self.short_id_to_uuid[short_id]
        del self.uuid_to_short_id[uuid]

    def get_uuid(self, short_id: int):
        return self.short_id_to_uuid.get(short_id)

    def get_short_id(self, uuid: UUID):
        return self.uuid_to_short_id.get(uuid)

    def clear(self):
        self.uuid_to_short_id.clear()
        self.short_id_to_uuid.clear()
