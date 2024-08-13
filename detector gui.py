import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
import os

top = tk.Tk()
top.geometry("800x600")
top.title("Meeting Room Analyzer")
top.configure(background="#CDCDCD")
label_gender = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
label_age = Label(top, background="#CDCDCD", font=("arial", 15, "bold"))
sign_image = Label(top)

def analyze_meeting_room(image_path):
    try:
        global label_gender, label_age

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (400, 300))

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) < 2:
            messagebox.showerror("Error", "Less than 2 people detected in the meeting.")
            return
        males_count = 0
        females_count = 0

        for (x, y, w, h) in faces:
            face_roi = image[y:y+h, x:x+w]
            
            shirt_color = detect_shirt_color(face_roi)

            if shirt_color == "white":
                age = 23
            elif shirt_color == "black":
                age = "Child"
            else:
                age = predict_age_from_face(face_roi)
            gender = predict_gender_from_face(face_roi)
            if gender == "Male":
                males_count += 1
            elif gender == "Female":
                females_count += 1

        label_gender.config(foreground="#011638", text=f"Males: {males_count}, Females: {females_count}")
        label_age.config(foreground="#011638", text=f"Age prediction: {age}")

    except Exception as e:
        print("Error:", e)
def predict_gender_from_face(face_roi):
    return "Male"  
def predict_age_from_face(face_roi):
    return 30 
def detect_shirt_color(face_roi):
    avg_color_per_row = np.average(face_roi, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    b, g, r = avg_color

    if r > 200 and g > 200 and b > 200:
        return "white"
    elif r < 50 and g < 50 and b < 50:
        return "black"
    else:
        return "unknown"

def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label_gender.config(text="")
        label_age.config(text="")
        analyze_meeting_room(file_path)

    except Exception as e:
        print("Error:", e)

# Button to upload an image
upload_button = Button(top, text="Upload Meeting Room Image", command=upload_image, padx=10, pady=5)
upload_button.config(background="#364156", foreground="white", font=("arial", 10, "bold"))
upload_button.pack(side="bottom", pady=20)

# Packing labels
sign_image.pack(side="bottom", expand=True)
label_gender.pack()
label_age.pack()

# Label for heading
heading = Label(top, text="Meeting Room Analyzer", pady=20, font=("arial", 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

# Start GUI main loop
top.mainloop()
