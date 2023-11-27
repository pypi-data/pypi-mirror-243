"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Copyright (C) 2023 Michael Hall <https://github.com/mikeshardmind>
"""
# intentional restructuring the problem space a bit from solver.py
# Goal of simplifying the problem of allowing complex conditions to be expressible and performant

from __future__ import annotations

import enum
import operator
from collections.abc import Callable
from typing import Literal

from msgspec import Struct, field
from msgspec.structs import astuple, replace


class ClassesEnum(enum.IntEnum):
    EMPTY = -1
    Feca = 0
    Osa = 1
    Osamodas = Osa
    Enu = 2
    Enutrof = Enu
    Sram = 3
    Xel = 4
    Xelor = Xel
    Eca = 5
    Ecaflip = Eca
    Eni = 6
    Eniripsa = Eni
    Iop = 7
    Cra = 8
    Sadi = 9
    Sadida = Sadi
    Sac = 10
    Sacrier = Sac
    Panda = 11
    Pandawa = Panda
    Rogue = 12
    Masq = 13
    Masqueraiders = Masq
    Ougi = 14
    Ouginak = Ougi
    Fog = 15
    Foggernaut = Fog
    Elio = 16
    Eliotrope = Elio
    Hupper = 17
    Huppermage = Hupper


class ElementsEnum(enum.IntFlag, boundary=enum.STRICT):
    empty = 0
    fire = 1 << 0
    earth = 1 << 1
    water = 1 << 2
    air = 1 << 3


class Priority(enum.IntEnum):
    unvalued = 0
    prioritized = 1
    full_negative_only = 2
    half_negative_only = 4


class StatPriority(Struct, frozen=True, array_like=True):
    distance_mastery: Priority = Priority.unvalued
    melee_mastery: Priority = Priority.unvalued
    heal_mastery: Priority = Priority.unvalued
    rear_mastery: Priority = Priority.unvalued
    berserk_mastery: Priority = Priority.unvalued
    elements: ElementsEnum = ElementsEnum.empty

    @property
    def is_valid(self) -> bool:
        return all(x < 2 for x in (self.distance_mastery, self.melee_mastery, self.heal_mastery))


class Stats(Struct, frozen=True, gc=True):
    ap: int = 0
    mp: int = 0
    wp: int = 0
    ra: int = 0
    crit: int = 0
    crit_mastery: int = 0
    elemental_mastery: int = 0
    one_element_mastery: int = 0
    two_element_mastery: int = 0
    three_element_mastery: int = 0
    distance_mastery: int = 0
    rear_mastery: int = 0
    heal_mastery: int = 0
    beserk_mastery: int = 0
    melee_mastery: int = 0
    control: int = 0
    block: int = 0
    fd: int = 0
    heals_performed: int = 0
    lock: int = 0
    dodge: int = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stats):
            return NotImplemented
        return astuple(self) == astuple(other)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Stats):
            return NotImplemented
        return astuple(self) != astuple(other)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Stats):
            return NotImplemented

        return all(s < o for s, o in zip(astuple(self), astuple(other), strict=True))

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Stats):
            return NotImplemented

        return all(s <= o for s, o in zip(astuple(self), astuple(other), strict=True))

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Stats):
            return NotImplemented

        return all(s > o for s, o in zip(astuple(self), astuple(other), strict=True))

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Stats):
            return NotImplemented

        return all(s >= o for s, o in zip(astuple(self), astuple(other), strict=True))

    def __sub__(self, other: object) -> Stats:
        if not isinstance(other, Stats):
            return NotImplemented

        return Stats(*(operator.sub(s, o) for s, o in zip(astuple(self), astuple(other), strict=True)))

    def __add__(self, other: object) -> Stats:
        if not isinstance(other, Stats):
            return NotImplemented

        return Stats(*(operator.add(s, o) for s, o in zip(astuple(self), astuple(other), strict=True)))


DUMMY_MIN: int = -1_000_000
DUMMY_MAX: int = 1_000_000


class SetMinimums(Stats, frozen=True, gc=False):
    ap: int = DUMMY_MIN
    mp: int = DUMMY_MIN
    wp: int = DUMMY_MIN
    ra: int = DUMMY_MIN
    crit: int = DUMMY_MIN
    crit_mastery: int = DUMMY_MIN
    elemental_mastery: int = DUMMY_MIN
    one_element_mastery: int = DUMMY_MIN
    two_element_mastery: int = DUMMY_MIN
    three_element_mastery: int = DUMMY_MIN
    distance_mastery: int = DUMMY_MIN
    rear_mastery: int = DUMMY_MIN
    heal_mastery: int = DUMMY_MIN
    beserk_mastery: int = DUMMY_MIN
    melee_mastery: int = DUMMY_MIN
    control: int = DUMMY_MIN
    block: int = DUMMY_MIN
    fd: int = DUMMY_MIN
    heals_performed: int = DUMMY_MIN
    lock: int = DUMMY_MIN
    dodge: int = DUMMY_MIN

    def unhandled(self) -> bool:
        _ap, _mp, _wp, _ra, _crit, *rest = astuple(self)
        return any(stat != DUMMY_MIN for stat in rest)

    def __and__(self, other: object) -> SetMinimums:
        if not isinstance(other, SetMinimums):
            return NotImplemented

        return SetMinimums(*(max(s, o) for s, o in zip(astuple(self), astuple(other), strict=True)))


class SetMaximums(Stats, frozen=True, gc=False):
    ap: int = DUMMY_MAX
    mp: int = DUMMY_MAX
    wp: int = DUMMY_MAX
    ra: int = DUMMY_MAX
    crit: int = DUMMY_MAX
    crit_mastery: int = DUMMY_MAX
    elemental_mastery: int = DUMMY_MAX
    one_element_mastery: int = DUMMY_MAX
    two_element_mastery: int = DUMMY_MAX
    three_element_mastery: int = DUMMY_MAX
    distance_mastery: int = DUMMY_MAX
    rear_mastery: int = DUMMY_MAX
    heal_mastery: int = DUMMY_MAX
    beserk_mastery: int = DUMMY_MAX
    melee_mastery: int = DUMMY_MAX
    control: int = DUMMY_MAX
    block: int = DUMMY_MAX
    fd: int = DUMMY_MAX
    heals_performed: int = DUMMY_MAX
    lock: int = DUMMY_MAX
    dodge: int = DUMMY_MAX

    def unhandled(self) -> bool:
        _ap, _mp, _wp, _ra, _crit, *rest = astuple(self)
        return any(stat != DUMMY_MAX for stat in rest)

    def __and__(self, other: object) -> SetMaximums:
        if not isinstance(other, SetMaximums):
            return NotImplemented

        return SetMaximums(*(min(s, o) for s, o in zip(astuple(self), astuple(other), strict=True)))


def effective_mastery(stats: Stats, rel_mastery_key: Callable[[Stats], int]) -> float:
    # there's a hidden 3% base crit rate in game
    # There's also clamping on crit rate
    crit_rate = max(min(stats.crit + 3, 100), 0)

    fd = 1 + (stats.fd / 100)

    rel_mastery = rel_mastery_key(stats)

    return (rel_mastery * (100 - crit_rate) / 100) * fd + ((rel_mastery + stats.crit_mastery) * crit_rate * (fd + 0.25))


def effective_healing(stats: Stats, rel_mastery_key: Callable[[Stats], int]) -> float:
    """
    We assume a worst case "heals didn't crit" for healing,
    under the philosophy of minimum healing required for safety.

    Crits under this philosophy *may* allow cutting a heal from a rotation on reaction
    making crit a damage stat even in the case of optimizing healing
    """
    return rel_mastery_key(stats) * (1 + (stats.heals_performed / 100))


def apply_w2h(stats: Stats) -> Stats:
    return replace(stats, ap=stats.ap + 2, mp=stats.mp - 2)


def apply_unravel(stats: Stats) -> Stats:
    if stats.crit >= 40:
        return replace(stats, elemental_mastery=stats.elemental_mastery + stats.crit_mastery, crit_mastery=0)
    return stats


def apply_elementalism(stats: Stats) -> Stats:
    if (stats.one_element_mastery == stats.two_element_mastery == 0) and stats.three_element_mastery != 0:
        return replace(stats, fd=stats.fd + 30, heals_performed=stats.heals_performed + 30)
    return stats


class v1Config(Struct, kw_only=True):
    lv: int = 230
    ap: int = 5
    mp: int = 2
    wp: int = 0
    ra: int = 0
    num_mastery: int = 3
    dist: bool = False
    melee: bool = False
    zerk: bool = False
    rear: bool = False
    heal: bool = False
    unraveling: bool = False
    skipshields: bool = False
    lwx: bool = False
    bcrit: int = 0
    bmast: int = 0
    bcmast: int = 0
    forbid: list[str] = field(default_factory=list)
    idforbid: list[int] = field(default_factory=list)
    idforce: list[int] = field(default_factory=list)
    twoh: bool = False
    skiptwo_hand: bool = False
    locale: Literal["en", "fr", "pt", "es"] = "en"
    dry_run: bool = False
    hard_cap_depth: int = 25
    negzerk: Literal["full", "half", "none"] = "none"
    negrear: Literal["full", "half", "none"] = "none"
    forbid_rarity: list[int] = field(default_factory=list)
    allowed_rarities: list[int] = field(default_factory=lambda: [1, 2, 3, 4, 5, 6, 7])
    nameforce: list[str] = field(default_factory=list)
    tolerance: int = 30
    # Don't modify the below in wakforge, too slow
    exhaustive: bool = False
    search_depth: int = 1
    # dont touch these in wakforge either
    baseap: int = 0
    basemp: int = 0
    bawewp: int = 0
    basera: int = 0
    elements: ElementsEnum = ElementsEnum.empty
