import tkinter as tk  # UI
import telnetlib  # เชื่อมต่อ Laser ด้วย Telnet
from datetime import datetime  # ใช้ดึงเวลาปัจจุบัน
import pygame  # สำหรับเล่นเสียง
import threading
import os
import csv
import time

# กำหนด UI
root = tk.Tk()

# Function to toggle data recording
def toggle_recording():
    global recording
    recording = not recording
    recording_status.config(text=f"Recording: {'On' if recording else 'Off'}")

# Create button and label for recording control

root.title("Laser VIRON (Version 2.5 add sound)")
root.configure(bg='#B8BBBF')

# กำหนดค่าการเชื่อมต่อ Telnet
global telnet_ip
telnet_ip = tk.StringVar()
telnet_ip.set("10.49.234.235")  # กำหนดค่าเริ่มต้น IP Address
global telnet_port
telnet_port = tk.StringVar()
telnet_port.set("23")  # กำหนดค่าเริ่มต้น Port
global telnet_user
telnet_user = tk.StringVar()
telnet_user.set("VR70AB07")  # กำหนดค่าเริ่มต้น Login $LOGIN OK

# Variable to control sound and recording
sound_on = True
recording = True

# Function to toggle data recording
def toggle_recording():
    global recording
    recording = not recording
    recording_status.config(text=f"Recording: {'On' if recording else 'Off'}")


# Directory for storing logs
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Variables for recording data
log_file = None
log_writer = None

# Initialize pygame for sound
pygame.mixer.init()

# ฟังก์ชันเล่นเสียง
def play_sound(file_path):
    if sound_on:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

# แสดงผลการตั้งค่าเลเซอร์
def laser_conection_setting():
    print("IP: " + telnet_ip.get())
    print("Port: " + telnet_port.get())
    print("User: " + telnet_user.get())

# ล็อกกับ Laser
def telnet_login(host, port, username):
    try:
        global tn
        current_time = str(datetime.now().strftime("%H:%M:%S"))
        username = "$LOGIN " + username
        tn = telnetlib.Telnet(host, port, timeout=1)
        tn.write(username.encode('ascii') + b"\r\n")
        response = tn.read_until(b"$LOGIN OK: ", timeout=1)
        print("Telnet Connection: OK")
        received_data = response.decode("utf-8").strip()
        terminal.insert(tk.END, current_time+": "+received_data + '\n')
        terminal.see(tk.END)
    except Exception as e:
        print("Telnet Connection: Error:", e)

# เชื่อมต่อกับ Laser
def telnet_connect():
    print("IP: " + str(ip_entry.get()))
    print("Port: " + str(port_entry.get()))
    print("User: " + str(user_entry.get()))
    telnet_login(str(ip_entry.get()), str(port_entry.get()), str(user_entry.get()))

# ล็อกกับ Laser ใหม่
def telnet_relogin():
    print("relogin")
    tn.write(str(user_entry.get()).encode('ascii') + b"\r\n")
    response = tn.read_until(b"$LOGIN OK: ", timeout=1)
    print("Telnet Login: OK")
    received_data = response.decode("utf-8").strip()
    terminal.insert(tk.END, received_data + '\n')
    terminal.see(tk.END)

# ส่งคำสั่งไป Laser
def telnet_send(command):
    current_time = str(datetime.now().strftime("%H:%M:%S"))
    if command == "MANUAL":
        command = str(command_entry.get())
    elif command == "DFREQ":
        command = command + " " + str(frequency_entry.get())
    elif command == "QSDELAY":
        command = command + " " + str(qsdelay_entry.get())

    command = "$" + str(command) + "\r\n"
    tn.write(command.encode())
    response = tn.read_until(b"\r ", timeout=1)
    received_data = response.decode("utf-8").strip()

    if received_data == "$LOGOUT":
        print("LOGOUT")
        tn.close()

    terminal.insert(tk.END, current_time + ": " + received_data + '\n')
    terminal.see(tk.END)

# ฟังก์ชันเล่นเสียงแล้วส่งคำสั่ง
def play_sound_and_send(command):
    def task():
        play_sound('count.mp3')
        if command == "FIRE":
            start_recording()
        else:
            stop_recording()
        telnet_send(command)
    thread = threading.Thread(target=task)
    thread.start()

# ฟังก์ชันเล่นเสียงเมื่อกดปุ่ม Standby
def play_standby_and_send():
    def task():
        play_sound('Standby.mp3')  # เล่นเสียง Standby.mp3
        telnet_send("STANDBY")  # ส่งคำสั่ง Standby
        stop_recording()  # หยุดการบันทึกข้อมูล
    thread = threading.Thread(target=task)
    thread.start()

# Toggle sound on/off
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    mute_button.config(text="Unmute" if not sound_on else "Mute")

# ล้างหน้าจอ Terminal
def terminal_clear():
    terminal.delete('1.0', tk.END)

# Start recording data to CSV
def start_recording():
    global recording, log_file, log_writer
    recording = True
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = open(os.path.join(log_dir, f"laser_{timestamp}.csv"), mode='w', newline='')
    log_writer = csv.writer(log_file)
    log_writer.writerow(["Timestamp", "Machine Status", "QSDELAY", "Internal Temperature (°C)"])
    record_data()

