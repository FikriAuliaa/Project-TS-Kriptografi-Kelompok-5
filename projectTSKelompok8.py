# Mini AES Constants
S_BOX = [
    [0x3, 0x4, 0x2, 0x1], 
    [0x0, 0x3, 0x4, 0x2], 
    [0x1, 0x0, 0x3, 0x4], 
    [0x2, 0x1, 0x0, 0x3]
]

# Functions for AES operations
def subnibbles(state):
    """Substitute bytes using the 4-bit S-Box"""
    for i in range(4):
        for j in range(4):
            # Ensure the value is within the range of the S-Box (0x0 - 0xF)
            if state[i][j] < 0 or state[i][j] > 15:
                raise ValueError(f"Invalid state value {state[i][j]} for SubNibbles.")
            state[i][j] = S_BOX[state[i][j] // 4][state[i][j] % 4]
    return state

def shiftrows(state):
    """Shift rows of the state matrix"""
    return [state[0], [state[1][1], state[1][2], state[1][3], state[1][0]],
            [state[2][2], state[2][3], state[2][0], state[2][1]], 
            [state[3][3], state[3][0], state[3][1], state[3][2]]]

def mixcolumns(state):
    """Mix columns using a simplified operation in GF(2^4)"""
    matrix = [[0x2, 0x3, 0x1, 0x1], [0x1, 0x2, 0x3, 0x1], [0x1, 0x1, 0x2, 0x3], [0x3, 0x1, 0x1, 0x2]]
    result = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = sum(matrix[i][k] * state[k][j] for k in range(4)) % 0x10
    return result

def addroundkey(state, key):
    """XOR each byte of state with the corresponding byte of the key"""
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key[i][j]  # XOR with key
    return state

def key_expansion(key):
    """Expand the 16-bit key into a 4x4 matrix of round keys"""
    round_keys = [
        [((key >> 12) & 0xF), ((key >> 8) & 0xF), ((key >> 4) & 0xF), (key & 0xF)],
        [((key >> 20) & 0xF), ((key >> 16) & 0xF), ((key >> 12) & 0xF), ((key >> 8) & 0xF)],
        [((key >> 28) & 0xF), ((key >> 24) & 0xF), ((key >> 20) & 0xF), ((key >> 16) & 0xF)],
        [((key >> 4) & 0xF), ((key >> 0) & 0xF), ((key >> 28) & 0xF), ((key >> 24) & 0xF)]
    ]
    return round_keys

# Function to convert plaintext string to a 4x4 state matrix
def text_to_state(text):
    """Convert plaintext text into a 4x4 state matrix"""
    # Convert text to bytes (UTF-8)
    text_bytes = text.encode('utf-8')
    # Make sure to pad or truncate to 16 bytes (for 16-bit block size)
    text_bytes = text_bytes[:16] + b'\x00' * (16 - len(text_bytes))  # pad if less than 16 bytes

    # Convert bytes into 4x4 state matrix
    state = []
    for i in range(4):
        row = []
        for j in range(4):
            byte = text_bytes[i * 4 + j]
            # Split byte into two nibbles (4-bit values)
            high_nibble = byte >> 4
            low_nibble = byte & 0xF
            row.append(high_nibble)
            row.append(low_nibble)
        state.append(row)
    return state

# Main encryption function
def encrypt(plaintext, key):
    """Encrypt the given plaintext with the given key"""
    state = text_to_state(plaintext)  # Convert text to 4x4 matrix
    
    key_matrix = key_expansion(key)
    
    state = addroundkey(state, key_matrix)

    for round in range(3):  # Simplified to 3 rounds
        state = subnibbles(state)
        state = shiftrows(state)
        state = mixcolumns(state)
        state = addroundkey(state, key_matrix)

    ciphertext = 0
    for i in range(4):
        for j in range(4):
            ciphertext |= state[i][j] << (8 * (3-i))
    return ciphertext

# Main function to handle terminal input
def main():
    # Input plaintext and key from the terminal
    plaintext = input("Enter plaintext (text): ").strip()
    key = input("Enter key (16-bit Hex): ").strip()

    try:
        if not plaintext or not key:
            raise ValueError("Plaintext and Key cannot be empty.")
        
        if len(key) != 4 or not all(c in '0123456789ABCDEF' for c in key.upper()):
            raise ValueError("Key must be a valid 16-bit hexadecimal value.")

        # Convert Hex Key to Integer
        key = int(key, 16)

        # Encrypt the plaintext (which is a string)
        ciphertext = encrypt(plaintext, key)
        print(f"Ciphertext: {hex(ciphertext)}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
