#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2014 by trgk.
# All rights reserved.
# This file is part of EUD python library (eudplib), and is released under "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package.
from collections.abc import Iterator

from eudplib import core as c
from eudplib import ctrlstru as cs
from eudplib import utils as ut

from ...localize import _
from ..memiof import f_dwread_epd, f_getcurpl, f_setcurpl


@c.EUDTypedFunc([c.TrgPlayer], [None])
def f_playerexist(player):
    """Check if player has not left the game.

    :returns: 1 if player exists, 0 if not.
    """
    f_playerexist._frets = [c.SetDeaths(0, c.SetTo, 0, 0)]
    f_playerexist._retn = 1
    ret = c.EUDLightVariable(_from=f_playerexist._frets[0])
    pts = 0x51A280

    cs.EUDSwitch(player)
    block = ut.EUDGetLastBlockOfName("swblock")[1]
    block["_actions"] = ret.SetNumber(1)
    for p in ut.RandList(range(8)):
        if cs.EUDSwitchCase()(p):
            c.RawTrigger(
                nextptr=block["swend"],
                conditions=c.Memory(pts + p * 12 + 8, c.Exactly, ~(pts + p * 12 + 4)),
                actions=ret.SetNumber(0),
            )

    if cs.EUDSwitchDefault()():
        ret << 0
    cs.EUDEndSwitch()
    # return ret


# --------


def EUDLoopPlayer(
    ptype: str | None = "Human", force=None, race: str | None = None
) -> Iterator[c.EUDVariable]:
    def EncodeForce(f):
        force_dict = {c.Force1: 0, c.Force2: 1, c.Force3: 2, c.Force4: 3}
        if type(f) != int and f in force_dict:
            return force_dict[f]
        return f

    plist = []
    for p in range(8):
        pinfo = c.GetPlayerInfo(p)
        if (
            (not ptype or pinfo.typestr == ptype)
            and (not force or pinfo.force == EncodeForce(force))
            and (not race or pinfo.racestr == race)
        ):
            plist.append(p)
    ut.EUDCreateBlock("loopplayerblock", None)
    if not plist:
        errmsg = _("No player met condition for input map settings:")
        if ptype:
            errmsg += _(" type {}").format(ptype)
        if force:
            errmsg += _(" force {}").format(force)
        if race:
            errmsg += _(" race {}").format(race)
        errmsg += "\n" + _("Check out whether Start Locations are placed correctly.")
        raise ut.EPError(errmsg)
    start, end = min(plist), max(plist)

    v = c.EUDVariable()
    v << start
    if cs.EUDWhile()(v <= end):
        for i in range(start, end):
            if i not in plist:
                cs.EUDContinueIf(v == i)
        cs.EUDContinueIfNot(f_playerexist(v))
        yield v
        cs.EUDSetContinuePoint()
        v += 1
    cs.EUDEndWhile()
    ut.EUDPopBlock("loopplayerblock")


# -------


def EUDPlayerLoop():
    def _footer():
        block = {"origcp": f_getcurpl(), "playerv": c.EUDVariable()}
        playerv = block["playerv"]

        playerv << 0
        cs.EUDWhile()(playerv <= 7)
        cs.EUDContinueIfNot(f_playerexist(playerv))
        f_setcurpl(playerv)

        ut.EUDCreateBlock("ploopblock", block)
        return True

    return cs.CtrlStruOpener(_footer)


def EUDEndPlayerLoop():
    block = ut.EUDPopBlock("ploopblock")[1]
    playerv = block["playerv"]
    origcp = block["origcp"]

    if not cs.EUDIsContinuePointSet():
        cs.EUDSetContinuePoint()

    playerv += 1
    cs.EUDEndWhile()
    f_setcurpl(origcp)
