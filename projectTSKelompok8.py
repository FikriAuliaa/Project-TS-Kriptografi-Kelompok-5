# mini_aes.py

# S-Box 4-bit
S_BOX = [0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5, 0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7]

# Invers S-Box jika perlu (opsional)
INV_S_BOX = [S_BOX.index(i) for i in range(16)]

# Galois Field Multiplication for GF(2^4)
def gf_mult(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0b10011
        b >>= 1
    return p & 0xF

def sub_nibbles(state):
    return [S_BOX[nibble] for nibble in state]

def shift_rows(state):
    return [state[0], state[3], state[2], state[1]]

def mix_columns(state):
    return [
        gf_mult(1, state[0]) ^ gf_mult(4, state[1]),
        gf_mult(4, state[0]) ^ gf_mult(1, state[1]),
        gf_mult(1, state[2]) ^ gf_mult(4, state[3]),
        gf_mult(4, state[2]) ^ gf_mult(1, state[3]),
    ]

def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

def key_expansion(key):
    w = [(key >> 12) & 0xF, (key >> 8) & 0xF, (key >> 4) & 0xF, key & 0xF]
    rcon1 = 0b1000
    rcon2 = 0b0011

    w.append(S_BOX[w[3]] ^ rcon1 ^ w[0])
    w.append(w[1] ^ w[4])
    w.append(w[2] ^ w[5])
    w.append(w[3] ^ w[6])

    w.append(S_BOX[w[7]] ^ rcon2 ^ w[4])
    w.append(w[5] ^ w[8])
    w.append(w[6] ^ w[9])
    w.append(w[7] ^ w[10])

    return [w[0:4], w[4:8], w[8:12]]  # 3 round keys

def int_to_state(n):
    return [(n >> 12) & 0xF, (n >> 8) & 0xF, (n >> 4) & 0xF, n & 0xF]

def state_to_int(state):
    return (state[0] << 12) | (state[1] << 8) | (state[2] << 4) | state[3]

def encrypt(plaintext, key):
    state = int_to_state(plaintext)
    round_keys = key_expansion(key)

    output_steps = []
    output_steps.append(("Initial State", state.copy()))
    state = add_round_key(state, round_keys[0])
    output_steps.append(("After AddRoundKey (Round 0)", state.copy()))

    for i in range(1, 3):
        state = sub_nibbles(state)
        output_steps.append((f"After SubNibbles (Round {i})", state.copy()))
        state = shift_rows(state)
        output_steps.append((f"After ShiftRows (Round {i})", state.copy()))
        if i != 2:  # no MixColumns in final round
            state = mix_columns(state)
            output_steps.append((f"After MixColumns (Round {i})", state.copy()))
        state = add_round_key(state, round_keys[i])
        output_steps.append((f"After AddRoundKey (Round {i})", state.copy()))

    return state_to_int(state), output_steps
