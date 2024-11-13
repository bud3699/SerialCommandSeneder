import serial
import threading
import tkinter as tk
from tkinter import scrolledtext

serial_port = 'COM6'
baud_rate = 57600

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")

def read_from_serial():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            output_text.insert(tk.END, data + "\n")
            output_text.see(tk.END)

def send_command(event=None): 
    command = command_entry.get()
    if command:
        ser.write((command + '\n').encode('utf-8'))
        command_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Buds Serial Command Sender")
root.geometry("500x300")

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
output_text.pack(padx=10, pady=10)
output_text.config(state=tk.NORMAL)

command_entry = tk.Entry(root, width=40)
command_entry.pack(padx=10, pady=5)

send_button = tk.Button(root, text="Send", command=send_command)
send_button.pack(pady=5)

command_entry.bind('<Return>', send_command)

thread = threading.Thread(target=read_from_serial, daemon=True)
thread.start()

root.mainloop()
