import cv2
import face_recognition
import numpy as np
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk
import time
import os
import threading
from plyer import notification 

# 1. SETUP
log_dir = "incident_logs"
if not os.path.exists(log_dir): os.makedirs(log_dir)
text_log_path = os.path.join(log_dir, "security_audit.txt")

try:
    owner_image = face_recognition.load_image_file("owner.jpg")
    owner_encoding = face_recognition.face_encodings(owner_image)[0]
    print("✓ Biometric Key Ready.")
except:
    print("X ERROR: No owner.jpg found."); exit()

# SHARED STATE
is_authorized = True
is_blurred = False
last_frame = None
last_log_time = 0
current_faces = [] 
motion_detected = False
motion_contours = [] # For drawing motion areas

# --- BACKGROUND ALERT ---
def background_alert(ts, frame_copy):
    try:
        with open(text_log_path, "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] SECURITY BREACH: Unauthorized face detected.\n")
        
        # Forensic Header
        cv2.rectangle(frame_copy, (0, 0), (frame_copy.shape[1], 40), (0, 0, 0), -1)
        header_text = f"BREACH DETECTED | {ts} | SYSTEM: SECURE LENS"
        cv2.putText(frame_copy, header_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imwrite(os.path.join(log_dir, f"intruder_{int(time.time())}.jpg"), frame_copy)
        
        time.sleep(1.0) 
        notification.notify(title="SECURITY ALERT", message=f"Breach logged at {ts}", app_name="SecureLens_Final", timeout=5)
    except: pass

# 2. THE BRAIN
def biometric_audit():
    global is_authorized, last_frame, current_faces, motion_detected, motion_contours
    prev_gray = None
    
    while True:
        if last_frame is not None:
            # A. MOTION DETECTION (Processing)
            gray = cv2.cvtColor(cv2.resize(last_frame, (160, 120)), cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if prev_gray is None:
                prev_gray = gray
                continue

            frame_delta = cv2.absdiff(prev_gray, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            
            # --- NEW: DETECT CONTOURS OF MOTION ---
            cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion_contours = cnts # Store for drawing later
            
            motion_score = np.sum(thresh)
            prev_gray = gray

            if motion_score > 5000:
                motion_detected = True
                small_frame = cv2.resize(last_frame, (0, 0), fx=0.5, fy=0.5)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                temp_is_authorized = True
                temp_face_data = []

                if len(face_encodings) > 0:
                    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                        matches = face_recognition.compare_faces([owner_encoding], encoding, tolerance=0.65)
                        is_owner = matches[0]
                        temp_face_data.append(((top*2, right*2, bottom*2, left*2), is_owner))
                        if not is_owner: temp_is_authorized = False
                    if len(face_encodings) > 1: temp_is_authorized = False
                else:
                    temp_is_authorized = is_authorized

                is_authorized = temp_is_authorized
                current_faces = temp_face_data
            else:
                motion_detected = False
                motion_contours = []
        
        time.sleep(0.2)

# 3. DISPLAY & UI
overlay = tk.Tk()
overlay.attributes("-fullscreen", True, "-topmost", True)
overlay.withdraw()
canvas = tk.Label(overlay)
canvas.pack()

cap = cv2.VideoCapture(0)
threading.Thread(target=biometric_audit, daemon=True).start()

# For FPS Calculation
prev_time = 0

while True:
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    last_frame = frame.copy() 

    # --- DRAW MOTION CONTOURS ---
    # Scaled up from 160x120 back to frame size
    h_scale, w_scale = frame.shape[0]/120, frame.shape[1]/160
    for c in motion_contours:
        if cv2.contourArea(c) < 500: continue # Ignore tiny movements
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (int(x*w_scale), int(y*h_scale)), 
                      (int((x+w)*w_scale), int((y+h)*h_scale)), (255, 255, 0), 1)

    # --- TECHNICAL DATA OVERLAY ---
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
    prev_time = curr_time

    # Dark HUD Background
    cv2.rectangle(frame, (frame.shape[1]-220, 0), (frame.shape[1], 100), (40, 40, 40), -1)
    cv2.putText(frame, f"FPS: {int(fps)}", (frame.shape[1]-210, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"MOTION: {'ON' if motion_detected else 'IDLE'}", (frame.shape[1]-210, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(frame, f"STATUS: {'SECURE' if is_authorized else 'BREACH'}", (frame.shape[1]-210, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0) if is_authorized else (0, 0, 255), 1)

    # Face Boxes
    for (top, right, bottom, left), is_owner in current_faces:
        color = (0, 255, 0) if is_owner else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    if not is_authorized:
        if not is_blurred:
            screenshot = pyautogui.screenshot()
            scr_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            scr_small = cv2.resize(scr_np, (0,0), fx=0.5, fy=0.5)
            scr_blur = cv2.GaussianBlur(scr_np, (41, 41), 0)
            img_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(scr_blur, cv2.COLOR_BGR2RGB)))
            canvas.config(image=img_tk)
            canvas.image = img_tk
            overlay.deiconify()
            overlay.update()
            is_blurred = True

            if time.time() - last_log_time > 15:
                ts = time.strftime("%H:%M:%S")
                threading.Thread(target=background_alert, args=(ts, frame.copy()), daemon=True).start()
                last_log_time = time.time()
    else:
        if is_blurred:
            overlay.withdraw()
            is_blurred = False
            last_log_time = 0 
    
    cv2.imshow('Secure Lens - SOC Edition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()