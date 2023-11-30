#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2014 by trgk.
# All rights reserved.
# This file is part of EUD python library (eudplib), and is released under "MIT License Agreement".
# Please see the LICENSE file that should have been included as part of this package.

from eudplib import core as c
from eudplib import ctrlstru as cs
from eudplib.trigger.tpatcher import NegateCondition
from eudplib.utils.eperror import EPError


def EUDOr(cond1, *conds) -> c.EUDLightBool:
    """cond1 || cond2 || ... || condn

    .. warning:: Short circuiting is not supported

    :param conds: List of conditions
    """

    v = c.EUDLightBool()
    if cs.EUDIf()(cond1):
        c.RawTrigger(actions=v.Set())
    for cond in conds:
        if cs.EUDElseIf()(cond):
            c.RawTrigger(actions=v.Set())
    if cs.EUDElse()():
        c.RawTrigger(actions=v.Clear())
    cs.EUDEndIf()
    return v


def EUDAnd(cond1, *conds) -> c.EUDLightBool:
    """cond1 && cond2 && ... && condn

    .. note::
        This function computes AND value of various conditions.
        If you don't want to do much computation, you should better use
        plain list instead of this function.

    .. warning:: Short circuiting is not supported.

    :param conds: List of conditions
    """

    v = c.EUDLightBool()
    if cs.EUDIfNot()(cond1):
        c.RawTrigger(actions=v.Clear())
    for cond in conds:
        if cs.EUDElseIfNot()(cond):
            c.RawTrigger(actions=v.Clear())
    if cs.EUDElse()():
        c.RawTrigger(actions=v.Set())
    cs.EUDEndIf()
    return v


def EUDNot(cond):
    """!cond

    :param conds: Condition to negate
    """

    if c.IsEUDVariable(cond):
        # TODO: better handle !v in conditional
        v = c.EUDVariable()
        v << 0
        c.RawTrigger(
            conditions=cond.Exactly(0),
            actions=v.SetNumber(1),
        )
        return v

    if isinstance(cond, bool):
        if cond:
            return False
        return True
    try:
        return NegateCondition(cond)
    except (AttributeError, EPError):
        pass
    v = c.EUDLightBool()
    c.RawTrigger(actions=v.Set())
    if cs.EUDIf()(cond):
        c.RawTrigger(actions=v.Clear())
    cs.EUDEndIf()
    return v
