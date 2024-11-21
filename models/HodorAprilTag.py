from common.Vector2 import Vector2


class HodorAprilTag:
    def __init__(self, center: Vector2, tag_id: int, relative_distance, yaw, pitch, roll):
        self.center = center
        self.tag_id = tag_id
        self.relative_distance = relative_distance
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
