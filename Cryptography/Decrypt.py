from cryptography.fernet import Fernet

enc_key = "xTiiUmaNwb3i8kr1YYhhUqYrp-gMgTmXp_PfsnZcyOM="

system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard.txt"
keys_information_e = "e_Key_adv_log.txt"

enc_files = [system_information_e, clipboard_information_e, keys_information_e]
count = 0

for decrypt_file in enc_files:
    with open(decrypt_file, 'rb') as f:
        data = f.read()
    
    fernet = Fernet(enc_key)
    decrypted = fernet.decrypt(data)

    with open(enc_files[count], 'wb') as f:
        f.write(decrypted)

    count += 1