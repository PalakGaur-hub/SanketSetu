# 🤟 SanketSetu — AI-Powered Indian Sign Language Translator

<p align="center">
  <img src="assets/banner.png" alt="SanketSetu Banner" width="100%">
</p>

<p align="center">
  <b>Bridging Hands. Building Understanding.</b><br>
  Deep Learning based Indian Sign Language Translation using MediaPipe + Transformer V5.2.
</p>

<p align="center">

  ![Transformer](https://img.shields.io/badge/Transformer-V5.2-E8B4A0?style=for-the-badge)

  ![Validation Accuracy](https://img.shields.io/badge/Best%20Validation-92.06%25-BFD7C1?style=for-the-badge)

  ![Test Accuracy](https://img.shields.io/badge/Test%20Accuracy-89.76%25-F6EDE3?style=for-the-badge)

  ![Gesture Classes](https://img.shields.io/badge/ISL%20Gestures-210-9DB8C8?style=for-the-badge)

</p>

---

## ✨ About SanketSetu

**SanketSetu** is an AI-powered Indian Sign Language (ISL) translation system built to improve accessibility and communication for the hearing and speech-impaired community.

Instead of recognizing images directly, the model learns **temporal hand movement patterns** from sequences of **MediaPipe hand landmarks** using a custom **Transformer V5.2** architecture. Each gesture is represented as a sequence of **154 frames**, allowing the model to understand motion rather than a single static pose.

The project is being developed as a complete end-to-end accessibility platform consisting of a **Deep Learning model**, **Frontend Web Interface**, and **Backend API**.

---

# 🌟 Features

- 🤟 Real-time Indian Sign Language gesture recognition.
- 🧠 Transformer V5.2 sequence classification model.
- 📷 MediaPipe hand landmark extraction (21 keypoints → 63 features).
- 🎯 Recognition of **210 Indian Sign Language gestures**.
- 📊 Detailed evaluation using confusion matrix, class accuracy and classification reports.
- 🌙 Modern responsive frontend with Dark & Light mode *(currently under development)*.
- 🔊 Future support for live text and voice translation.

---

# 📊 Model Results

| Metric | Result |
|--------|--------|
| 🎯 Test Accuracy | **89.76%** |
| 📈 Best Validation Accuracy | **92.06%** |
| 🤟 Gesture Classes | **210** |
| 📷 Hand Landmark Features | **63** |
| 🎞️ Sequence Length | **154 Frames** |
| 📚 Original Training Samples | **7,320** |
| 🔄 Training Samples After Augmentation | **9,948** |

> **Transformer V5.2** achieved over **92% validation accuracy** while maintaining strong generalization on unseen gesture sequences.

---

# 🧠 Model Pipeline

```text
 Webcam Input
      │
      ▼
 MediaPipe Hand Landmark Detection
 (21 Hand Landmarks → 63 Features)
      │
      ▼
 Sequence Builder
 (154 Frames per Gesture)
      │
      ▼
 Transformer V5.2
 Multi-Head Self Attention
 Feed Forward Network
 Residual Connections
 Layer Normalization
      │
      ▼
 Global Average Pooling
      │
      ▼
 Softmax Classifier
 (210 ISL Gestures)
      │
      ▼
 Predicted Gesture + Confidence Score
```

The prediction is generated in real time using the trained **Transformer V5.2** model.

---

# ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| 🐍 Programming Language | Python |
| 🧠 Deep Learning | TensorFlow, Keras |
| 👋 Hand Tracking | MediaPipe |
| 👁️ Computer Vision | OpenCV |
| 📊 Data Processing | NumPy, Pandas |
| 📈 Visualization | Matplotlib |
| 🤖 Model Evaluation | Scikit-learn |
| 🌐 Frontend *(In Progress)* | React + Tailwind CSS |
| ⚡ Backend *(In Progress)* | Flask |
| 💻 IDE | VS Code & Jupyter Notebook |

---

# 📦 Dataset Information

The dataset consists of landmark sequences extracted from Indian Sign Language gesture videos.

| Dataset Detail | Value |
|---------------|-------|
| Total Gesture Classes | **210** |
| Hand Landmark Points | **21** |
| Features per Frame | **63** |
| Frames per Gesture Sequence | **154** |
| Original Training Samples | **7,320** |
| Augmented Training Samples | **9,948** |
| Validation Samples | **630** |
| Test Samples | **420** |

### Data Augmentation

Controlled augmentation was applied to improve robustness while preserving gesture semantics.

Augmentation techniques include:

- Rotation
- Translation
- Scaling
- Gaussian Noise
- Temporal Shift
- Random Frame Dropout

Augmentation increased the effective training dataset without altering validation or test samples.

---

# 🧩 Transformer V5.2 Architecture

The final model uses a lightweight Transformer architecture optimized for landmark-based gesture recognition.

### Architecture Summary

- Input Shape: **(154, 63)**
- Dense Projection Layer
- 2 Transformer Encoder Blocks
- Multi-Head Self Attention
- Feed Forward Network
- Layer Normalization
- Residual Connections
- Global Average Pooling
- Dropout Regularization
- Dense Softmax Output (**210 classes**)

This architecture learns spatial and temporal relationships between hand landmark movements across the gesture sequence.

---

# 📈 Evaluation

The model was evaluated on an unseen test dataset.

### Confusion Matrix

![Confusion Matrix](outputs/confusion_matrix_v5_2.png)

### Evaluation Files

The repository includes detailed evaluation artifacts:

| File | Description |
|------|-------------|
| `outputs/confusion_matrix_v5_2.png` | Confusion Matrix visualization |
| `outputs/class_accuracy_v5_2.csv` | Per-class accuracy scores |
| `outputs/classification_report_v5_2.csv` | Precision, Recall and F1-score |
| `outputs/top15_confused_pairs_v5_2.csv` | Most frequently confused gesture pairs |
| `outputs/transformer_history_v5_2.pkl` | Training history |

---

# 📁 Project Structure

```text
SANKETSETU
│
├── assets/
│   └── banner.png
│
├── app/
│   ├── frontend/              # React UI (In Progress)
│   └── backend/               # Flask API (In Progress)
│
├── dataset/
│   ├── raw/
│   ├── processed/
│   └── training/
│
├── models/
│   ├── best_lstm_model.keras
│   ├── best_transformer_v4.keras
│   └── best_transformer_v5_2.keras      ⭐ Final Model
│
├── notebooks/
│   ├── 00_dataset_audit.ipynb
│   ├── 01_dataset_setup.ipynb
│   ├── 02_dataset_eda.ipynb
│   ├── 03_mediapipe_preprocessing.ipynb
│   ├── 04_build_dataset.ipynb
│   ├── 05_prepare_training_data.ipynb
│   ├── 06_train_lstm_model.ipynb
│   ├── 07_transformer_model.ipynb
│   ├── 08_model_evaluation.ipynb
│   ├── 09_transformer_v5_final.ipynb
│   └── 10_model_analysis_v5.ipynb
│
├── outputs/
│   ├── confusion_matrix_v5_2.png
│   ├── class_accuracy_v5_2.csv
│   ├── classification_report_v5_2.csv
│   ├── class_distribution.csv
│   ├── top15_confused_pairs_v5_2.csv
│   └── transformer_history_v5_2.pkl
│
├── src/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Future Scope

SanketSetu is designed to evolve into a complete accessibility ecosystem.

### Planned Features

- 🎥 Live webcam-based gesture detection.
- 📝 Real-time text translation.
- 🔊 Voice output for translated gestures.
- 🌍 Multilingual translation support.
- 📱 Responsive web application.
- 🤖 Larger real-world ISL dataset training.
- ☁️ Deployment using Flask API + React frontend.

---

# 🎨 Frontend Vision *(Currently Designing)*

The frontend is inspired by modern editorial interfaces with a calm, premium aesthetic.

**Design Direction**

- 🌙 Soft Dark Mode & Elegant Light Mode.
- 🎨 Dusty Peach, Sage Green, Lavender and Warm Beige gradients.
- ✨ Frosted glass cards with subtle blur.
- 🤍 Minimal typography with generous spacing.
- 📊 Real-time prediction cards and confidence indicators.
- 📷 Live webcam detection interface.
- 📚 Learn ISL module and gesture history.

The UI focuses on accessibility, simplicity and a modern user experience.

---

# 👩‍💻 Project Status

| Module | Status |
|--------|--------|
| Dataset Preparation | ✅ Completed |
| MediaPipe Landmark Extraction | ✅ Completed |
| Transformer V5.2 Training | ✅ Completed |
| Model Evaluation | ✅ Completed |
| Frontend Development | 🚧 In Progress |
| Backend API | 🚧 In Progress |
| Real-time Webcam Translation | 🚧 Planned |

---

# 🤍 Team

**Project Name:** SanketSetu

**Domain:** Artificial Intelligence • Deep Learning • Computer Vision

Developed as a college AI & Deep Learning project focused on building an accessible Indian Sign Language translation system using Transformer-based sequence learning.

---

<p align="center">
  <b>Bridging Hands. Building Understanding.</b><br>
  Made with 🤍 using TensorFlow, MediaPipe and Transformer V5.2.
</p>
