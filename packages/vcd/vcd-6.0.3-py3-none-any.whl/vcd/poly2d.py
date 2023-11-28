"""
Module to handle representations fo 2D polygons.

This module implements functions to transform and handle poly2D elements.
"""
# VCD (Video Content Description) library.
#
# Project website: http://vcd.vicomtech.org
#
# Copyright (C) 2023, Vicomtech (http://www.vicomtech.es/),
# (Spain) all rights reserved.
#
# VCD is a Python library to create and manage OpenLABEL content.
# VCD is distributed under MIT License. See LICENSE.

from __future__ import annotations

import math

import numpy as np


def compute_rs6fcc(coords: tuple | list) -> tuple[list[int], int, int, int, int]:
    """
    Convert the polyline points using RS6FCC method.

    Args:
        coords (list): list of x, y coordinates of the polyline points.
    """
    _distances = []
    # high_symbol = 7
    # low_symbol = 6

    if len(coords) == 0:
        return [], 0, 0, 0, 0

    _xinit = int(coords[0])
    _yinit = int(coords[1])
    xinit = _xinit
    yinit = _yinit

    static_direction_kernel = np.array([[5, 6, 7], [4, 9, 0], [3, 2, 1]])

    kernel_direction_data = np.array(
        [
            [[5, 4, 2], [5, 9, 0], [5, 3, 1]],  # direction 0 updated kernel
            [[5, 5, 4], [5, 9, 2], [3, 1, 0]],  # direction 1 updated kernel
            [[5, 5, 5], [3, 9, 4], [1, 0, 2]],  # direction 2 updated kernel
            [[3, 5, 5], [1, 9, 5], [0, 2, 4]],  # direction 3 updated kernel
            [[1, 3, 5], [0, 9, 5], [2, 4, 5]],  # direction 4 updated kernel
            [[0, 1, 3], [2, 9, 5], [4, 5, 5]],  # direction 5 updated kernel
            [[2, 0, 1], [4, 9, 3], [5, 5, 5]],  # direction 6 updated kernel
            [[4, 2, 0], [5, 9, 1], [5, 5, 3]],
        ]
    )  # direction 7 updated kernel
    # the polygon contouring starts always going down.
    previous_direction = 2

    for i in range(2, len(coords), 2):
        x = round(coords[i])
        y = round(coords[i + 1])
        xi = x - xinit
        yi = y - yinit
        temp = []
        fin = max(abs(xi), abs(yi))

        xii = int(xi / abs(xi)) if xi != 0 else 0
        yii = int(yi / abs(yi)) if yi != 0 else 0

        for _j in range(0, fin):
            move = kernel_direction_data[previous_direction][yii + 1][xii + 1]
            if move < 5:
                temp.append(move)
                previous_direction = static_direction_kernel[yii + 1][xii + 1]
            elif move == 5:
                temp.append(move)
                previous_direction = (previous_direction + 4) % 8
                move = kernel_direction_data[previous_direction][yii + 1][xii + 1]
                temp.append(move)
                previous_direction = static_direction_kernel[yii + 1][xii + 1]

        for _, elem in enumerate(temp):
            _distances.append(elem)

        xinit = x
        yinit = y

    if len(_distances) != 0:
        (
            _distances,
            rs6fcc_low_simplifier,
            rs6fcc_high_simplifier,
        ) = simplify_calculated_front_sequence_movements(_distances)
    else:
        rs6fcc_high_simplifier = 0
        rs6fcc_low_simplifier = 0

    return _distances, rs6fcc_low_simplifier, rs6fcc_high_simplifier, _xinit, _yinit


