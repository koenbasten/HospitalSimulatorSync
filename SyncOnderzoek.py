import random
import threading
from queue import PriorityQueue
import time
from gui import set_patient, clear_patient, maxSizeQueue, clear_doctor, set_doctor, add_patient, start, remove_patient_from_queue, amountOfRooms


patient_counter = 0


doctors = threading.Semaphore(4)
beds = threading.Semaphore(amountOfRooms)

waitingRoom = PriorityQueue(maxsize=maxSizeQueue)

waitingRoomChanged = threading.Semaphore(1)
addingToWaitingRoomGUI = threading.Semaphore(1)


def thread_producer():
    global patient_counter
    while True:
        if waitingRoom.qsize() < maxSizeQueue:
            time.sleep(0.2)
            # print(waitingRoom.qsize())
            priority = random.randint(0, 2)
            waitingRoom.put((priority , patient_counter))

            addingToWaitingRoomGUI.acquire()
            add_patient(patient_counter, priority)
            addingToWaitingRoomGUI.release()

            patient_counter += 1

        else:
            time.sleep(0.3)


def thread_consumer(id_room):
    while True:
        beds.acquire()

        priority, patient_id = waitingRoom.get()

        addingToWaitingRoomGUI.acquire()
        remove_patient_from_queue(patient_id)
        set_patient(id_room, priority,patient_id)
        addingToWaitingRoomGUI.release()

        time.sleep(0.2)
        doctors.acquire()
        set_doctor(id_room)

        time.sleep(random.randint(4, 6))
        doctors.release()
        clear_doctor(id_room)
        clear_patient(id_room)
        time.sleep(0.2)

        beds.release()



thread_producer = threading.Thread(target=thread_producer)
consumers = []
for n in range(amountOfRooms):
    t = threading.Thread(target=thread_consumer, args=([n]))
    consumers.append(t)


def main():
    thread_producer.start()

    for t in consumers:
        t.start()

    for t in consumers:
        t.join()
    thread_producer.join()


if __name__=="__main__":
    threading.Thread(target=main).start()
    start()