# Stop recording data to CSV
def stop_recording():
    global recording, log_file
    recording = True

# Function to toggle data recording
def toggle_recording():
    global recording
    recording = not recording
    recording_status.config(text=f"Recording: {'On' if recording else 'Off'}")

    if log_file:
        log_file.close()
        log_file = None

# Record data every 5 seconds
def record_data():
    if not recording:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ส่งคำสั่งและบันทึกค่าที่กลับมาในตัวแปร
    tn.write(b"STATUS ?\r\n")
    response = tn.read_until(b"\r ", timeout=1)
    machine_status = response.decode("utf-8").strip()

    tn.write(b"QSDELAY ?\r\n")
    response = tn.read_until(b"\r ", timeout=1)
    qsdelay = response.decode("utf-8").strip()

    tn.write(b"LTEMF ?\r\n")
    response = tn.read_until(b"\r ", timeout=1)
    internal_temp = response.decode("utf-8").strip()

    # บันทึกข้อมูลลงในไฟล์ CSV
    log_writer.writerow([timestamp, machine_status, qsdelay, internal_temp])

    # แสดงผลบน terminal
    terminal.insert(tk.END, f"Recorded: {timestamp}, {machine_status}, {qsdelay}, {internal_temp}\n")
    terminal.see(tk.END)

    # เรียกฟังก์ชันนี้อีกครั้งหลังจาก 5 วินาที
    root.after(5000, record_data)

# Disconnect from Laser
def telnet_disconnect():
    telnet_send("LOGOUT")
    terminal.insert(tk.END, "Disconnected\n")
    terminal.see(tk.END)

laser_conection_setting()

# Configure grid layout
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

connection_frame = tk.LabelFrame(root, borderwidth=2, relief="groove", padx=5, pady=5, text="Laser Connection (Telnet)", fg='#193A76', font=("Arial", 12, 'bold'), bg='#B8BBBF')
connection_frame.pack(padx=20, pady=5, fill="both", expand=True)

# UI for user, IP, and port
user_label = tk.Label(connection_frame, text="User", bg='#B8BBBF')
user_label.pack(row=0, column=0, padx=2, pady=0, sticky='w')
user_entry = tk.Entry(connection_frame, width=15)
user_entry.pack(row=1, column=0, padx=2, pady=0, sticky='w')
user_entry.insert(0, telnet_user.get())

ip_label = tk.Label(connection_frame, text="IP Address", bg='#B8BBBF')
ip_label.pack(row=0, column=1, padx=2, pady=0, sticky='w')
ip_entry = tk.Entry(connection_frame, width=21)
ip_entry.pack(row=1, column=1, padx=2, pady=0, sticky='w')
ip_entry.insert(0, telnet_ip.get())

port_label = tk.Label(connection_frame, text="Port", bg='#B8BBBF')
port_label.pack(row=0, column=2, padx=2, pady=0, sticky='w')
port_entry = tk.Entry(connection_frame, width=8)
port_entry.pack(row=1, column=2, padx=2, pady=0, sticky='w')
port_entry.insert(0, telnet_port.get())

connect_bt = tk.Button(connection_frame, text="Connect", fg='white', command=telnet_connect, bg='#193A76')
connect_bt.pack(row=1, column=3, padx=5, pady=0)

status_frame = tk.LabelFrame(root, borderwidth=2, relief="groove", padx=5, pady=5, text="Laser Response", fg='#193A76', font=("Arial", 12, 'bold'), bg='#B8BBBF')
status_frame.pack(row=2, column=1, padx=19, pady=5, sticky='nsew')

disconnect_bt = tk.Button(connection_frame, text="Disconnect", fg='white', command=telnet_disconnect, bg='#193A76')
disconnect_bt.pack(row=2, column=3, padx=5, pady=5)

recording_status = tk.Label(root, text="Recording: On", bg="#B8BBBF")
recording_status.pack(row=3, column=3, padx=5, pady=5)
toggle_record_button = tk.Button(root, text="Toggle Recording", command=toggle_recording)
#      
# Terminal for displaying responses
terminal = tk.Text(status_frame, height=5, width=49, font=("Arial", 10))
terminal.pack(row=0, column=0, padx=4, pady=0, sticky='nsew')

claer_bt = tk.Button(status_frame, text="Clear", fg='white', width=20, command=terminal_clear, bg='#193A76')
claer_bt.pack(row=1, column=0, padx=0, pady=0)

setting_control_frame = tk.LabelFrame(root, borderwidth=2, relief="groove", padx=5, pady=5, text="Laser Setting", fg='#193A76', font=("Arial", 12, 'bold'), bg='#B8BBBF')
setting_control_frame.pack(row=3, column=1, padx=20, pady=5, sticky='nsew')

