# -*- coding: utf-8 -*-

#  iso conversions that are not in lmrlib.py


def depth_in2mm(pp):
    return (float(pp)*25.4)


def vel_mph2mps(vel):
    return float(vel*0.44704)


def dis_mi2m(dis):
    return float(dis*1609.34)
