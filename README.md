# Project-TS-Kriptografi-Kelompok-5
# Anggota Kelompok
| Nama  | NRP  |
|----------|----------|
| Fikri Aulia As S.  | 5027231026 |
| Rama Owarianto P.  | 5027231049 |
| M. Andrean Rizq P  | 5027231052 |
| M. Kenas Galeno P.  | 5027231069 |

# Mini-AES 16-bit Encryption

Mini-AES adalah versi sederhana dari algoritma Advanced Encryption Standard (AES) yang dirancang untuk keperluan pembelajaran. Proyek ini mengimplementasikan Mini-AES 16-bit dengan GUI berbasis web menggunakan Streamlit.

## 🔐 Spesifikasi Algoritma Mini-AES
- Ukuran blok: 16-bit (4 nibbles)
- Ukuran kunci: 16-bit
- Jumlah ronde: 3
- Operasi per ronde:
  - SubNibbles: substitusi menggunakan S-Box 4-bit
  - ShiftRows: rotasi baris
  - MixColumns: perkalian di GF(2^4)
  - AddRoundKey: XOR dengan kunci ronde

## 🔁 Key Expansion
- Menghasilkan 3 round key dari 1 kunci utama
- Sederhana menggunakan rotasi, S-Box, dan RCON

## 🧪 Test Case

| No | Plaintext | Key     | Ciphertext (Output) |
|----|-----------|---------|---------------------|
| 1  | 0x1234    | 0x5678  | 0x90DE  |
| 2  | 0x0000    | 0xFFFF  | 0x2ED1  |
| 3  | 0xAAAA    | 0x5555  | 0x0055  |

## 📈 Flowchart

### Mini-AES Algorithm

Plaintext (16-bit)
       ↓
[ AddRoundKey (Round 0) ]
       ↓
[ SubNibbles ]
       ↓
[ ShiftRows ]
       ↓
[ MixColumns ]
       ↓
[ AddRoundKey (Round 1) ]
       ↓
[ SubNibbles ]
       ↓
[ ShiftRows ]
       ↓
[ AddRoundKey (Round 2) ]
       ↓
→ Ciphertext


### Key Expansion

Key (16-bit)
       ↓
[ S-Box Substitution ]
       ↓
[ XOR with RCON ]
       ↓
[ Generate W0 – W11 ]
       ↓
→ RoundKey 0, RoundKey 1, RoundKey 2



## ✅ Kelebihan & Keterbatasan Mini-AES

**Kelebihan:**
- Sederhana untuk dipelajari
- Struktur mirip AES asli
- Cocok untuk simulasi dan pembelajaran

**Keterbatasan:**
- Tidak aman secara kriptografi
- Terbatas hanya 16-bit
- Tidak cocok untuk data nyata

---

## 📦 Cara Menjalankan

1. Install dependensi:
```bash
pip install streamlit
streamlit run streamlit_app.py
```
