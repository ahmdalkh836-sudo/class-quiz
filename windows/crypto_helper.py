# -*- coding: utf-8 -*-
"""
Classroom Quiz Server - Cryptographic Data Sync Module (AES-256-CBC)
Fully interoperable with the Android App (StudentCryptoManager) and Windows 11
"""

import base64
import hashlib
import json
import os

DEFAULT_KEY = "ClassroomQuiz#2026!SecureKey"
PREFIX = "CRS_ENC_V1:"

# Rijndael S-Box and Inverted S-Box
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

INV_S_BOX = [0] * 256
for idx, v in enumerate(S_BOX):
    INV_S_BOX[v] = idx

RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

def _sub_word(w):
    return ((S_BOX[(w >> 24) & 0xff] << 24) |
            (S_BOX[(w >> 16) & 0xff] << 16) |
            (S_BOX[(w >> 8) & 0xff] << 8) |
            (S_BOX[w & 0xff]))

def _rot_word(w):
    return (((w << 8) & 0xffffffff) | (w >> 24))

def _key_expansion(key_bytes):
    w = [0] * 60
    for i in range(8):
        w[i] = (key_bytes[4*i] << 24) | (key_bytes[4*i + 1] << 16) | (key_bytes[4*i + 2] << 8) | key_bytes[4*i + 3]
    for i in range(8, 60):
        temp = w[i - 1]
        if i % 8 == 0:
            temp = _sub_word(_rot_word(temp)) ^ (RCON[i // 8] << 24)
        elif i % 8 == 4:
            temp = _sub_word(temp)
        w[i] = w[i - 8] ^ temp
    return w

def _xtime(a):
    return (((a << 1) ^ 0x1b) & 0xff) if (a & 0x80) else (a << 1)

def _mul(a, b):
    res = 0
    for _ in range(8):
        if b & 1: res ^= a
        hi = a & 0x80
        a = (a << 1) & 0xff
        if hi: a ^= 0x1b
        b >>= 1
    return res

def _cipher_block(block, w):
    state = [[block[r + 4*c] for c in range(4)] for r in range(4)]
    for c in range(4):
        k = w[c]
        state[0][c] ^= (k >> 24) & 0xff
        state[1][c] ^= (k >> 16) & 0xff
        state[2][c] ^= (k >> 8) & 0xff
        state[3][c] ^= k & 0xff

    for rnd in range(1, 14):
        for r in range(4):
            for c in range(4):
                state[r][c] = S_BOX[state[r][c]]
        state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
        state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
        for c in range(4):
            s0 = state[0][c]; s1 = state[1][c]; s2 = state[2][c]; s3 = state[3][c]
            state[0][c] = _xtime(s0 ^ s1) ^ s1 ^ s2 ^ s3
            state[1][c] = _xtime(s1 ^ s2) ^ s2 ^ s3 ^ s0
            state[2][c] = _xtime(s2 ^ s3) ^ s3 ^ s0 ^ s1
            state[3][c] = _xtime(s3 ^ s0) ^ s0 ^ s1 ^ s2
        for c in range(4):
            k = w[rnd * 4 + c]
            state[0][c] ^= (k >> 24) & 0xff
            state[1][c] ^= (k >> 16) & 0xff
            state[2][c] ^= (k >> 8) & 0xff
            state[3][c] ^= k & 0xff

    for r in range(4):
        for c in range(4):
            state[r][c] = S_BOX[state[r][c]]
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]
    for c in range(4):
        k = w[14 * 4 + c]
        state[0][c] ^= (k >> 24) & 0xff
        state[1][c] ^= (k >> 16) & 0xff
        state[2][c] ^= (k >> 8) & 0xff
        state[3][c] ^= k & 0xff

    out = bytearray(16)
    for r in range(4):
        for c in range(4):
            out[r + 4*c] = state[r][c]
    return bytes(out)

def _inv_cipher_block(block, w):
    state = [[block[r + 4*c] for c in range(4)] for r in range(4)]
    for c in range(4):
        k = w[14 * 4 + c]
        state[0][c] ^= (k >> 24) & 0xff
        state[1][c] ^= (k >> 16) & 0xff
        state[2][c] ^= (k >> 8) & 0xff
        state[3][c] ^= k & 0xff

    for rnd in range(13, 0, -1):
        state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
        state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
        state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]
        for r in range(4):
            for c in range(4):
                state[r][c] = INV_S_BOX[state[r][c]]
        for c in range(4):
            k = w[rnd * 4 + c]
            state[0][c] ^= (k >> 24) & 0xff
            state[1][c] ^= (k >> 16) & 0xff
            state[2][c] ^= (k >> 8) & 0xff
            state[3][c] ^= k & 0xff
        for c in range(4):
            s0 = state[0][c]; s1 = state[1][c]; s2 = state[2][c]; s3 = state[3][c]
            state[0][c] = _mul(0x0e, s0) ^ _mul(0x0b, s1) ^ _mul(0x0d, s2) ^ _mul(0x09, s3)
            state[1][c] = _mul(0x09, s0) ^ _mul(0x0e, s1) ^ _mul(0x0b, s2) ^ _mul(0x0d, s3)
            state[2][c] = _mul(0x0d, s0) ^ _mul(0x09, s1) ^ _mul(0x0e, s2) ^ _mul(0x0b, s3)
            state[3][c] = _mul(0x0b, s0) ^ _mul(0x0d, s1) ^ _mul(0x09, s2) ^ _mul(0x0e, s3)

    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][3], state[1][0], state[1][1], state[1][2]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][1], state[3][2], state[3][3], state[3][0]
    for r in range(4):
        for c in range(4):
            state[r][c] = INV_S_BOX[state[r][c]]
    for c in range(4):
        k = w[c]
        state[0][c] ^= (k >> 24) & 0xff
        state[1][c] ^= (k >> 16) & 0xff
        state[2][c] ^= (k >> 8) & 0xff
        state[3][c] ^= k & 0xff

    out = bytearray(16)
    for r in range(4):
        for c in range(4):
            out[r + 4*c] = state[r][c]
    return bytes(out)

