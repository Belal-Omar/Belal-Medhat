import re
import tkinter as tk
from tkinter import messagebox, scrolledtext

BG_COLOR = "#F7F9FC" 
TEXT_COLOR = "#2C3E50"  
BTN_COLOR = "#4A90E2" 
BTN_HOVER_COLOR = "#357ABD"  
ENTRY_BG = "#E3EAFD"  
TEXT_BG = "#FFFFFF"  
FONT = ("Arial", 12)

def prepare_key(key):
    key = key.upper().replace("J", "I")
    key = re.sub(r"[^A-Z]", "", key)
    seen = set()
    key_matrix = [char for char in key if not (char in seen or seen.add(char))]
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            key_matrix.append(char)
    return key_matrix

def create_playfair_matrix(key):
    key_matrix = prepare_key(key)
    return [key_matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None, None

def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = re.sub(r"[^A-Z]", "", text)
    text = list(text)
    i = 0
    while i < len(text) - 1:
        if text[i] == text[i + 1]:
            text.insert(i + 1, "X")
        i += 2
    if len(text) % 2 != 0:
        text.append("X")
    return "".join(text)

def encrypt_pair(matrix, pair):
    a, b = pair
    row_a, col_a = find_position(matrix, a)
    row_b, col_b = find_position(matrix, b)
    if row_a == row_b:
        return matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
    elif col_a == col_b:
        return matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
    return matrix[row_a][col_b] + matrix[row_b][col_a]

def decrypt_pair(matrix, pair):
    a, b = pair
    row_a, col_a = find_position(matrix, a)
    row_b, col_b = find_position(matrix, b)
    if row_a == row_b:
        return matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
    elif col_a == col_b:
        return matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
    return matrix[row_a][col_b] + matrix[row_b][col_a]

def encrypt(plaintext, key):
    matrix = create_playfair_matrix(key)
    plaintext = prepare_text(plaintext)
    return "".join(encrypt_pair(matrix, plaintext[i:i+2]) for i in range(0, len(plaintext), 2))

def decrypt(ciphertext, key):
    matrix = create_playfair_matrix(key)
    return "".join(decrypt_pair(matrix, ciphertext[i:i+2]) for i in range(0, len(ciphertext), 2))

def display_matrix(matrix):
    matrix_text.delete(1.0, tk.END)
    matrix_text.insert(tk.END, "\n".join(" ".join(row) for row in matrix))

def on_encrypt():
    key, plaintext = key_entry.get().strip(), plaintext_entry.get("1.0", tk.END).strip()
    if not key or not plaintext:
        messagebox.showwarning("⚠️ Error", "Please enter both the text and the keyword!")
        return
    ciphertext = encrypt(plaintext, key)
    ciphertext_entry.delete(1.0, tk.END)
    ciphertext_entry.insert(tk.END, ciphertext)
    display_matrix(create_playfair_matrix(key))

def on_decrypt():
    key, ciphertext = key_entry.get().strip(), ciphertext_entry.get("1.0", tk.END).strip()
    if not key or not ciphertext:
        messagebox.showwarning("⚠️ Error", "Please enter both the encrypted text and the keyword!")
        return
    plaintext = decrypt(ciphertext, key)
    plaintext_entry.delete(1.0, tk.END)
    plaintext_entry.insert(tk.END, plaintext)
    display_matrix(create_playfair_matrix(key))

#  GUI 
root = tk.Tk()
root.title("🔐 Playfair Cipher - Encryption & Decryption")
root.geometry("700x550")
root.configure(bg=BG_COLOR)

frame_top = tk.Frame(root, bg=BG_COLOR)
frame_top.pack(pady=10)

frame_middle = tk.Frame(root, bg=BG_COLOR)
frame_middle.pack(pady=10)

frame_bottom = tk.Frame(root, bg=BG_COLOR)
frame_bottom.pack(pady=10)

tk.Label(frame_top, text="🔑 Keyword:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
key_entry = tk.Entry(frame_top, width=30, font=FONT, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
key_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_middle, text="✍️ Plaintext:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR).grid(row=0, column=0, padx=10, pady=5)
plaintext_entry = scrolledtext.ScrolledText(frame_middle, width=50, height=5, font=FONT, bg=TEXT_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
plaintext_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_middle, text="🔒 Encrypted Text:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR).grid(row=1, column=0, padx=10, pady=5)
ciphertext_entry = scrolledtext.ScrolledText(frame_middle, width=50, height=5, font=FONT, bg=TEXT_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
ciphertext_entry.grid(row=1, column=1, padx=10, pady=5)

encrypt_button = tk.Button(frame_bottom, text="🔐 Encrypt", font=FONT, bg=BTN_COLOR, fg="white", width=15, command=on_encrypt)
encrypt_button.grid(row=0, column=0, padx=10, pady=5)

decrypt_button = tk.Button(frame_bottom, text="🔓 Decrypt", font=FONT, bg=BTN_COLOR, fg="white", width=15, command=on_decrypt)
decrypt_button.grid(row=0, column=1, padx=10, pady=5)

matrix_text = scrolledtext.ScrolledText(root, width=50, height=5, font=FONT, bg=TEXT_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
matrix_text.pack(pady=10)

root.mainloop()

