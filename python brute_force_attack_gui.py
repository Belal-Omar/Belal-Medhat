import itertools
import string
import tkinter as tk
from tkinter import scrolledtext, messagebox
import random

running = False 

def atbash_cipher_decrypt(ciphertext):
    """ فك تشفير Atbash بشكل صحيح """
    alphabet_upper = string.ascii_uppercase
    alphabet_lower = string.ascii_lowercase
    reversed_upper = alphabet_upper[::-1]
    reversed_lower = alphabet_lower[::-1]
    
    # إنشاء خريطة استبدال الأحرف
    atbash_map = str.maketrans(alphabet_upper + alphabet_lower, reversed_upper + reversed_lower)
    
    # استبدال الأحرف مع الاحتفاظ بالمسافات والعلامات الأخرى
    return ciphertext.translate(atbash_map)

def decrypt_with_key(ciphertext, key):
    """ فك تشفير Monoalphabetic باستخدام مفتاح محدد """
    alphabet = string.ascii_uppercase
    key_map = str.maketrans(''.join(key), alphabet)
    return ciphertext.translate(key_map)

def brute_force_monoalphabetic(ciphertext, output_text, max_attempts=50):
    """ تجربة عدة مفاتيح لفك Monoalphabetic """
    global running
    running = True
    alphabet = string.ascii_uppercase
    
    decrypted_texts = []
    
    for _ in range(max_attempts):
        if not running:
            break
        key = list(alphabet)
        random.shuffle(key)
        plaintext = decrypt_with_key(ciphertext, key)
        decrypted_texts.append(plaintext)
    
    random.shuffle(decrypted_texts)
    
    for i, text in enumerate(decrypted_texts):
        if not running:
            break
        output_text.insert(tk.END, f"المحاولة {i+1}: {text}\n")
        output_text.update_idletasks()  # تحديث النص تدريجيًا
    
    if running:
        output_text.insert(tk.END, "\n✅ انتهت عملية فك التشفير.\n")

def start_decryption():
    """ تشغيل عملية فك التشفير """
    global running
    running = True
    encrypted_message = entry.get().strip()
    
    if not encrypted_message:
        messagebox.showwarning("⚠️ خطأ في الإدخال", "يرجى إدخال نص مشفر.")
        return
    
    output_text.delete(1.0, tk.END)
    
    # فك تشفير Atbash
    atbash_result = atbash_cipher_decrypt(encrypted_message)
    output_text.insert(tk.END, "🔍 فك تشفير Atbash:\n" + atbash_result + "\n\n")
    
    brute_force_monoalphabetic(encrypted_message.upper(), output_text, max_attempts=50)

def stop_decryption():
    """ إيقاف عملية فك التشفير """
    global running
    running = False
    output_text.insert(tk.END, "\n⏹ توقفت عملية فك التشفير.\n")

# GUI
root = tk.Tk()
root.title("🔍 فك تشفير تلقائي (تحليل التكرار + قيصر + Atbash)")
root.geometry("650x450")
root.configure(bg="#f2f2f2")

frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

tk.Label(frame, text="🔐 أدخل النص المشفر:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(pady=5)
entry = tk.Entry(frame, width=50, font=("Arial", 12))
entry.pack(pady=5)

button_frame = tk.Frame(root, bg="#f2f2f2")
button_frame.pack(pady=10)

decrypt_button = tk.Button(button_frame, text="🔓 فك التشفير", font=("Arial", 11), command=start_decryption, bg="#4CAF50", fg="white", width=15)
decrypt_button.pack(side=tk.LEFT, padx=10)

stop_button = tk.Button(button_frame, text="⏹ إيقاف", font=("Arial", 11), command=stop_decryption, bg="#e67e22", fg="white", width=15)
stop_button.pack(side=tk.LEFT, padx=10)

def clear_output():
    """ مسح النتائج """
    output_text.delete(1.0, tk.END)
clear_button = tk.Button(button_frame, text="🗑 مسح النتائج", font=("Arial", 11), command=clear_output, bg="#f39c12", fg="white", width=15)
clear_button.pack(side=tk.LEFT, padx=10)

def exit_program():
    """ إنهاء البرنامج """
    root.quit()
exit_button = tk.Button(button_frame, text="🚪 خروج", font=("Arial", 11), command=exit_program, bg="#e74c3c", fg="white", width=15)
exit_button.pack(side=tk.LEFT, padx=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, font=("Arial", 12))
output_text.pack(pady=10)

root.mainloop()


# Try (GSRH RH Z HVXIVG ) 😉
