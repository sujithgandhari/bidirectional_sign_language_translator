# bidirectional_sign_language_translato
## 📌 About
An AI-powered system that recognizes American Sign Language (ASL) alphabet in real-time using computer vision and deep learning.

## ✨ Features
- Real-time hand gesture detection
- 26 alphabet signs recognition (A-Z)
- 95% accuracy with CNN model
- MediaPipe hand tracking
- OpenCV video processing

## 📁 Folder Structure
folder structure:
sign_language_project/
├── frontend/          ← your 3 HTML files (login & signup now wired!)
├── backend/
│   ├── main.py        ← start the server from here
│   ├── requirements.txt
│   ├── routes/
│   │   ├── auth.py    ← signup, login, JWT tokens
│   │   ├── predict.py ← sign-to-text prediction
│   │   └── tts.py     ← text-to-sign image lookup
│   ├── database/
│   │   ├── db.py      ← SQLite database setup
│   │   └── models.py  ← User table
│   └── static/signs/  ← put A.png, B.png … here later
└── ml_models/
    └── cnn_rfc.py     ← your MediaPipe + RFC classifier


## 🚀 Installation
```bash
git clone https://github.com/yourusername/sign-language-recognition.git
cd sign-language-recognition
pip install -r requirements.txt
```

## 💻 Usage
```bash
# Train the model
python train.py --epochs 50

# Run prediction
python predict.py --model models/best_model.pth

# Real-time detection
python main.py
```

## 🛠 Technologies
- **Language:** Python 3.9+
- **Frameworks:** PyTorch, TensorFlow
- **Computer Vision:** OpenCV, MediaPipe
- **Models:** CNN, RCF, Transformers
- **Libraries:** NumPy, Pandas, Matplotlib

## 📊 Performance
- **Accuracy:** 95.2%** on test dataset
- **Inference Time:** 0.05 seconds/frame

## 📸 Demo
![Demo](demo.gif)

## 🔮 Future Work
- [ ] Number recognition (0-9)
- [ ] Full sentence translation
- [ ] Mobile app integration

## 👨‍💻 Author
**Gandhari Sujith**  
GitHub: [@yourusername](https://github.com/yourusername)
