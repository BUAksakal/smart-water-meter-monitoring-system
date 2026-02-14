# 💧 Water Meter Monitoring & Live Data Visualization
**Internship Project – Baylan Water & Energy Meters**

This project is a real-time monitoring and visualization system developed during my internship at **Baylan Water & Energy Meters**. The aim of the project was to process, analyze, and visualize smart water meter payload data through both a desktop interface and a live web dashboard.

The system combines data processing, file monitoring, GUI development, and live data visualization into a unified pipeline. Incoming payload data is decoded, transformed into meaningful metrics (such as voltage, credit, battery status, warnings, and connection types), and presented to the user through interactive interfaces.

---

## 🚀 Project Overview

The system consists of three main components:

### 🖥️ Desktop Monitoring Application (Tkinter)
A graphical user interface built with **Python + Tkinter** that allows real-time monitoring of decoded meter data, manual data input for testing, background process management, live updates through file change detection, and automatic decoding of payload information. Key features include voltage calculation, credit extraction, battery status interpretation, warning detection, and meter type identification.
![710af76d-64b1-44fe-8596-c44580633ee5](https://github.com/user-attachments/assets/1586f71c-e392-4324-a188-772a8022933c)


### 🌐 Live Web Dashboard (Streamlit)
A lightweight web dashboard designed for live monitoring that displays incoming data in table format, refreshes automatically at intervals, connects to a local API or JSON source, and provides quick operational visualization.

### ⚙️ Data Processing Pipeline
The backend logic handles JSON-based payload parsing, data decoding and transformation, event-driven updates via file system monitoring, and logging/process control. The architecture separates data generation, processing, and visualization layers for clarity and scalability.

---

## 🧱 System Workflow

Incoming Payload Data → JSON Storage → Data Processing & Decoding (Python) → File Monitoring (Watchdog) → Desktop GUI (Tkinter) + Live Dashboard (Streamlit)

---

## 📸 Demo Video

A demo video showing the full system workflow will be added here:




https://github.com/user-attachments/assets/2605876d-2a5b-4f7d-b2a5-17c5035db465




---

## 🧠 Technologies Used

**Programming & Core**
- Python
- JSON Processing

**GUI & Visualization**
- Tkinter
- Streamlit
- Pillow (PIL)

**Data Handling & Automation**
- Watchdog (file monitoring)
- Subprocess
- Logging

**Libraries & Tools**
- Pandas
- Requests
- Queue / Threading
- Flask API (integration side)

---

## 🧩 Key Technical Highlights

- Real-time payload decoding pipeline
- Event-driven architecture using file system observers
- Parallel desktop and web visualization
- Modular structure allowing integration with external services
- Manual and live data modes for testing and debugging

---

## 🎓 Academic & Professional Context

Developed as an **internship project** at Baylan Water & Energy Meters, focusing on practical applications of data processing, monitoring systems, and user interface design within smart metering technologies.

---

## ⚠️ Note

Due to company confidentiality policies, some components and internal implementation details have been simplified or adapted for demonstration purposes.

---

## 👨‍💻 Author

**Berke Uğur Aksakal**  
AI Engineering Master’s Student  
Deggendorf Institute of Technology
