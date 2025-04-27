# streamlit_app.py

import streamlit as st
from projectTSKelompok8 import (
    encrypt, encrypt_ecb, encrypt_cbc,
    split_blocks, merge_blocks,
    export_to_file, import_from_file
)

st.title("Mini-AES 16-bit Encryption")
st.markdown("### Encrypt 16-bit plaintext using Mini-AES (3 rounds)")

plaintext_hex = st.text_input("Enter 16-bit Plaintext (hex, e.g. 0x1234)", value="0x1234")
key_hex = st.text_input("Enter 16-bit Key (hex, e.g. 0x5678)", value="0x5678")
mode = st.selectbox("Select Mode", ["Single Block (Normal)", "ECB Mode", "CBC Mode"])

if mode == "CBC Mode":
    iv_hex = st.text_input("Enter IV (Hex, e.g. 0x1A2B)", value="0x1A2B")
else:
    iv_hex = None
    
if st.button("Encrypt"):
    try:
        plaintext = int(plaintext_hex, 16)
        key = int(key_hex, 16)
        if plaintext >= (1 << 64) or key >= 0x10000:
            st.error("Plaintext max 64-bit (0xFFFFFFFFFFFFFFFF), Key must be 16-bit (0x0000 to 0xFFFF)")
        else:
            if mode == "Single Block (Normal)":
                ciphertext, steps = encrypt(plaintext, key)
                st.success(f"Ciphertext: 0x{ciphertext:04X}")
                st.markdown("### Round Steps:")
                for title, state in steps:
                    st.write(f"**{title}**: {[f'{x:X}' for x in state]}")
            else:
                blocks = split_blocks(plaintext)
                if mode == "ECB Mode":
                    ct_blocks, steps = encrypt_ecb(blocks, key)
                elif mode == "CBC Mode":
                    iv = int(iv_hex, 16)
                    ct_blocks, steps = encrypt_cbc(blocks, key, iv)
                ciphertext = merge_blocks(ct_blocks)
                st.success(f"Ciphertext: 0x{ciphertext:X}")
                st.markdown("### Round Steps (per Block):")
                for idx, block_steps in enumerate(steps):
                    st.write(f"#### Block {idx}")
                    for title, state in block_steps:
                        st.write(f"**{title}**: {[f'{x:X}' for x in state]}")

            # Save to file
            export_to_file("output_result.txt", plaintext, ciphertext, mode=mode, steps_log=steps)
            st.download_button("Download Result", data=open("output_result.txt", "rb"), file_name="output_result.txt", mime="text/plain")
    except ValueError:
        st.error("Invalid input format. Use hexadecimal (e.g. 0x1A2B).")

st.markdown("---")
st.header("Upload Input File (.txt)")
uploaded_file = st.file_uploader("Choose a file", type=["txt"])
if uploaded_file is not None:
    with open("uploaded_input.txt", "wb") as f:
        f.write(uploaded_file.getbuffer())
    plaintext, _ = import_from_file("uploaded_input.txt")
    st.success(f"Loaded Plaintext from file: 0x{plaintext:X}")

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
