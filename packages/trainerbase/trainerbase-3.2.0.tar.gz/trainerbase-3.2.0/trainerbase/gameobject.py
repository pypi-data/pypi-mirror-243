from abc import ABC, abstractmethod
from typing import Self, override

from pymem.exception import MemoryWriteError

from trainerbase.memory import ConvertibleToAddress, ensure_address, pm


class AbstractReadableObject[T](ABC):
    @property
    @abstractmethod
    def value(self) -> T:
        pass


class GameObject[PymemType, TrainerBaseType](AbstractReadableObject[TrainerBaseType]):
    created_objects: list[Self] = []

    @staticmethod
    @abstractmethod
    def pm_read(address: int) -> PymemType:
        pass

    @staticmethod
    @abstractmethod
    def pm_write(address: int, value: PymemType) -> None:
        pass

    def __init__(
        self,
        address: ConvertibleToAddress,
        frozen: TrainerBaseType | None = None,
    ):
        GameObject.created_objects.append(self)

        self.address = ensure_address(address)
        self.frozen = frozen

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}"
            f" at {hex(self.address.resolve())}:"
            f" value={self.value},"
            f" frozen={self.frozen}"
            ">"
        )

    def after_read(self, value: PymemType) -> TrainerBaseType:
        return value  # type: ignore

    def before_write(self, value: TrainerBaseType) -> PymemType:
        return value  # type: ignore

    @property
    @override
    def value(self) -> TrainerBaseType:
        return self.after_read(self.pm_read(self.address.resolve()))

    @value.setter
    def value(self, new_value: TrainerBaseType):
        self.pm_write(self.address.resolve(), self.before_write(new_value))


class GameFloat(GameObject[float, float]):
    pm_read = pm.read_float  # type: ignore
    pm_write = pm.write_float

    @override
    def before_write(self, value):
        return float(value)


class GameDouble(GameObject[float, float]):
    pm_read = pm.read_double  # type: ignore
    pm_write = pm.write_double

    @override
    def before_write(self, value):
        return float(value)


class GameByte(GameObject[bytes, int]):
    @staticmethod
    @override
    def pm_read(address: int) -> bytes:
        return pm.read_bytes(address, length=1)

    @staticmethod
    @override
    def pm_write(address: int, value: bytes) -> None:
        pm.write_bytes(address, value, length=1)

    @override
    def before_write(self, value: int) -> bytes:
        return value.to_bytes(length=1, byteorder="little")

    @override
    def after_read(self, value: bytes) -> int:
        return int.from_bytes(value, byteorder="little")


class GameInt(GameObject[int, int]):
    pm_read = pm.read_int  # type: ignore
    pm_write = pm.write_int


class GameShort(GameObject[int, int]):
    pm_read = pm.read_short  # type: ignore
    pm_write = pm.write_short


class GameLongLong(GameObject[int, int]):
    pm_read = pm.read_longlong  # type: ignore
    pm_write = pm.write_longlong


class GameUnsignedInt(GameObject[int, int]):
    pm_read = pm.read_uint  # type: ignore
    pm_write = pm.write_uint


class GameUnsignedShort(GameObject[int, int]):
    pm_read = pm.read_ushort  # type: ignore
    pm_write = pm.write_ushort


class GameUnsignedLongLong(GameObject[int, int]):
    pm_read = pm.read_ulonglong  # type: ignore
    pm_write = pm.write_ulonglong


class GameBool(GameObject[bool, bool]):
    pm_read = pm.read_bool  # type: ignore
    pm_write = pm.write_bool


class ReadonlyGameObjectSumGetter(AbstractReadableObject[int | float]):
    def __init__(self, *game_numbers: GameInt | GameFloat):
        self.game_numbers = game_numbers

    @property
    def value(self) -> int | float:
        return sum(number.value for number in self.game_numbers)


def update_frozen_objects():
    for game_object in GameObject.created_objects:
        if game_object.frozen is not None:
            try:
                game_object.value = game_object.frozen
            except MemoryWriteError:
                continue
