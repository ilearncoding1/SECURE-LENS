# SECURE-LENS

<img src="https://img.shields.io/badge/language-python-blue.svg" alt="Python Badge">
<img src="https://img.shields.io/badge/security-biometric-lightgreen" alt="Biometric Security Badge">
<img src="https://img.shields.io/badge/license-unlicensed-lightgrey" alt="License Badge">

<p align="center">
  <img src="https://user-images.githubusercontent.com/198291843/placeholder-securelens-demo.gif" alt="SECURE-LENS Demo" width="540">
</p>

**SECURE-LENS** is a real-time computer vision security application focused on biometric authentication and automatic incident response. Powered by Python and leveraging libraries such as OpenCV, face_recognition, and PyAutoGUI, this project turns your webcam into a security sentinel that locks down your computer when unauthorized faces are detected.

---

## 🚀 Features

- 🎯 **Biometric Authentication**
- 🚨 **Motion-Triggered Monitoring**
- 🔒 **Automatic Screen Lockdown**
- 📝 **Incident Logging & Snapshots**
- 🔔 **Real-Time Desktop Notifications**
- ⚡ **Multi-threaded – Always Responsive**

---

## 🖼️ Demo

<p align="center">
  <!-- Replace with actual GIF/Screenshot if available -->
  <img src="https://user-images.githubusercontent.com/198291843/placeholder-securelens-demo.gif" alt="Demo Animation" width="480">
  <br>
  <b>Live Intrusion Detection and Screen Blur</b>
</p>

---

## 🎬 How It Works

1. 🧑 **Enroll Your Face**:<br>&nbsp;&nbsp;&nbsp;&nbsp;Place a clear frontal image (`owner.jpg`) in the root folder.
2. 🎥 **Webcam Surveillance**:<br>&nbsp;&nbsp;&nbsp;&nbsp;Monitors for motion and scans for faces only if something moves.
3. 🕵️‍♂️ **Breach Response**:<br>&nbsp;&nbsp;&nbsp;&nbsp;If an unauthorized face is detected:
    - An incident is logged with a snapshot and timestamp.
    - The desktop display is blurred and a fullscreen warning overlay appears.
    - You receive a real-time notification.
4. 🙆 **Recovery**:<br>&nbsp;&nbsp;&nbsp;&nbsp;Restores access automatically for authorized users.

---

## ⚙️ Getting Started

### Requirements

- Python 3.8+
- `opencv-python`
- `face_recognition`
- `numpy`
- `pyautogui`
- `Pillow`
- `plyer`

Install dependencies:
```sh
pip install opencv-python face_recognition numpy pyautogui Pillow plyer
```

### Quick Start

1. **Add `owner.jpg`** – Save your face image (frontal, well-lit) as `owner.jpg` in the repo folder.
2. **Run the application:**
   ```sh
   python "Secure Lens.py"
   ```
3. **Exit any time:** Press `q` in the main camera window.

---

## 📁 Project Structure

```text
SECURE-LENS/
├── Secure Lens.py             # Main application
├── Secure Lens cropped.py     # (Alternative/app variant)
├── .gitignore
├── incident_logs/             # Forensic images/logs
│   └── security_audit.txt
└── owner.jpg                  # Your biometric key (not in repo)
```

---

## 🛡️ Security & Privacy

- **Local only:** No biometric data leaves your device.
- **Forensic audit:** Incident logs + snapshot images per breach.
- **Total control:** Close the app to release webcam.

---

## 🧩 Contributing

Pull requests, suggestions, and issues are always welcome!
1. Fork the project
2. Create a new branch
3. Submit a PR with details of your changes or ideas

---

## 📜 License

Unlicensed (for now). For commercial or non-personal use, please contact the maintainer.

---

<p align="center">
 <b>Stay secure with <span style="color:#43b581">SECURE-LENS</span>!</b>
</p>