def extract_rs6fcc2points(
    _chaincode: list[int], _xinit: int, _yinit: int, _low: int, _high: int
) -> list[int]:
    rs6fcc_high_simplifier = _high
    rs6fcc_low_simplifier = _low
    rs6fcc_high_symbol = 7
    rs6fcc_low_symbol = 6
    _coords = []
    _coords.append(int(_xinit))
    _coords.append(int(_yinit))
    xinit = int(_xinit)
    yinit = int(_yinit)
    if len(_chaincode) == 0:
        return _coords

    static_direction_kernel = np.array([[5, 6, 7], [4, 9, 0], [3, 2, 1]])

    kernel_direction_data = np.array(
        [
            [[5, 4, 2], [5, 9, 0], [5, 3, 1]],  # direction 0 updated kernel
            [[5, 5, 4], [5, 9, 2], [3, 1, 0]],  # direction 1 updated kernel
            [[5, 5, 5], [3, 9, 4], [1, 0, 2]],  # direction 2 updated kernel
            [[3, 5, 5], [1, 9, 5], [0, 2, 4]],  # direction 3 updated kernel
            [[1, 3, 5], [0, 9, 5], [2, 4, 5]],  # direction 4 updated kernel
            [[0, 1, 3], [2, 9, 5], [4, 5, 5]],  # direction 5 updated kernel
            [[2, 0, 1], [4, 9, 3], [5, 5, 5]],  # direction 6 updated kernel
            [[4, 2, 0], [5, 9, 1], [5, 5, 3]],
        ]
    )  # direction 7 updated kernel
    # the polygon contouring starts always going down.
    previous_direction = 2

    counter = 0
    for i, code in enumerate(_chaincode):
        if 6 > code > 0:
            if counter > 0:
                x, y = check_pixel_in_mat(kernel_direction_data[previous_direction], 0)
                xinit += x * counter if x != 0 else 0
                yinit += y * counter if y != 0 else 0
                _coords.append(xinit)
                _coords.append(yinit)
                counter = 0

            if code == 5:
                previous_direction = (previous_direction + 4) % 8
            else:
                xi, yi = check_pixel_in_mat(
                    kernel_direction_data[previous_direction], code
                )
                xinit += xi
                yinit += yi
                _coords.append(xinit)
                _coords.append(yinit)
                previous_direction = static_direction_kernel[yi + 1][xi + 1]

        elif code == 0:
            counter += 1
        elif code == rs6fcc_low_symbol:
            counter += rs6fcc_low_simplifier
        elif code == rs6fcc_high_symbol:
            counter += rs6fcc_high_simplifier

        if i == len(_chaincode) - 1 and counter > 0:
            x, y = check_pixel_in_mat(kernel_direction_data[previous_direction], 0)
            xinit += x * counter if x != 0 else 0
            yinit += y * counter if y != 0 else 0
            _coords.append(xinit)
            _coords.append(yinit)

    return _coords


def compute_srf6dcc(_coords: tuple | list) -> tuple[list[int], int, int]:
    _distances = []
    srf6dcc_high_simplifier = 15
    srf6dcc_low_simplifier = 3
    srf6dcc_high_symbol = 7
    srf6dcc_low_symbol = 6
    if len(_coords) == 0:
        return [], 0, 0
    _xinit = int(_coords[0])
    _yinit = int(_coords[1])
    xinit = _xinit
    yinit = _yinit

    static_direction_kernel = np.array([[5, 6, 7], [4, 9, 0], [3, 2, 1]])

    kernel_direction_data = np.array(
        [
            [[5, 4, 2], [5, 9, 0], [5, 3, 1]],  # direction 0 updated kernel
            [[5, 5, 4], [5, 9, 2], [3, 1, 0]],  # direction 1 updated kernel
            [[5, 5, 5], [3, 9, 4], [1, 0, 2]],  # direction 2 updated kernel
            [[3, 5, 5], [1, 9, 5], [0, 2, 4]],  # direction 3 updated kernel
            [[1, 3, 5], [0, 9, 5], [2, 4, 5]],  # direction 4 updated kernel
            [[0, 1, 3], [2, 9, 5], [4, 5, 5]],  # direction 5 updated kernel
            [[2, 0, 1], [4, 9, 3], [5, 5, 5]],  # direction 6 updated kernel
            [[4, 2, 0], [5, 9, 1], [5, 5, 3]],
        ]
    )  # direction 7 updated kernel
    # the polygon contouring starts always going down.
    # the polygon contouring starts always going down.
    previous_direction = 2
    for i in range(2, len(_coords), 2):
        x = round(_coords[i])
        y = round(_coords[i + 1])
        xi = x - xinit
        yi = y - yinit
        temp = []
        fin = max(abs(xi), abs(yi))

        xii = int(xi / abs(xi)) if xi != 0 else 0
        yii = int(yi / abs(yi)) if yi != 0 else 0

        for _j in range(0, fin):
            move = kernel_direction_data[previous_direction][yii + 1][xii + 1]
            if move < 5:
                temp.append(move)
                previous_direction = static_direction_kernel[yii + 1][xii + 1]
            elif move == 5:
                temp.append(move)
                previous_direction = (previous_direction + 4) % 8
                move = kernel_direction_data[previous_direction][yii + 1][xii + 1]
                temp.append(move)
                previous_direction = static_direction_kernel[yii + 1][xii + 1]

        for _, elem in enumerate(temp):
            _distances.append(elem)

        xinit = x
        yinit = y

        if len(_distances) != 0:
            _distances = simplify_all_front_sequence_movements(
                _distances,
                srf6dcc_low_simplifier,
                srf6dcc_high_simplifier,
                srf6dcc_low_symbol,
                srf6dcc_high_symbol,
            )
    return _distances, _xinit, _yinit


