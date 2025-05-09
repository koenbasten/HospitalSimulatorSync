import tkinter as tk
from pathlib import Path

amountOfRooms = 6
maxSizeQueue = 8

rooms = []

root = tk.Tk()
lb = None

def start():
    global root, lb

    root.title("Hospital Simulation Sync")
    root.geometry("1800x600")


    queue_frame = tk.Frame(root, bg="lightblue", height=100)  # create the queueFrame
    queue_frame.pack(fill="x")

    label = tk.Label(queue_frame, text="WaitingRoom/Queue", bg="lightblue")  # QueueLabel
    label.pack(padx=8, pady=8)
    lb = tk.Listbox(queue_frame, width=30, height=10)  # QueueList
    lb.pack(padx=10, pady=10, expand=False)

    row = tk.Frame(root) # field for rooms
    row.pack(padx=10, pady=60)

    for col in range(amountOfRooms):
        room_frame = tk.Frame(row, bg="lightblue", height=100, borderwidth=5, relief="groove", width=30)  # create the queueFrame
        room_frame.grid(row=0,column=col)
        # small label on top
        tk.Label(room_frame, text=f"Room {col + 1}").grid(row=0, column=0, padx=16, pady=(0, 8))
        # entry box right under it
        label_doctor = tk.Label(room_frame, text="No doctor", bg="lightblue")  # QueueLabel
        label_doctor.grid(row=1, column=0, padx=16, pady=(12, 20))

        label_patient = tk.Label(room_frame, text="PatientID:  NO PATIENT Priority: NONE", bg="lightblue")  # QueueLabel
        label_patient.grid(row=2, column=0, padx=16, pady=(12, 20))

        rooms.append({"frame": room_frame,"doctor": label_doctor, "patient": label_patient})

    root.mainloop()


def add_patient(patient, priority):
    global lb
    text = format_patient(patient, priority)
    root.after(0, lambda: lb.insert(patient, text))

def remove_patient_from_queue(patient_id: int):
    prefix = f"PatientID:  {patient_id}"
    global lb

    def _do_delete():
        matches = [
            idx
            for idx, text in enumerate(lb.get(0, tk.END))
            if text.startswith(prefix)
        ]
        for idx in reversed(matches):
            lb.delete(idx)

    root.after(0, _do_delete)

def clear_doctor(room_id: int):
    lbl = rooms[room_id]["doctor"]
    lbl.config(text="No doctor")
    lbl.grid()

def set_doctor(room_id: int):
    lbl = rooms[room_id]["doctor"]
    frame = rooms[room_id]["frame"]
    frame.config(bg="green")
    lbl.config(text="Doctor present")
    lbl.grid()

def clear_patient(room_id: int):
    lbl = rooms[room_id]["patient"]
    frame = rooms[room_id]["frame"]
    frame.config(bg="lightblue")
    lbl.config(text="PatientID:  NO PATIENT Priority: NONE")
    lbl.grid()


def set_patient(room_id: int, priority, patient):
    lbl = rooms[room_id]["patient"]

    text = format_patient(patient, priority)
    lbl.config(text=f"Patient: {text}")
    lbl.grid()




def format_patient(patient, priority):
    priority_text = ""
    if priority == 0:
        priority_text = "HIGH"
    elif priority == 1:
        priority_text = "MEDIUM"
    elif priority == 2:
        priority_text = "LOW"

    return "PatientID:  " + str(patient) + "  Priority:  " + priority_text