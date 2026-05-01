import json
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad

# --- CONFIGURATION AREA ---
# Add your servers here. You can add as many as you want.
SERVERS = [
    {
        "serverType": 2, # 2 = SSH
        "Name": "Premium SSH Server",
        "Flag": "in", # us, br, de, etc (matches flags in assets)
        "Info": "SSH WebSocket",
        "ServerIP": "omnitrix.space",
        "ServerPort": "443",
        "SSLPort": "443",
        "SSHUser": "Voldemort",
        "SSHPass": "Voldemort7273",
        "ProxyIP": "nriebiz.licindia.in", # Optional: Bug IP / Cloudflare IP
        "ProxyPort": "80",
        "Payload": "GET / HTTP/1.1[crlf]Host: [host][crlf]Service: SSH[crlf]ModeX: Bypass[crlf]Upgrade: websocket[crlf][crlf]"
    }
]

VERSION = "1.0"
RELEASE_NOTES = "New high-speed servers added!"
# --------------------------

# Security constants (Do not change)
PASSWORD = "Ahpaim"
JA_TEST_B64 = "4paZ4paa4pab4pac4pad4pae4paf4paD4paE4paF4paG4paH4paI4paJ4paK4paQ"
JA_TEST = base64.b64decode(JA_TEST_B64).decode('utf-8')

def Jacodes(s):
    char_array = list(JA_TEST)
    sb = ""
    for b in s.encode('utf-8'):
        sb += char_array[(b & 240) >> 4]
        sb += char_array[b & 15]
    return sb

def encrypt(password, plaintext):
    key_hex = password.encode('utf-8').hex().upper()
    hasher = SHA256.new()
    hasher.update(key_hex.encode('utf-8'))
    key = hasher.digest()
    iv = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    b64_str = base64.b64encode(encrypted).decode('utf-8')
    return Jacodes(b64_str)

# Generate JSON
config_obj = {
    "Version": VERSION,
    "ReleaseNotes": RELEASE_NOTES,
    "Servers": SERVERS
}

json_str = json.dumps(config_obj, separators=(',', ':'))
encrypted_str = encrypt(PASSWORD, json_str)

# Save to file
with open('Config.json', 'w') as f:
    f.write(encrypted_str)

print(f"SUCCESS: Config.json version {VERSION} generated!")
print("Now push this file to your 'android-metadata-provider' repository.")
