from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import partial, wraps
from typing import Any, Self, override
from uuid import uuid4

from dearpygui import dearpygui as dpg
from keyboard import add_hotkey
from pymem.exception import MemoryReadError, MemoryWriteError

from trainerbase.codeinjection import AbstractCodeInjection
from trainerbase.common import ShortLongPressSwitch, Switchable, Teleport
from trainerbase.gameobject import (
    GameBool,
    GameByte,
    GameDouble,
    GameFloat,
    GameInt,
    GameLongLong,
    GameObject,
    GameShort,
    GameUnsignedInt,
    GameUnsignedLongLong,
    GameUnsignedShort,
)
from trainerbase.scriptengine import Script
from trainerbase.speedhack import SpeedHack
from trainerbase.tts import say


TAG_TELEPORT_LABELS = "__teleport_labels"
TAG_SPEEDHACK_FACTOR_INPUT = "tag_speedhack_factor_input"


class AbstractUIComponent(ABC):
    @abstractmethod
    def add_to_ui(self) -> None:
        pass


class ScriptUI(AbstractUIComponent):
    DPG_TAG_PREFIX = "script__"

    def __init__(
        self,
        script: Script,
        label: str,
        hotkey: str | None = None,
        tts_on_hotkey: bool = True,
    ):
        self.script = script
        self.pure_label = label
        self.label_with_hotkey = label if hotkey is None else f"[{hotkey}] {label}"
        self.hotkey = hotkey
        self.tts_on_hotkey = tts_on_hotkey

        self.dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"

    @override
    def add_to_ui(self) -> None:
        if self.hotkey is not None:
            add_hotkey(self.hotkey, self.on_hotkey_press)

        dpg.add_checkbox(
            label=self.label_with_hotkey,
            tag=self.dpg_tag,
            callback=self.on_script_state_change,
            default_value=self.script.enabled,
        )

    def on_script_state_change(self):
        self.script.enabled = dpg.get_value(self.dpg_tag)

    def on_hotkey_press(self):
        dpg.set_value(self.dpg_tag, not dpg.get_value(self.dpg_tag))

        self.on_script_state_change()

        if self.tts_on_hotkey:
            status = "enabled" if self.script.enabled else "disabled"
            say(f"Script {self.pure_label} {status}")


class CodeInjectionUI(AbstractUIComponent):
    DPG_TAG_PREFIX = "injection__"

    def __init__(
        self,
        injection: AbstractCodeInjection,
        label: str,
        hotkey: str | None = None,
        tts_on_hotkey: bool = True,
    ):
        self.injection = injection
        self.pure_label = label
        self.label_with_hotkey = label if hotkey is None else f"[{hotkey}] {label}"
        self.hotkey = hotkey
        self.tts_on_hotkey = tts_on_hotkey

        self.dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"

    @override
    def add_to_ui(self) -> None:
        if self.hotkey is not None:
            add_hotkey(self.hotkey, self.on_hotkey_press)

        dpg.add_checkbox(label=self.label_with_hotkey, tag=self.dpg_tag, callback=self.on_codeinjection_state_change)

    def on_codeinjection_state_change(self):
        if dpg.get_value(self.dpg_tag):
            change_codeinjection_state = self.injection.inject
        else:
            change_codeinjection_state = self.injection.eject

        try:
            change_codeinjection_state()
        except (MemoryReadError, MemoryWriteError):
            dpg.set_value(self.dpg_tag, not dpg.get_value(self.dpg_tag))

    def on_hotkey_press(self):
        dpg.set_value(self.dpg_tag, not dpg.get_value(self.dpg_tag))
        self.on_codeinjection_state_change()

        if self.tts_on_hotkey:
            status = "applied" if dpg.get_value(self.dpg_tag) else "removed"
            say(f"CodeInjection {self.pure_label} {status}")


