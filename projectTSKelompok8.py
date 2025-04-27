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
# Invers S-Box (sudah ada di awal file jika pakai S_BOX.index)
def inverse_sub_nibbles(state):
    return [INV_S_BOX[nibble] for nibble in state]

def inverse_shift_rows(state):
    # ShiftRows normal: [0, 3, 2, 1] → inverse adalah: [0, 3, 2, 1] juga (karena cuma 2 baris)
    return [state[0], state[3], state[2], state[1]]

def inverse_mix_columns(state):
    return [
        gf_mult(9, state[0]) ^ gf_mult(2, state[1]),
        gf_mult(2, state[0]) ^ gf_mult(9, state[1]),
        gf_mult(9, state[2]) ^ gf_mult(2, state[3]),
        gf_mult(2, state[2]) ^ gf_mult(9, state[3]),
    ]

def decrypt(ciphertext, key):
    state = int_to_state(ciphertext)
    round_keys = key_expansion(key)

    output_steps = []
    output_steps.append(("Initial Ciphertext", state.copy()))

    # Round 2
    state = add_round_key(state, round_keys[2])
    output_steps.append(("After AddRoundKey (Round 2)", state.copy()))
    state = inverse_shift_rows(state)
    output_steps.append(("After Inverse ShiftRows (Round 2)", state.copy()))
    state = inverse_sub_nibbles(state)
    output_steps.append(("After Inverse SubNibbles (Round 2)", state.copy()))

    # Round 1
    state = add_round_key(state, round_keys[1])
    output_steps.append(("After AddRoundKey (Round 1)", state.copy()))
    state = inverse_mix_columns(state)
    output_steps.append(("After Inverse MixColumns (Round 1)", state.copy()))
    state = inverse_shift_rows(state)
    output_steps.append(("After Inverse ShiftRows (Round 1)", state.copy()))
    state = inverse_sub_nibbles(state)
    output_steps.append(("After Inverse SubNibbles (Round 1)", state.copy()))

    # Round 0
    state = add_round_key(state, round_keys[0])
    output_steps.append(("After AddRoundKey (Round 0)", state.copy()))

    return state_to_int(state), output_steps

def avalanche_test(plaintext, key):
    base_ciphertext, _ = encrypt(plaintext, key)
    results = []

    for i in range(16):  # 16-bit plaintext
        modified_plaintext = plaintext ^ (1 << i)
        new_ciphertext, _ = encrypt(modified_plaintext, key)
        diff = base_ciphertext ^ new_ciphertext
        changed_bits = bin(diff).count("1")
        results.append((i, modified_plaintext, new_ciphertext, changed_bits))

    return results

def encrypt_ecb(plaintext_blocks, key):
    """Encrypt multiple blocks using ECB mode."""
    ciphertext_blocks = []
    all_steps = []
    for block in plaintext_blocks:
        cipher_block, steps = encrypt(block, key)
        ciphertext_blocks.append(cipher_block)
        all_steps.append(steps)
    return ciphertext_blocks, all_steps

def decrypt_ecb(ciphertext_blocks, key):
    """Decrypt multiple blocks using ECB mode."""
    plaintext_blocks = []
    all_steps = []
    for block in ciphertext_blocks:
        plain_block, steps = decrypt(block, key)
        plaintext_blocks.append(plain_block)
        all_steps.append(steps)
    return plaintext_blocks, all_steps

def encrypt_cbc(plaintext_blocks, key, iv):
    """Encrypt multiple blocks using CBC mode."""
    ciphertext_blocks = []
    all_steps = []
    previous = iv
    for block in plaintext_blocks:
        block ^= previous  # XOR dengan previous ciphertext (atau IV untuk blok pertama)
        cipher_block, steps = encrypt(block, key)
        ciphertext_blocks.append(cipher_block)
        all_steps.append(steps)
        previous = cipher_block
    return ciphertext_blocks, all_steps

def decrypt_cbc(ciphertext_blocks, key, iv):
    """Decrypt multiple blocks using CBC mode."""
    plaintext_blocks = []
    all_steps = []
    previous = iv
    for block in ciphertext_blocks:
        plain_block, steps = decrypt(block, key)
        plain_block ^= previous  # XOR hasil dekripsi dengan previous ciphertext (atau IV)
        plaintext_blocks.append(plain_block)
        all_steps.append(steps)
        previous = block
    return plaintext_blocks, all_steps

def split_blocks(data, block_size=16):
    """Split integer data into blocks of block_size bits."""
    blocks = []
    while data:
        blocks.insert(0, data & (2**block_size - 1))
        data >>= block_size
    return blocks

def merge_blocks(blocks, block_size=16):
    """Merge blocks back into a single integer."""
    data = 0
    for block in blocks:
        data = (data << block_size) | block
    return data

def export_to_file(filename, plaintext, ciphertext, mode, steps_log=None):
    """Save plaintext, ciphertext, mode, and log steps into a file."""
    with open(filename, 'w') as f:
        f.write(f"Mode: {mode}\n")
        f.write(f"Plaintext: 0x{plaintext:X}\n")
        f.write(f"Ciphertext: 0x{ciphertext:X}\n")
        if steps_log:
            f.write("\nSteps Log:\n")
            for block_idx, steps in enumerate(steps_log):
                f.write(f"Block {block_idx}:\n")
                for title, state in steps:
                    f.write(f"{title}: {[hex(x) for x in state]}\n")

def import_from_file(filename):
    """Load plaintext and ciphertext from a file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    plaintext = None
    ciphertext = None
    for line in lines:
        if line.startswith("Plaintext:"):
            plaintext = int(line.split(":")[1].strip(), 16)
        elif line.startswith("Ciphertext:"):
            ciphertext = int(line.split(":")[1].strip(), 16)
    return plaintext, ciphertext
