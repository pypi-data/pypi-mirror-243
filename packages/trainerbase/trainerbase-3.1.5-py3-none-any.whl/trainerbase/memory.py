from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import partial
from typing import Self, assert_never

from pymem import Pymem
from pymem.exception import ProcessNotFound
from pymem.pattern import pattern_scan_all, pattern_scan_module
from pymem.process import module_from_name

from trainerbase.config import pymem_config


for process_name in pymem_config["process_names"]:
    try:
        pm = Pymem(process_name, exact_match=pymem_config["exact_match"], ignore_case=pymem_config["ignore_case"])
    except ProcessNotFound:
        continue
    break
else:
    raise ProcessNotFound(f"not any: {pymem_config['process_names']}")


ARCH = 32 if pm.is_WoW64 else 64
POINTER_SIZE = 4 if pm.is_WoW64 else 8


type ConvertibleToAddress = AbstractAddress | int | bytes


read_pointer: Callable[[int], int] = pm.read_uint if pm.is_WoW64 else pm.read_ulonglong  # type: ignore


class AbstractAddress(ABC):
    @abstractmethod
    def resolve(self) -> int:
        pass


class AOBScan(AbstractAddress):
    def __init__(
        self,
        aob: bytes,
        *,
        add: int = 0,
        module_name: str | None = None,
        multiple_result_index: int | None = None,
        should_cache: bool = True,
    ):
        self._should_cache = should_cache
        self._saved_scan_result: int | None = None

        self.aob = aob
        self.add = add
        self.module_name = module_name
        self.multiple_result_index = multiple_result_index

    def resolve(self) -> int:
        if self._saved_scan_result is not None:
            return self._saved_scan_result

        return_multiple = self.multiple_result_index is not None

        if self.module_name is None:
            find_aob = partial(pattern_scan_all, pm.process_handle, return_multiple=return_multiple)
        else:
            module = module_from_name(pm.process_handle, self.module_name)

            if module is None:
                raise ValueError(f"Module not found: {self.module_name}")

            find_aob = partial(pattern_scan_module, pm.process_handle, module, return_multiple=return_multiple)

        scan_result: list[int] | int | None = find_aob(self.aob)

        if not scan_result:
            raise ValueError(f"AOB not found: {self.aob}")

        if isinstance(scan_result, list):
            result_address = scan_result[self.multiple_result_index]  # type: ignore
        else:
            result_address = scan_result

        result_address += self.add

        if self._should_cache:
            self._saved_scan_result = result_address

        return result_address


class Address(AbstractAddress):
    def __init__(self, base_address: int, offsets: list[int] | None = None, add: int = 0):
        self.base_address = base_address
        self.offsets = [] if offsets is None else offsets
        self.add = add

    def __add__(self, other: int | list[int]) -> Self:
        match other:
            case int(extra_add):
                new_add = self.add + extra_add
                return self.inherit(new_add=new_add)
            case list(extra_offsets):
                return self.inherit(extra_offsets=extra_offsets)
            case _:
                assert_never(other)

    def inherit(self, *, extra_offsets: list[int] | None = None, new_add: int | None = None) -> Self:
        new_address = self.__class__(self.base_address, self.offsets.copy(), self.add)

        if extra_offsets is not None:
            new_address.offsets.extend(extra_offsets)

        if new_add is not None:
            new_address.add = new_add

        return new_address

    def resolve(self) -> int:
        pointer = self.base_address
        for offset in self.offsets:
            pointer = read_pointer(pointer) + offset

        return pointer + self.add


def ensure_address(obj: ConvertibleToAddress) -> AbstractAddress:
    match obj:
        case AbstractAddress():
            return obj
        case int():
            return Address(obj)
        case bytes():
            return AOBScan(obj)
        case _:
            raise TypeError(f"Cannot create AbstractAddress from {type(obj)}")
