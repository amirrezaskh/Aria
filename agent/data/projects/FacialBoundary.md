# Facial Boundary and Facial Landmarks Detection using Convolutional Neural Networks

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.8+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

A comprehensive deep learning project that implements facial boundary detection and facial landmarks identification using Convolutional Neural Networks (CNNs). The system consists of two main components: an R-CNN model for face detection and a CNN model for 68-point facial landmark detection.

## 🎯 Overview

This project combines two powerful deep learning models to create a complete facial analysis pipeline:

1. **Facial Boundary Detection**: Uses an R-CNN architecture with VGG16 backbone to detect face bounding boxes in images
2. **Facial Landmarks Detection**: Employs a custom CNN to identify 68 facial landmarks within detected face regions

<div align="center">
  <img width="290" alt="Facial boundary detection example" src="https://user-images.githubusercontent.com/47675870/182039742-d0c66097-c88f-4e52-a5db-013a016d4e98.png">
  <img width="293" alt="Facial landmarks detection example" src="https://user-images.githubusercontent.com/47675870/182039785-bdcdc577-9ffc-43a1-b2a4-dcb1dc8a286a.png">
</div>

## ✨ Features

- **Multi-face Detection**: Detects multiple faces in a single image
- **High-precision Landmarks**: Identifies 68 facial landmarks per detected face
- **Real-time Processing**: Optimized for efficient inference
- **Pre-trained Models**: Ready-to-use models available for immediate deployment
- **Comprehensive Training Pipeline**: Complete training notebooks for both models
- **Visualization Tools**: Built-in functions for result visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- TensorFlow 2.8+
- OpenCV
- NumPy, Matplotlib, Pandas

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/amirrezaskh/Facial-Boundary-and-Facial-Landmarks-Detection-using-Convolutional-Neural-Networks.git
cd Facial-Boundary-and-Facial-Landmarks-Detection-using-Convolutional-Neural-Networks
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Download pre-trained models**:
   - [Pre-trained Models](https://drive.google.com/drive/folders/1c_ze_4aHxxI0RQVpwE_jqS4lbRs-5FD2?usp=sharing)
   - [Dataset](https://drive.google.com/file/d/1NFK3swEXOHFEsdIUT50PabBniTbJ-vNu/view?usp=sharing)

### Usage

The main usage interface is provided in `Facial_Boundary_and_Facial_Landmarks_Detection_Using_CNNs.ipynb`. This notebook demonstrates:

- Loading pre-trained models
- Processing input images
- Visualizing detection results
- End-to-end facial analysis pipeline

```python
import tensorflow as tf
import cv2
import numpy as np

# Load pre-trained models
rcnn_model = tf.keras.models.load_model("models/ieeercnn_vgg16.h5")
landmark_model = tf.keras.models.load_model("models/lm_det.h5")

# Process your image
image = cv2.imread("your_image.jpg")
# ... (see notebook for complete pipeline)
```

## 📁 Project Structure

```
├── Facial_Boundary_and_Facial_Landmarks_Detection_Using_CNNs.ipynb  # Main usage notebook
├── Part_1_RCNN.ipynb                                                # R-CNN training notebook  
├── Part_2_Facial_Landmarks_Detection.ipynb                          # Landmarks CNN training notebook
├── README.md                                                         # This file
├── INSTALLATION.md                                                   # Detailed installation guide
├── CONTRIBUTING.md                                                   # Contribution guidelines
├── LICENSE                                                           # MIT License
├── requirements.txt                                                  # Python dependencies
└── models/                                                          # Directory for pre-trained models
    ├── ieeercnn_vgg16.h5                                           # R-CNN model weights
    └── lm_det.h5                                                    # Landmarks detection model weights
```

## 🧠 Model Architecture

### 1. Facial Boundary Detection (R-CNN)
- **Backbone**: VGG16 (pre-trained on ImageNet)
- **Architecture**: R-CNN with custom classification head
- **Input**: RGB images of variable size
- **Output**: Face bounding boxes with confidence scores
- **Training**: Transfer learning approach with fine-tuning

### 2. Facial Landmarks Detection (CNN)
- **Architecture**: Custom CNN with multiple convolutional layers
- **Input**: Grayscale face images (256×256)
- **Output**: 68 facial landmark coordinates (x, y)
- **Features**: 
  - Conv2D layers with ReLU activation
  - MaxPooling for downsampling
  - Dense layers for coordinate regression
  - Dropout for regularization

## 🎓 Training

### Datasets
The project uses a custom dataset derived from the WIDER Face dataset, specifically prepared for facial boundary and landmarks detection tasks.

### Training Process

#### Part 1: R-CNN Training (`Part_1_RCNN.ipynb`)
- Data preprocessing and augmentation
- IoU calculation for bounding box evaluation
- Transfer learning from VGG16
- Custom loss functions for object detection
- Model evaluation and validation

#### Part 2: Landmarks Detection (`Part_2_Facial_Landmarks_Detection.ipynb`)
- Face region extraction and normalization
- 68-point landmark annotation processing
- CNN architecture design and training
- Coordinate regression optimization
- Performance evaluation metrics

### Training Features
- **Data Augmentation**: Random transformations to improve generalization
- **Early Stopping**: Prevents overfitting during training
- **Model Checkpointing**: Saves best performing models
- **Visualization**: Training progress and result visualization

## 📊 Performance

The models achieve competitive performance on facial detection and landmark identification tasks:

- **Face Detection**: High precision in multi-face scenarios
- **Landmark Accuracy**: Robust 68-point landmark detection
- **Processing Speed**: Optimized for real-time applications
- **Generalization**: Effective across diverse facial variations

## 🔧 Technical Details

### Dependencies
- **TensorFlow/Keras**: Deep learning framework
- **OpenCV**: Image processing and computer vision
- **NumPy**: Numerical computations
- **Matplotlib**: Visualization and plotting
- **Pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning utilities
- **tqdm**: Progress bars for training loops

## 🔗 Links

- **Colab Notebooks**:
  - [Part 1 - Facial Boundary Detection](https://colab.research.google.com/drive/1Xrq_DMWYPgOz0P8U6JP5EcnVbvTtPc9k?usp=sharing)
  - [Part 2 - Facial Landmarks Detection](https://colab.research.google.com/drive/1bjt13XIs5PddRa9JiB5nkbtCrr-RAqWt?usp=sharing)
- **Resources**:
  - [Pre-trained Models](https://drive.google.com/drive/folders/1c_ze_4aHxxI0RQVpwE_jqS4lbRs-5FD2?usp=sharing)
  - [Dataset](https://drive.google.com/file/d/1NFK3swEXOHFEsdIUT50PabBniTbJ-vNu/view?usp=sharing)


---

<div align="center">
  <strong>⭐ If this project helped you, please consider giving it a star! ⭐</strong>
</div>

