from typing import TypedDict

class Process(TypedDict):
    name: str
    pid: int
    debug: bool
    handle: int

class Vector3(TypedDict):
    x: float
    y: float
    z: float

class Vector2(TypedDict):
    x: float
    y: float