class GameObjectUI(AbstractUIComponent):
    DPG_TAG_PREFIX = "object__"
    DPG_TAG_POSTFIX_IS_FROZEN = "__frozen"
    DPG_TAG_POSTFIX_GETTER = "__getter"
    DPG_TAG_POSTFIX_SETTER = "__setter"

    displayed_objects: list[Self] = []

    def __init__(
        self,
        gameobject: GameObject,
        label: str,
        hotkey: str | None = None,
        default_setter_input_value: Any = 0,
        before_set: Callable | None = None,
        tts_on_hotkey: bool = True,
    ):
        self.gameobject = gameobject
        self.pure_label = label
        self.label_with_hotkey = label if hotkey is None else f"[{hotkey}] {label}"
        self.hotkey = hotkey
        self.default_setter_input_value = default_setter_input_value
        self.before_set = before_set
        self.tts_on_hotkey = tts_on_hotkey

        dpg_tag = f"{self.DPG_TAG_PREFIX}{uuid4()}"
        self.dpg_tag_frozen = f"{dpg_tag}{self.DPG_TAG_POSTFIX_IS_FROZEN}"
        self.dpg_tag_getter = f"{dpg_tag}{self.DPG_TAG_POSTFIX_GETTER}"
        self.dpg_tag_setter = f"{dpg_tag}{self.DPG_TAG_POSTFIX_SETTER}"

    @override
    def add_to_ui(self) -> None:
        if self.hotkey is not None:
            add_hotkey(self.hotkey, self.on_hotkey_press)

        match self.gameobject:
            case GameFloat():
                add_setter_input = dpg.add_input_float
            case GameDouble():
                add_setter_input = dpg.add_input_double
            case GameByte() | GameShort() | GameInt() | GameLongLong() | GameBool():
                add_setter_input = dpg.add_input_int
            case GameUnsignedShort() | GameUnsignedInt() | GameUnsignedLongLong():
                add_setter_input = partial(dpg.add_input_int, min_clamped=True, min_value=0)
            case _:
                add_setter_input = dpg.add_input_text

        with dpg.group(horizontal=True):
            dpg.add_checkbox(tag=self.dpg_tag_frozen, callback=self.on_frozen_state_change)
            dpg.add_text(self.label_with_hotkey)
            dpg.add_input_text(width=220, tag=self.dpg_tag_getter, readonly=True)
            add_setter_input(width=220, tag=self.dpg_tag_setter, default_value=self.default_setter_input_value)
            dpg.add_button(label="Set", callback=self.on_value_set)

        GameObjectUI.displayed_objects.append(self)

    def on_frozen_state_change(self):
        try:
            self.gameobject.frozen = self.gameobject.value if dpg.get_value(self.dpg_tag_frozen) else None
        except MemoryReadError:
            dpg.set_value(self.dpg_tag_frozen, False)

    def on_value_set(self):
        raw_new_value = dpg.get_value(self.dpg_tag_setter)
        new_value = raw_new_value if self.before_set is None else self.before_set(raw_new_value)

        if self.gameobject.frozen is None:
            try:
                self.gameobject.value = new_value
            except MemoryWriteError:
                pass
        else:
            self.gameobject.frozen = new_value

    def on_hotkey_press(self):
        dpg.set_value(self.dpg_tag_frozen, not dpg.get_value(self.dpg_tag_frozen))

        self.on_frozen_state_change()

        if self.tts_on_hotkey:
            status = "released" if self.gameobject.frozen is None else "frozen"
            say(f"GameObject {self.pure_label} {status}")


