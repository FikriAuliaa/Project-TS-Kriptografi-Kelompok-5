from projectTSKelompok8 import encrypt, decrypt, avalanche_test

pt = 0x1234
key = 0x5678

# Enkripsi
ct, steps_enc = encrypt(pt, key)
print(f"[Encrypt] Ciphertext: 0x{ct:04X}")

# Menampilkan langkah-langkah proses enkripsi
for step_desc, state in steps_enc:
    print(f"{step_desc}: {state}")

# Dekripsi
pt_recovered, steps_dec = decrypt(ct, key)
print(f"[Decrypt] Recovered Plaintext: 0x{pt_recovered:04X}")

# Menampilkan langkah-langkah proses dekripsi
for step_desc, state in steps_dec:
    print(f"{step_desc}: {state}")

# Avalanche Effect
print("\n[ Avalanche Test - Flip 1 bit in plaintext ]")
results = avalanche_test(pt, key)
for bit_index, new_pt, new_ct, changed_bits in results:
    print(f"Bit {bit_index:2d} flipped -> New PT = 0x{new_pt:04X}, CT = 0x{new_ct:04X}, Changed Bits: {changed_bits}")