def extract_srf6dcc2points(_chaincode: list[int], _xinit: int, _yinit: int) -> list[int]:
    srf6dcc_high_simplifier = 15
    srf6dcc_low_simplifier = 3
    return extract_rs6fcc2points(
        _chaincode, _xinit, _yinit, srf6dcc_low_simplifier, srf6dcc_high_simplifier
    )


def check_pixel_in_mat(
    _kernel_direction_data: list[list[int]], target: int
) -> tuple[int, int]:
    for row in range(0, 3):
        for col in range(0, 3):
            if _kernel_direction_data[row][col] == target:
                return col - 1, row - 1
    return 0, 0


def check_value_in_kernel(
    _kernel_direction_data: list[list[int]], target: int
) -> tuple[int, int]:
    for row in range(0, 3):
        for col in range(0, 3):
            if _kernel_direction_data[row][col] == target:
                return col, row
    return 0, 0


def simplify_front_sequence_movements(
    _num: int,
    _low: int,
    _high: int,
    _low_symbol: int,
    _high_symbol: int,
    _next_steps: list[int],
) -> list[int]:
    if _high != -1:
        res1 = int(math.floor(_num / _high))
        res2 = int(_num % _high / _low)
        res3 = int(_num % _high % _low)
    else:
        res1 = 0
        res2 = int(_num / _low)
        res3 = int(_num % _low)

    for _i in range(0, res1):
        # _high_symbol: {SRF6DCC: 7} for high Roman numerals-like counting simplifications
        _next_steps.append(_high_symbol)
    for _i in range(0, res2):
        # _low_symbol: {SRF6DCC: 6} for low Roman numerals-like counting simplifications
        _next_steps.append(_low_symbol)
    for _i in range(0, res3):
        _next_steps.append(0)
    return _next_steps


def simplify_all_front_sequence_movements(
    _chaincode: list[int], _low: int, _high: int, _low_symbol: int, _high_symbol: int
) -> list[int]:
    counter = 0
    i = 0
    while i < len(_chaincode):
        if _chaincode[i] == 0:
            counter += 1
        elif _chaincode[i] != 0:
            if counter >= _low:
                # i - counter //position of last 0 - counter
                next_steps: list[int] = []
                next_steps = simplify_front_sequence_movements(
                    counter, _low, _high, _low_symbol, _high_symbol, next_steps
                )
                del _chaincode[i - counter : i]
                i -= counter
                _chaincode[i:i] = next_steps
                i += len(next_steps)
            counter = 0
        if i == len(_chaincode) - 1:
            if counter >= _low:
                next_steps = []
                next_steps = simplify_front_sequence_movements(
                    counter, _low, _high, _low_symbol, _high_symbol, next_steps
                )
                del _chaincode[len(_chaincode) - counter : len(_chaincode)]
                i -= counter
                _chaincode[len(_chaincode) : len(_chaincode)] = next_steps
                i += len(next_steps)
            counter = 0
        i += 1
    return _chaincode


def base64_encoder(_num: int) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return alphabet[_num]


def base64_decoder(_value: str) -> int:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return alphabet.find(_value)


# Converts a vector of chaincode integers into a json printable characters string.
# By joining the digits to compose a 6 bits integer and the converting that integer in
# base64 character.
def chaincode_base64_encoder(
    _chaincodevector: list[int], _chaincode_bits: int
) -> tuple[str, int]:
    # Add odd number in the vector for codification
    num_digits = int(6 / _chaincode_bits)
    _outputstring = ""
    rest = len(_chaincodevector) % num_digits
    if rest != 0:
        vectrest = int(num_digits - rest)
        for _i in range(0, vectrest):
            _chaincodevector.append(0)
    else:
        vectrest = 0
    for i in range(0, len(_chaincodevector), num_digits):
        byte = 0
        for j in range(0, num_digits):
            byte += _chaincodevector[i + j] << (num_digits - 1 - j) * _chaincode_bits
        _outputstring += base64_encoder(byte)
    return _outputstring, vectrest


