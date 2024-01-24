import customtkinter
from Crypto.Util import number
import math
import os
from PIL import Image


if not os.path.exists("keys"):
    os.makedirs("keys")


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
    # Couldn't figure out how to calculate keys without using variables. Maybe that's an issue? 1.05
    with open(f'keys/{keyname.get()}-public.key', 'w') as file:
        file.write(f"{keymod},{publick}")
        file.close()
    with open(f'keys/{keyname.get()}-private.key', 'w') as file:
        file.write(f"{keymod},{privatek}")
        file.close()


def keygen_run():
    global wkeyname
    wkeyname = keyname.get()
    if os.path.isfile(f"keys/{keyname.get()}-public.key") or os.path.isfile(f"{keyname.get()}/-private.key"):
        print("Key with given name already exists.")
        return 1
    else:
        generate_keys()
        print("Complete. Written to .key files.")
        publickey.delete(0.0, 'end')
        publickey.insert("end", f"{keymod}, {publick}")
        privatekey.delete(0.0, 'end')
        privatekey.insert("end", f"{keymod}, {privatek}")


def submit_e():
    encode()


def encode():
    global encoded
    encode_two = int.from_bytes(to_encode.get().encode('utf-8'), byteorder='big', signed=False)
    if ekeylocation.get().startswith("/"):
        if ekeylocation.get().startswith("//"):
            with open(f'keys/{ekeylocation.get()}-public.key', "r") as f:
                content = f.read()
                keymod, publick = content.split(",")
        else:
            with open(ekeylocation.get()) as f:
                content = f.read()
                keymod, publick = content.split(",")
    else:
        keymod, publick = ekeylocation.get().split(",")
    encoded = pow(encode_two, int(publick), int(keymod), )
    Eoutput.delete(index1=0.0, index2='end')
    Eoutput.insert("end", encoded)


def submit_d():
    decode()


def decode():
    global decoded
    encodedfile = to_decode.get(0.0, 'end')
    if to_decode.get(0.0, 'end').startswith("/"):
        encodedfile = encodedfile.strip(encodedfile.split("/", 1)[1])
        with open(f"{encodedfile}", "r") as f:
            message = f.read()
    else:
        message = encodedfile
    with open(f'keys/{keylocation.get()}-private.key', "r") as f:
        content = f.read()
        Doutput.delete(index1=0.0, index2='end')
        Doutput.insert("end", (int(pow(int(message), int(content.split(",")[1]),
                                       int(content.split(",")[0])))).to_bytes(math.ceil((int(pow(int(message),
                                                                                                 int(content.split(",")[
                                                                                                         1]),
                                                                                                 int(content.split(",")
                                                                                                     [0]))))
                                                                                        .bit_length() / 8), byteorder=
                                                                              'big', signed=False).decode('utf-8'))


customtkinter.set_appearance_mode("dark")
app = customtkinter.CTk()
app.title("TeRSA")
app.geometry("832x400")
helpfont = customtkinter.CTkFont(size=15)
tabview = customtkinter.CTkTabview(app, width=800, height=410)
tabview.grid(row=0, column=0, pady=10)
encode_tab = tabview.add('Encode')
decode_tab = tabview.add('Decode')
keygen_tab = tabview.add('Key generation')
helptab = tabview.add("Help")

# Encode tab
to_encode = customtkinter.CTkEntry(encode_tab, placeholder_text="Message to encode?", height=30, width=700)
to_encode.grid(row=0, column=0, sticky="w", padx=5, pady=7)
submit = customtkinter.CTkButton(master=encode_tab, command=submit_e, text="Encode", width=100)
submit.grid(row=0, column=1, padx=5)
ekeylocation = customtkinter.CTkEntry(encode_tab, placeholder_text="Enter key. To use key directory, prefix the "
                                                                   "path with '/'. To use the key name (from /keys/),"
                                                                   "prefix the name with '//'.", height=30, width=800)
ekeylocation.grid(row=1, column=0, padx=5, pady=7, sticky="ew", columnspan=2)
Eoutput = customtkinter.CTkTextbox(master=encode_tab, width=800, pady=5, height=230)
Eoutput.grid(row=2, column=0, padx=5, pady=7, columnspan=2, sticky='ew')

