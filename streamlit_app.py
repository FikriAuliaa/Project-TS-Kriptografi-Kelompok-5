import streamlit as st
from projectTSKelompok8 import encrypt

def avalanche_test(plaintext, key):
    results = []
    for bit_index in range(16):  # plaintext 16-bit
        new_pt = plaintext ^ (1 << bit_index)  # Membalikkan satu bit
        new_ct, _ = encrypt(new_pt, key)  # Enkripsi dengan plaintext yang sudah dibalik bit-nya
        original_ct, _ = encrypt(plaintext, key)  # Enkripsi dengan plaintext asli
        # Menghitung jumlah bit yang berubah antara ciphertext asli dan baru
        changed_bits = bin(original_ct ^ new_ct).count('1')
        results.append((bit_index, new_pt, new_ct, changed_bits))
    return results

# Streamlit UI
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

# Run test cases
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

st.markdown("---")
st.header("🔓 Decrypt Ciphertext")

ciphertext_hex = st.text_input("Enter 16-bit Ciphertext to Decrypt (hex)", value="0x90DE")

if st.button("Decrypt"):
    try:
        ciphertext = int(ciphertext_hex, 16)
        plaintext, steps = decrypt(ciphertext, key)
        st.success(f"Recovered Plaintext: 0x{plaintext:04X}")
        st.markdown("### Decryption Round Steps:")
        for title, state in steps:
            st.write(f"**{title}**: {[f'{x:X}' for x in state]}")
    except Exception as e:
        st.error(f"Error during decryption: {str(e)}")

st.markdown("---")
st.header("🌊 Avalanche Effect Test")

if st.button("Run Avalanche Test"):
    try:
        results = avalanche_test(plaintext, key)
        st.markdown("### Avalanche Results (1-bit difference in Plaintext):")
        for bit_index, new_pt, new_ct, changed_bits in results:
            st.write(
                f"Bit {bit_index:2d} flipped → New PT = 0x{new_pt:04X}, "
                f"CT = 0x{new_ct:04X}, Changed Bits = {changed_bits}"
            )
    except Exception as e:
        st.error(f"Error during avalanche test: {str(e)}")
