# streamlit_app.py

import streamlit as st
from projectTSKelompok8 import encrypt

st.title("Mini-AES 16-bit Encryption")
st.markdown("### Encrypt 16-bit plaintext using Mini-AES (3 rounds)")

plaintext_hex = st.text_input("Enter 16-bit Plaintext (hex, e.g. 0x1234)", value="0x1234")
key_hex = st.text_input("Enter 16-bit Key (hex, e.g. 0x5678)", value="0x5678")

if st.button("Encrypt"):
    try:
        plaintext = int(plaintext_hex, 16)
        key = int(key_hex, 16)
        if plaintext >= 0x10000 or key >= 0x10000:
            st.error("Plaintext and Key must be 16-bit (0x0000 to 0xFFFF)")
        else:
            ciphertext, steps = encrypt(plaintext, key)
            st.success(f"Ciphertext: 0x{ciphertext:04X}")
            st.markdown("### 🔄 Round Steps:")
            for title, state in steps:
                st.write(f"**{title}**: {[f'{x:X}' for x in state]}")
    except ValueError:
        st.error("Invalid input format. Use hexadecimal (e.g. 0x1A2B).")

# Tambahkan di bawah tombol Encrypt
if st.button("Run Test Cases"):
    test_cases = [
        ("0x1234", "0x5678"),
        ("0x0000", "0xFFFF"),
        ("0xAAAA", "0x5555")
    ]
    st.markdown("### 🧪 Test Case Results")
    for pt_hex, key_hex in test_cases:
        pt = int(pt_hex, 16)
        key = int(key_hex, 16)
        ct, steps = encrypt(pt, key)
        st.write(f"**Plaintext: {pt_hex}, Key: {key_hex} → Ciphertext: 0x{ct:04X}**")

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
