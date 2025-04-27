from projectTSKelompok8 import (
    encrypt, decrypt, avalanche_test,
    encrypt_ecb, decrypt_ecb, encrypt_cbc, decrypt_cbc,
    split_blocks, merge_blocks,
    export_to_file, import_from_file
)

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

# --------- ECB Mode ---------
print("\n--- ECB Mode ---")
blocks = split_blocks(pt)
ct_blocks_ecb, steps_ecb = encrypt_ecb(blocks, key)
merged_ct_ecb = merge_blocks(ct_blocks_ecb)
print(f"[Encrypt ECB] Ciphertext: 0x{merged_ct_ecb:X}")

pt_blocks_ecb, _ = decrypt_ecb(ct_blocks_ecb, key)
merged_pt_ecb = merge_blocks(pt_blocks_ecb)
print(f"[Decrypt ECB] Plaintext: 0x{merged_pt_ecb:X}")

# --------- CBC Mode ---------
print("\n--- CBC Mode ---")
blocks = split_blocks(pt)
ct_blocks_cbc, steps_cbc = encrypt_cbc(blocks, key, iv)
merged_ct_cbc = merge_blocks(ct_blocks_cbc)
print(f"[Encrypt CBC] Ciphertext: 0x{merged_ct_cbc:X}")

pt_blocks_cbc, _ = decrypt_cbc(ct_blocks_cbc, key, iv)
merged_pt_cbc = merge_blocks(pt_blocks_cbc)
print(f"[Decrypt CBC] Plaintext: 0x{merged_pt_cbc:X}")

# --------- Export to File ---------
export_to_file("output_ecb.txt", pt, merged_ct_ecb, mode="ECB", steps_log=steps_ecb)
export_to_file("output_cbc.txt", pt, merged_ct_cbc, mode="CBC", steps_log=steps_cbc)

# --------- Import from File ---------
plaintext_from_file, ciphertext_from_file = import_from_file("output_ecb.txt")
print(f"\n[Import from file] Plaintext: 0x{plaintext_from_file:X}, Ciphertext: 0x{ciphertext_from_file:X}")
