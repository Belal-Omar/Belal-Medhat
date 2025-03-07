from collections import Counter
import tkinter as tk
from tkinter import messagebox, scrolledtext

ENGLISH_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def frequency_analysis(ciphertext):
    """Perform frequency analysis on the ciphertext."""
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    
    freq = Counter(ciphertext)
    
    sorted_freq = sorted(freq.keys(), key=lambda x: freq[x], reverse=True)
    
    return sorted_freq

def map_letters(cipher_freq, english_freq):
    """Map ciphertext letters to English letters based on frequency."""
    mapping = {}
    for i in range(len(cipher_freq)):
        if i < len(english_freq):
            mapping[cipher_freq[i]] = english_freq[i]
        else:
            mapping[cipher_freq[i]] = '?'  
    return mapping

def decrypt_with_mapping(ciphertext, mapping):
    """Decrypt the ciphertext using the frequency mapping."""
    plaintext = []
    for char in ciphertext:
        if char.upper() in mapping:
            
            if char.islower():
                plaintext.append(mapping[char.upper()].lower())
            else:
                plaintext.append(mapping[char.upper()])
        else:
            plaintext.append(char)  
    return ''.join(plaintext)

def perform_cryptanalysis():
    """Perform cryptanalysis and display results."""
    ciphertext = ciphertext_entry.get("1.0", tk.END).strip()
    
    if not ciphertext:
        messagebox.showwarning("Input Error", "Please enter ciphertext.")
        return
    
    
    cipher_freq = frequency_analysis(ciphertext)
    freq_text.delete(1.0, tk.END)
    freq_text.insert(tk.END, "Frequency of letters in ciphertext (most to least):\n")
    freq_text.insert(tk.END, ", ".join(cipher_freq))
    
    
    mapping = map_letters(cipher_freq, ENGLISH_FREQ)
    mapping_text.delete(1.0, tk.END)
    mapping_text.insert(tk.END, "Suggested letter mapping:\n")
    for cipher_char, plain_char in mapping.items():
        mapping_text.insert(tk.END, f"{cipher_char} -> {plain_char}\n")
    
    
    plaintext = decrypt_with_mapping(ciphertext, mapping)
    plaintext_text.delete(1.0, tk.END)
    plaintext_text.insert(tk.END, "Most likely decrypted text:\n")
    plaintext_text.insert(tk.END, plaintext)

def adjust_mapping():
    """Allow the user to manually adjust the mapping."""
    ciphertext = ciphertext_entry.get("1.0", tk.END).strip()
    if not ciphertext:
        messagebox.showwarning("Input Error", "Please enter ciphertext.")
        return
    
    
    cipher_freq = frequency_analysis(ciphertext)
    mapping = map_letters(cipher_freq, ENGLISH_FREQ)
    
    
    adjust_window = tk.Toplevel(root)
    adjust_window.title("Adjust Letter Mapping")
    
    
    tk.Label(adjust_window, text="Current Mapping:").grid(row=0, column=0, padx=10, pady=10)
    for i, (cipher_char, plain_char) in enumerate(mapping.items()):
        tk.Label(adjust_window, text=f"{cipher_char} -> {plain_char}").grid(row=i+1, column=0, padx=10, pady=5)
        entry = tk.Entry(adjust_window)
        entry.grid(row=i+1, column=1, padx=10, pady=5)
        entry.insert(0, plain_char)
    
    def save_mapping():
        """Save the adjusted mapping and update the decrypted text."""
        for i, cipher_char in enumerate(mapping.keys()):
            new_char = adjust_window.grid_slaves(row=i+1, column=1)[0].get().upper()
            if new_char:
                mapping[cipher_char] = new_char
        
        
        plaintext = decrypt_with_mapping(ciphertext, mapping)
        plaintext_text.delete(1.0, tk.END)
        plaintext_text.insert(tk.END, "Most likely decrypted text:\n")
        plaintext_text.insert(tk.END, plaintext)
        
        adjust_window.destroy()
    
    
    tk.Button(adjust_window, text="Save", command=save_mapping).grid(row=len(mapping)+1, column=0, columnspan=2, padx=10, pady=10)


root = tk.Tk()
root.title("Monoalphabetic Cipher Cryptanalysis")
root.geometry("600x600")


tk.Label(root, text="Enter Ciphertext:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
ciphertext_entry = scrolledtext.ScrolledText(root, width=70, height=5)
ciphertext_entry.grid(row=1, column=0, padx=10, pady=10)

analyze_button = tk.Button(root, text="Analyze", command=perform_cryptanalysis)
analyze_button.grid(row=2, column=0, padx=10, pady=10)

adjust_button = tk.Button(root, text="Adjust Mapping", command=adjust_mapping)
adjust_button.grid(row=3, column=0, padx=10, pady=10)

tk.Label(root, text="Frequency Analysis:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
freq_text = scrolledtext.ScrolledText(root, width=70, height=3)
freq_text.grid(row=5, column=0, padx=10, pady=10)

tk.Label(root, text="Suggested Letter Mapping:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
mapping_text = scrolledtext.ScrolledText(root, width=70, height=5)
mapping_text.grid(row=7, column=0, padx=10, pady=10)

tk.Label(root, text="Decrypted Text:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
plaintext_text = scrolledtext.ScrolledText(root, width=70, height=5)
plaintext_text.grid(row=9, column=0, padx=10, pady=10)


root.mainloop()