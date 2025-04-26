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