# Converts back the json printable characters string to a vector of chaincode integers.
# By converting from base64 to 6bits integer and then splitting in chain code vector.
def chaincode_base64_decoder(
    _chaincodebits: str, _chaincode_bits: int, _bitsvectorrest: int
) -> list[int]:
    _chaincodevector: list[int] = []
    num_digits = int(6 / _chaincode_bits)
    getbits = pow(2, _chaincode_bits) - 1  # number of bits that need to move to

    for i, chaincode in enumerate(_chaincodebits):
        byte = base64_decoder(chaincode)
        for _j in range(0, num_digits):
            number = byte & getbits
            _chaincodevector.insert(i * num_digits, number)
            byte -= number
            byte = byte >> _chaincode_bits

    for _k in range(0, _bitsvectorrest):
        _chaincodevector.pop(len(_chaincodevector) - 1)

    return _chaincodevector


def calculate_multiplier(val: float, x: float) -> int:
    return int(math.floor(val / x) + (val % x))


def calculate_multiplier2(val: float, x: float, y: float) -> int:
    return calculate_multiplier(math.floor(val / y) + (val % y), x)


def extract_multiplier_map(in_map: dict) -> int:
    min_repetition = 0
    min_suma = math.inf
    for key_i in in_map:
        suma = 0
        for key_j in in_map:
            suma += in_map[key_j] * calculate_multiplier(key_j, key_i)
        if suma < min_suma:
            min_repetition = key_i
            min_suma = suma
    return min_repetition


def extract_multiplier_map2(in_map: dict) -> tuple[int, int]:
    min_suma = math.inf
    map_items = list(in_map.items())
    for val_i in map_items[:-1]:
        for val_j in map_items[1:]:
            suma = 0
            for val_k in map_items:
                suma += val_k[1] * calculate_multiplier2(val_k[0], val_i[0], val_j[0])
            if suma < min_suma:
                min_repetition_1 = val_i[0]
                min_repetition_2 = val_j[0]
                min_suma = suma
    return min_repetition_1, min_repetition_2


def simplify_calculated_front_sequence_movements(
    _chaincode: list[int],
) -> tuple[list[int], int, int]:
    repetition_counter_map: dict = {}
    i = 0
    while i < len(_chaincode) - 1:
        if _chaincode[i] == 0:
            counter = 1
            j = i + 1
            while j < len(_chaincode):
                if _chaincode[j] == 0:
                    counter += 1
                    if j == len(_chaincode) - 1:
                        i = j - 1
                else:
                    i = j - 1
                    break
                j = j + 1
            if counter > 1:
                if repetition_counter_map.get(counter) is None:
                    repetition_counter_map[counter] = 1
                else:
                    repetition_counter_map[counter] += 1
        i += 1

    if len(repetition_counter_map) <= 0:
        _low = -1
        _high = -1

    elif len(repetition_counter_map) == 1:
        for key in repetition_counter_map:
            _low = key
        _high = -1
        _chaincode = simplify_all_front_sequence_movements(_chaincode, _low, _high, 6, 7)
    elif len(repetition_counter_map) == 2:
        count = 0
        for key in repetition_counter_map:
            if count == 0:
                _low = key
            else:
                _high = key
            count += 1
        _chaincode = simplify_all_front_sequence_movements(_chaincode, _low, _high, 6, 7)
    else:
        _low, _high = extract_multiplier_map2(repetition_counter_map)
        _chaincode = simplify_all_front_sequence_movements(_chaincode, _low, _high, 6, 7)

    return _chaincode, _low, _high


def get_vec_from_encoded_srf6(x: int, y: int, rest: int, encoded_poly: str) -> list[int]:
    decoded = chaincode_base64_decoder(encoded_poly, 3, rest)
    vec = extract_srf6dcc2points(decoded, x, y)
    return vec


def get_vec_from_encoded_rs6(
    x: int, y: int, low: int, high: int, rest: int, encoded_poly: str
) -> list[int]:
    decoded = chaincode_base64_decoder(encoded_poly, 3, rest)
    vec = extract_rs6fcc2points(decoded, x, y, low, high)
    return vec
