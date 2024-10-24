from common.Vector2 import Vector2


class ScanResult:
    def __init__(self, target_position: Vector2):
        self.target_position = target_position
        self.obstacles = None
