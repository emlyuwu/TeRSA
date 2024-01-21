import customtkinter
from Crypto.Util import number
import math
import os

if not os.path.exists("keys"):
    os.makedirs("keys")

encoded = ""

def generate_keys():
    global publick
    global privatek
    global keymod
    blength = 2048
    p = number.getPrime(blength)
    q = number.getPrime(blength)
    keymod = p * q
    phi_n = (p - 1) * (q - 1)
    publick = 65537
    privatek = pow(publick, -1, phi_n)


def write_keys():
    global pubkey
    global privkey
    with open(f'keys/{wkeyname}-public.key', 'w') as file:
        file.write(f"{keymod},{publick}")
        file.close()
    with open(f'keys/{wkeyname}-private.key', 'w') as file:
        file.write(f"{keymod},{privatek}")
        file.close()
    pubkey = (f"{keymod}, {publickey}")
    privkey = (f"{keymod}, {privatekey}")


def keygen_run():
    global wkeyname
    wkeyname = keyname.get()
    if os.path.isfile(f"keys/{wkeyname}-public.key") or os.path.isfile(f"{wkeyname}/-private.key"):
        print("Key with given name already exists.")
        return(1)
    else:
        generate_keys()
        write_keys()
        print("Complete. Written to .key files.")
        publickey.delete(0.0,'end')
        publickey.insert("end", pubkey)
        privatekey.delete(0.0,'end')
        privatekey.insert("end", privkey)

def submit_e():
    global keyname
    global message
    message = to_encode.get()
    keyname = ekeylocation.get()
    encode()


def encode():
    global encoded
    encode_two = int.from_bytes(message.encode('utf-8'), byteorder='big', signed=False)
    with open(f'keys/{keyname}-public.key', "r") as f:
        content = f.read()
        keymod, publick = content.split(",")
    encoded = pow(encode_two, int(publick), int(keymod), )
    Eoutput.delete(index1=0.0, index2='end')
    Eoutput.insert("end", encoded)




def submit_d():
    global keyname
    keyname = keylocation.get()
    decode()


def decode():
    global decoded
    encodedfile = to_decode.get(0.0, 'end')
    if encodedfile.startswith("/"):
        encodedfile = encodedfile.split("/", 1)[1]
        encodedfile = encodedfile.strip()
        print(encodedfile)
        with open(f"{encodedfile}", "r") as f:
            message = f.read()
    else:
        message = encodedfile
    with open(f'keys/{keyname}-private.key', "r") as f:
        content = f.read()
        keymod, privatek = content.split(",")
    decode_two = pow(int(message), int(privatek), int(keymod), )
    decoded = (int(decode_two)).to_bytes(math.ceil((int(decode_two)).bit_length() / 8), byteorder='big',
                                         signed=False).decode('utf-8')
    Doutput.delete(index1=0.0, index2='end')
    Doutput.insert("end", decoded)






customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.title("TeRSA")
app.geometry("830x400")
tabview = customtkinter.CTkTabview(app, width=800, height=400)
tabview.pack(pady=10)
encode_tab = tabview.add('Encode')
decode_tab = tabview.add('Decode')
keygen_tab = tabview.add('Key generation')

to_encode = customtkinter.CTkEntry(encode_tab, placeholder_text="Message to encode?", height=30, width=700)
to_encode.grid(row=0, column=0, sticky="w", padx=5, pady=7)
submit = customtkinter.CTkButton(master=encode_tab, command=submit_e, text="Encode", width=100)
submit.grid(row=0, column=1, padx=5)
ekeylocation = customtkinter.CTkEntry(encode_tab, placeholder_text="Key name? (prefix to -public.key)", height=30,
                                     width=800)
ekeylocation.grid(row=1, column=0, padx=5, pady=7, sticky="ew", columnspan=2)
Eoutput = customtkinter.CTkTextbox(master=encode_tab, width=800, pady=5, height=230)
Eoutput.grid(row=2, column=0, padx=5, pady=7, columnspan=2, sticky='ew')


to_decode = customtkinter.CTkTextbox(master=decode_tab, width=700, pady=5, height=230)
to_decode.grid(row=0, column=0, padx=5, pady=7, sticky='w', columnspan=1)
submit = customtkinter.CTkButton(master=decode_tab, command=submit_d, text="Decode", width=100)
submit.grid(row=0, column=1, pady=7, sticky='nw')
encodeinfo = customtkinter.CTkLabel(master=decode_tab,text="Enter RSA encoded\nmessage or file\nlocation here.", width=100)
encodeinfo.grid(row=0, column=1, pady=7)
keylocation = customtkinter.CTkEntry(decode_tab, placeholder_text="Key name? (prefix to -private.key)", height=30,
                                     width=800)
keylocation.grid(row=1, column=0, pady=7, padx=5, sticky="ew", columnspan=2)
Doutput = customtkinter.CTkTextbox(decode_tab,height=30, width=800)
Doutput.grid(row=2, column=0, sticky="w", padx=5, pady=7, columnspan=2)

genkey = customtkinter.CTkButton(master=keygen_tab, command=keygen_run, text="Generate new keys", width=75, )
genkey.grid(row=1, column=1, pady=7)
publickey = customtkinter.CTkTextbox(master=keygen_tab, width=345, height=300)
publickey.grid(row=1,column=0, sticky="w")
privatekey = customtkinter.CTkTextbox(master=keygen_tab, width=345, height=300)
privatekey.grid(row=1,column=2, sticky="e")

keyname = customtkinter.CTkEntry(master=keygen_tab, placeholder_text="New key name:", width=130, )
keyname.grid(row=0, column=1, pady=7)
genkey = customtkinter.CTkLabel(master=keygen_tab, text="All generated keys\n are written to\n /keys/ with the\n"
                                                        " given name.", width=75, )
genkey.grid(row=1, column=1, pady=7, sticky='n')
vkeylabel = customtkinter.CTkLabel(master=keygen_tab, text="Private key:\n(dont send this one)", width=130, )
vkeylabel.grid(row=0, column=0, pady=7)
bkeylabel = customtkinter.CTkLabel(master=keygen_tab, text="Public key:\n(do send this one)", width=130, )
bkeylabel.grid(row=0, column=2, pady=7)

app.mainloop()
