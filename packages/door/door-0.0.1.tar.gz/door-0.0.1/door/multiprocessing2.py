""":mod:`door.multiprocessing2` defines utilities for multiprocessing."""

from dataclasses import dataclass, field
from multiprocessing import RLock

from door.primitives import Acquirable, SLock as SyncSLock


@dataclass
class SLock(SyncSLock):
    """The class for shared locks.

    This class is designed to be used for multiprocessing.

    The implementations in this library is read-preferring and follow
    the pseudocode in Concurrent Programming: Algorithms, Principles,
    and Foundations by Michel Raynal.
    """

    _r: Acquirable = field(default_factory=RLock, init=False)
    _g: Acquirable = field(default_factory=RLock, init=False)