class TeleportUI(AbstractUIComponent):
    def __init__(
        self,
        tp: Teleport,
        hotkey_save_position: str | None = None,
        hotkey_set_saved_position: str | None = None,
        hotkey_dash: str | None = None,
        tts_on_hotkey: bool = True,
    ):
        self.tp = tp
        self.hotkey_save_position = hotkey_save_position
        self.hotkey_set_saved_position = hotkey_set_saved_position
        self.hotkey_dash = hotkey_dash
        self.tts_on_hotkey = tts_on_hotkey

    @override
    def add_to_ui(self) -> None:
        self._tp_add_save_set_position_hotkeys_if_needed()
        self._tp_add_dash_hotkeys_if_needed()

        add_components(
            GameObjectUI(self.tp.player_x, "X"),
            GameObjectUI(self.tp.player_y, "Y"),
            GameObjectUI(self.tp.player_z, "Z"),
        )

        self._tp_add_labels_if_needed()

        dpg.add_button(label="Clip Coords", callback=self.on_clip_coords)

    def on_clip_coords(self):
        dpg.set_clipboard_text(repr(self.tp.get_coords()))

    def on_hotkey_save_position_press(self):
        self.tp.save_position()

        if self.tts_on_hotkey:
            say("Position saved")

    def on_hotkey_set_saved_position_press(self):
        is_position_restored = self.tp.restore_saved_position()

        if self.tts_on_hotkey:
            say("Position restored" if is_position_restored else "Save position at first")

    def on_hotkey_dash_press(self):
        self.tp.dash()
        if self.tts_on_hotkey:
            say("Dash!")

    def on_goto_label(self):
        self.tp.goto(dpg.get_value(TAG_TELEPORT_LABELS))

    def _tp_add_save_set_position_hotkeys_if_needed(self):
        if self.hotkey_save_position is None or self.hotkey_set_saved_position is None:
            return

        add_hotkey(self.hotkey_save_position, self.on_hotkey_save_position_press)
        add_hotkey(self.hotkey_set_saved_position, self.on_hotkey_set_saved_position_press)

        dpg.add_text(f"[{self.hotkey_save_position}] Save Position")
        dpg.add_text(f"[{self.hotkey_set_saved_position}] Set Saved Position")

    def _tp_add_dash_hotkeys_if_needed(self):
        if self.hotkey_dash is None:
            return

        add_hotkey(self.hotkey_dash, self.on_hotkey_dash_press)

        dpg.add_text(f"[{self.hotkey_dash}] Dash")

    def _tp_add_labels_if_needed(self):
        if not self.tp.labels:
            return

        labels = sorted(self.tp.labels.keys())

        with dpg.group(horizontal=True):
            dpg.add_button(label="Go To", callback=self.on_goto_label)
            dpg.add_combo(label="Labels", tag=TAG_TELEPORT_LABELS, items=labels, default_value=labels[0])


class SpeedHackUI(AbstractUIComponent):
    def __init__(self, speedhack: SpeedHack, key: str):
        self.speedhack = speedhack
        self.key = key
        self.switch = ShortLongPressSwitch(SpeedHackUISwitch(speedhack, TAG_SPEEDHACK_FACTOR_INPUT), key)

    @override
    def add_to_ui(self) -> None:
        dpg.add_text(f"Hold [{self.key}] Enable SpeedHack")
        dpg.add_text(f"Press [{self.key}] Toggle SpeedHack")

        dpg.add_input_double(
            tag=TAG_SPEEDHACK_FACTOR_INPUT,
            label="SpeedHack Factor",
            min_value=0.0,
            max_value=100.0,
            default_value=3.0,
            min_clamped=True,
            max_clamped=True,
        )

        self.switch.handle()


class SpeedHackUISwitch(Switchable):
    def __init__(self, speedhack: SpeedHack, dpg_tag: str):
        self.speedhack = speedhack
        self.dpg_tag = dpg_tag

    @override
    def enable(self):
        self.speedhack.factor = dpg.get_value(self.dpg_tag)

    @override
    def disable(self):
        self.speedhack.factor = 1.0


def add_components(*components: AbstractUIComponent):
    for component in components:
        component.add_to_ui()


def simple_trainerbase_menu(window_title: str, width: int, height: int):
    def menu_decorator(initializer: Callable):
        @wraps(initializer)
        def run_menu_wrapper(on_initialized: Callable):
            dpg.create_context()
            dpg.create_viewport(
                title=window_title,
                min_width=width,
                min_height=height,
                width=width,
                height=height,
            )
            dpg.setup_dearpygui()

            with dpg.window(
                label=window_title,
                tag="menu",
                min_size=[width, height],
                no_close=True,
                no_move=True,
                no_title_bar=True,
                horizontal_scrollbar=True,
            ):
                initializer()

            dpg.show_viewport()

            on_initialized()

            dpg.start_dearpygui()
            dpg.destroy_context()

        return run_menu_wrapper

    return menu_decorator


def update_displayed_objects():
    for game_object_ui in GameObjectUI.displayed_objects:
        try:
            new_value = game_object_ui.gameobject.value
        except MemoryReadError:
            new_value = "<Unresolved>"

        dpg.set_value(game_object_ui.dpg_tag_getter, new_value)
