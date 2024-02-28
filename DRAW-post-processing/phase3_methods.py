# -*- coding: utf-8 -*-

# def baro_Eng_in2mb(ei):
#    return float(ei) * 33.86389


# def temp_f2c(tf):
#    return (5.0/9.0) * (float(tf)-32.0)


def depth_in2mm(pp):
    return (float(pp)*25.4)


def vel_mph2mps(vel):
    return float(vel*0.44704)


def dis_mi2m(dis):
    return float(dis*1609.34)