# Frequency UI
frequency_label = tk.Label(setting_control_frame, text="Frequency (1-22Hz)", bg='#B8BBBF')
frequency_label.pack(row=0, column=0, padx=(0, 5), pady=0, sticky='w')
frequency_entry = tk.Entry(setting_control_frame, width=25)
frequency_entry.pack(row=0, column=1, padx=(0, 5), pady=0, sticky='w')
frequency_bt_ok = tk.Button(setting_control_frame, text="OK", command=lambda: telnet_send("DFREQ"), fg='white', bg='#193A76')
frequency_bt_ok.pack(row=0, column=2, padx=(0, 5), pady=0, sticky='w')
frequency_bt_get = tk.Button(setting_control_frame, text="Query", command=lambda: telnet_send("DFREQ ?"), fg='white', bg='#193A76')
frequency_bt_get.pack(row=0, column=3, padx=(0, 5), pady=0, sticky='w')

# QSDelay UI
qsdelay_label = tk.Label(setting_control_frame, text="QSDelay (0-400μs)", bg='#B8BBBF')
qsdelay_label.pack(row=1, column=0, padx=(0, 5), pady=0, sticky='w')
qsdelay_entry = tk.Entry(setting_control_frame, width=25)
qsdelay_entry.pack(row=1, column=1, padx=(0, 5), pady=0, sticky='w')
qsdelay_bt_ok = tk.Button(setting_control_frame, text="OK", command=lambda: telnet_send("QSDELAY"), fg='white', bg='#193A76')
qsdelay_bt_ok.pack(row=1, column=2, padx=(0, 5), pady=0, sticky='w')
qsdelay_bt_get = tk.Button(setting_control_frame, text="Query", command=lambda: telnet_send("QSDELAY ?"), fg='white', bg='#193A76')
qsdelay_bt_get.pack(row=1, column=3, padx=(0, 5), pady=0, sticky='w')

# Control buttons for Fire, Standby, Stop, Mute
control_frame = tk.LabelFrame(root, borderwidth=2, relief="groove", padx=5, pady=5, text="Laser Control", fg='#193A76', font=("Arial", 12, 'bold'), bg='#B8BBBF')
control_frame.pack(row=4, column=1, padx=20, pady=5, sticky='nsew')

fire_bt = tk.Button(control_frame, text="Fire", command=lambda: play_sound_and_send("FIRE"), width=11, height=2, font=("Arial", 11, 'bold'), fg='white', bg='#193A76')
fire_bt.pack(row=1, column=0, padx=5, pady=0, sticky='w')

mute_button = tk.Button(control_frame, text="Mute", command=toggle_sound, width=11, height=2, font=("Arial", 11, 'bold'), fg='white', bg='#193A76')
mute_button.pack(row=2, column=0, padx=5, pady=5, sticky='w')

standby_bt = tk.Button(control_frame, text="Standby", command=play_standby_and_send, width=11, height=2, font=("Arial", 11, 'bold'), fg='white', bg='#193A76')
standby_bt.pack(row=1, column=1, padx=5, pady=0, sticky='w')

stop_bt = tk.Button(control_frame, text="Stop", command=lambda: (telnet_send("STOP"), stop_recording()), width=11, height=2, font=("Arial", 11, 'bold'), fg='white', bg='#193A76')
stop_bt.pack(row=1, column=2, padx=4, pady=0, sticky='w')

temperature_frame = tk.LabelFrame(root, borderwidth=2, relief="groove", padx=5, pady=5, text="Laser Temperature", fg='#193A76', font=("Arial", 12, 'bold'), bg='#B8BBBF')
temperature_frame.pack(row=5, column=1, padx=20, pady=5, sticky='nsew')

# Internal and Diode Temperature Queries
internal_temperature_bt = tk.Button(temperature_frame, text="     Internal temperature (°C)     ", command=lambda command="LTEMF ?": telnet_send(command), fg='white', bg='#193A76')
internal_temperature_bt.pack(row=0, column=0, padx=4, pady=0, sticky='w')

diode_temperature_bt = tk.Button(temperature_frame, text="     Diode temperature (°C)     ", command=lambda command="DTEMF ?": telnet_send(command), fg='white', bg='#193A76')
diode_temperature_bt.pack(row=0, column=1, padx=4, pady=0, sticky='w')

command_frame = tk.LabelFrame(root, borderwidth=2, relief="groove", padx=5, pady=5, text="Command (Manual)", fg='#193A76', font=("Arial", 12, 'bold'), bg='#B8BBBF')
command_frame.pack(row=6, column=1, padx=20, pady=5, sticky='nsew')

# Manual Command Entry
command_entry = tk.Entry(command_frame, width=52)
command_entry.pack(row=0, column=0, padx=0, pady=0, sticky='w')
command_bt = tk.Button(command_frame, text="Send", command=lambda command="MANUAL": telnet_send(command), fg='white', bg='#193A76')
command_bt.pack(row=0, column=1, padx=0, pady=0, sticky='w')

warning_label = tk.Label(root, text="Warning: The software may still have bugs. Please use the Laser carefully.", pady=10, fg='red', bg='#B8BBBF')
warning_label.pack(row=7, column=1, sticky='nsew')

# Update and resize to fit content
root.update_idletasks()
root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")

root.mainloop()
