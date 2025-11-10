  
# 🌪️ Disaster-Relief-and-Rescue-System (DRAMS) 🚨
> A real-time disaster detection and rescue system made with ❤️ using Python, OpenCV & AI models 🤖  

![GitHub Repo stars](https://img.shields.io/github/stars/Shristirajpoot/Disaster-Relief-and-Rescue-System?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/Shristirajpoot/Disaster-Relief-and-Rescue-System?color=brightgreen)
![Built with](https://img.shields.io/badge/Built%20with-Python%20%7C%20OpenCV%20%7C%20DeepLearning-blue)

---

## 🌟 Overview

**DRAMS** is an AI-powered system to **detect disasters** like **fire 🔥 and flood 🌊** in real-time. It helps rescue teams respond faster by sending **automatic alerts 📢 with snapshots 📸**. The project also provides **Grad-CAM visualizations 🧠** for model interpretability.  

---

## 🎥 Demo Video

📺 **Watch the walkthrough here:**  
[![DRAMS - Demo Video](https://img.youtube.com/vi/4QeUZMUl0Ec/0.jpg)](https://youtu.be/4QeUZMUl0Ec)

> 🔗 *Click the image or [watch on YouTube](https://youtu.be/4QeUZMUl0Ec)*
---------

## 🎨 Features

- 🔥 Real-time **fire detection**  
- 🌊 Real-time **flood detection**  
- 🖥️ **Web streaming interface** for live monitoring  
- 📸 Automatic **alert snapshots** on disaster detection  
- 🧠 **Grad-CAM visualizations** for AI predictions  
- 🗄️ Stores data & metadata in **MongoDB**  
- 📱 Fully **responsive** web interface  
- ⚡ Quick AI predictions for emergency response  

---

## 📂 Project Structure

```plaintext
Disaster-Relief-and-Rescue-System/
├── DRAMS/                  # Web app files (Django/Flask)
├── Dataset/                # Fire & flood images/videos
├── firedetector/           # Fire prediction scripts
├── flooddetector/          # Flood prediction scripts
├── alert_snapshots/        # Captured alert images
├── output/                 # Prediction outputs
├── templates/              # HTML templates
├── static/                 # CSS / JS / assets
├── gradcam_visualizer.py   # Grad-CAM visualizer
├── predict_fire.py         # Fire prediction script
├── predict_flood.py        # Flood prediction script
├── train.py                # AI model training script
├── webstreaming.py         # Web streaming interface
├── requirements.txt        # Python dependencies
└── venv/                   # Virtual environment

```
## 🖼️ Screenshots
📸 Real views of DRAMS in action:

## 🖼️ Screenshots
📸 **Real Outputs & Model Visualizations from DRAMS (Disaster Relief and Management System)**

| Fire Detection (Grad-CAM) | Flood Detection Outputs | Flood Detection Variants |
| :------------------------: | :---------------------: | :----------------------: |
| <img src="./gradcam_fire.jpg" width="300"/> | <img src="./flood_output.jpg" width="300"/> | <img src="./flood_output_2.jpg" width="300"/> |
| <img src="./gradcam_flood.jpg" width="300"/> | <img src="./flood_output_3.jpg" width="300"/> | <img src="./flood_output4.jpg" width="300"/> |

| Model Training Visuals | LR Finder Curve | Color Plot |
| :--------------------: | :--------------: | :---------: |
| <img src="./training_plot.png" width="300"/> | <img src="./lrfind_plot.png" width="300"/> | <img src="./clr_plot.png" width="300"/> |

| Raw Output Frame | Grad-CAM (Alt Frame) |
| :---------------: | :-----------------: |
| <img src="./output_0.jpg" width="300"/> | <img src="./gradcam_fire_1761656138.jpg" width="300"/> |


## 🚀 Getting Started
📦 Install Dependencies
```bash
Copy code
git clone https://github.com/Shristirajpoot/Disaster-Relief-and-Rescue-System.git
cd Disaster-Relief-and-Rescue-System
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### ▶️ Run the System
```bash
Copy code
python webstreaming.py
```
🌐 Open http://127.0.0.1:5000 to see live disaster detection

## 🛠️ Built With
- 🐍 Python 3

- 🌐 Django / Flask

- 🖼️ OpenCV for video processing

- 🤖 TensorFlow / PyTorch for AI models

- 🗄️ MongoDB for dataset storage

- 🎨 HTML5 + CSS3 for web interface

## 👩‍💻 Author
### Shristi Rajpoot
- 📧 Email: shristirajpoot369@gmail.com
- 🔗 GitHub: @Shristirajpoot

## 📄 License
This project is licensed under the MIT License.

### 🌟 If you liked this project, consider starring the repo and sharing it!
