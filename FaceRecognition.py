from random import choice
import sys
import threading
import cv2
from deepface import DeepFace
import customtkinter as ctk
from tkinter import filedialog


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

face_match = False

reference_image = None


def chose_imgage():
    global reference_image
    file_path = filedialog.askopenfilename(filetypes=[("Reference Images", "*.jpg;*.png"), ("All files", "*.*")])
    reference_image = cv2.imread(file_path)
    start_button.pack(pady=10)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def on_closing():
    print("Se inchide aplicatia...")
    root.quit()
    sys.exit()

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_image.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

def face_window():
    global counter
    while True:
        ret, frame = cap.read()

        if ret:
            if counter % 30 == 0:
                try:
                    threading.Thread(target=check_face, args=(frame.copy(), )).start()
                except ValueError:
                    pass
            counter+=1

            if face_match: 
                cv2.putText(frame, "MATCH", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame,"NO MATCH", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("video", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or cv2.getWindowProperty("video", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

#Configurez fereastra
root =ctk.CTk()
root.title("Recunoasterea fetei")
root.geometry("200x150")

start_button = ctk.CTkButton(root, text="Incepe", command=face_window)

choice_button = ctk.CTkButton(root, text="Choose a reference image", command=chose_imgage)
choice_button.pack(pady=20)

root.protocol("WM_DELETE_WINDOW", on_closing)

def main():
    root.mainloop()
    
if __name__== "__main__":
    main()