# Decode tab
to_decode = customtkinter.CTkTextbox(master=decode_tab, width=700, pady=5, height=230)
to_decode.grid(row=0, column=0, padx=5, pady=7, sticky='w', columnspan=1)
submit = customtkinter.CTkButton(master=decode_tab, command=submit_d, text="Decode", width=100)
submit.grid(row=0, column=1, pady=7, sticky='nw')
encodeinfo = customtkinter.CTkLabel(master=decode_tab, text="Enter RSA encoded\nmessage or file\nlocation here.",
                                    width=100)
encodeinfo.grid(row=0, column=1, pady=7)
keylocation = customtkinter.CTkEntry(decode_tab, placeholder_text="Key name? (Ensure key is in /keys/ subfolder)",
                                     height=30,
                                     width=800)
keylocation.grid(row=1, column=0, pady=7, padx=5, sticky="ew", columnspan=2)
Doutput = customtkinter.CTkTextbox(decode_tab, height=30, width=810)
Doutput.grid(row=2, column=0, sticky="w", padx=5, pady=7, columnspan=2)

# Keygen tab
genkey = customtkinter.CTkButton(master=keygen_tab, command=keygen_run, text="Generate new keys", width=75, )
genkey.grid(row=1, column=1, pady=7)
publickey = customtkinter.CTkTextbox(master=keygen_tab, width=345, height=300)
publickey.grid(row=1, column=0, sticky="w")
privatekey = customtkinter.CTkTextbox(master=keygen_tab, width=345, height=300)
privatekey.grid(row=1, column=2, sticky="e")
keyname = customtkinter.CTkEntry(master=keygen_tab, placeholder_text="New key name:", width=130, )
keyname.grid(row=0, column=1, pady=7)
genkey = customtkinter.CTkLabel(master=keygen_tab, text="All generated keys\n are written to\n /keys/ with the\n"
                                                        " given name.", width=75, )
genkey.grid(row=1, column=1, pady=7, sticky='n')
vkeylabel = customtkinter.CTkLabel(master=keygen_tab, text="Private key:\n(dont send this one)", width=130, )
vkeylabel.grid(row=0, column=0, pady=7)
bkeylabel = customtkinter.CTkLabel(master=keygen_tab, text="Public key:\n(do send this one)", width=130, )
bkeylabel.grid(row=0, column=2, pady=7)

# Help tab
helpfrm = customtkinter.CTkFrame(master=helptab, width=820)
helpfrm.grid(row=0, column=0)
help1 = customtkinter.CTkTextbox(helpfrm, 500, 340, )
help1.grid(row=0,column=0)
help1.insert("0.0", "TeRSA uses"
                    " a method of encryption known as RSA. RSA encryption is a widely used \nasymmetric"
                    " cryptographic algorithm that involves a pair of keys, one public and one \nprivate. The sender "
                    "uses the recipient's public key to encrypt the message, and only \nthe recipient, who possesses "
                    "the corresponding private key, can decrypt and access \nthe original content.\n\nTo use TeRSA, you"
                    " first must receive a public key from the intended recipient, while \nthey retain their private key."
                    " To send a message, enter both the message you'd like to encrypt and the key itself. The key can "
                    "be formatted in several different ways \n(keyname, key path, raw key). If you can't figure the"
                    " formatting out, just paste the raw key. Send the resulting encoded number at the bottom to the"
                    " recipient . (the one who \ngenerated the keys)\n"
                    "\nIf you wish to receive a message, begin by using the Generate Keys tab to generate a pair of "
                    "keys. Then, send the generated public key (found either in the GUI after \ngeneration or in the "
                    "/keys/ sub-folder of the program) to whom you would like to \nreceive the message from."
                    "Once they have encoded it, enter the encoded message \n(should look like gibberish numbers) and the "
                    "original key name into the decode tab.")
help1.configure(state="disabled")
helpimage = customtkinter.CTkImage(light_image=Image.open("lightchart.png"), dark_image=Image.open("darkchart.png"),
                                   size=(320,320))
imagelabel = customtkinter.CTkLabel(helptab, image=helpimage)
imagelabel.grid(row=0, column=1)
app.mainloop()