def encrypt_students_aes(students_list, password=DEFAULT_KEY):
    key = hashlib.sha256((password.strip() or DEFAULT_KEY).encode('utf-8')).digest()
    iv = os.urandom(16)
    raw = json.dumps(students_list, ensure_ascii=False).encode('utf-8')

    # PKCS7 padding
    pad_len = 16 - (len(raw) % 16)
    padded = raw + bytes([pad_len] * pad_len)

    w = _key_expansion(key)
    res = bytearray()
    prev = iv
    for i in range(0, len(padded), 16):
        block = bytes(a ^ b for a, b in zip(padded[i:i+16], prev))
        enc = _cipher_block(block, w)
        res.extend(enc)
        prev = enc

    combined = iv + bytes(res)
    return PREFIX + base64.b64encode(combined).decode('ascii')

def decrypt_students_aes(cipher_str, password=DEFAULT_KEY):
    raw_str = cipher_str.strip()
    if PREFIX in raw_str:
        raw_str = raw_str.split(PREFIX)[1].strip()

    combined = base64.b64decode(raw_str)
    if len(combined) < 32:
        raise ValueError("الكود المشفر غير صالح أو تالف")

    iv = combined[:16]
    ciphertext = combined[16:]
    key = hashlib.sha256((password.strip() or DEFAULT_KEY).encode('utf-8')).digest()
    w = _key_expansion(key)

    res = bytearray()
    prev = iv
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        dec = _inv_cipher_block(block, w)
        plain = bytes(a ^ b for a, b in zip(dec, prev))
        res.extend(plain)
        prev = block

    pad_len = res[-1]
    if pad_len < 1 or pad_len > 16:
        raise ValueError("فشل فك التشفير: كلمة المرور غير صحيحة")
    unpadded = res[:-pad_len]
    return json.loads(unpadded.decode('utf-8'))
