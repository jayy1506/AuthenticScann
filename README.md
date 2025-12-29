<<<<<<< HEAD
# AuthentiScan - AI Image Authenticity Detector

AuthentiScan is a full-stack web application that classifies user-uploaded images as either AI Generated or Original/Real using a DenseNet deep learning model.

## 🚀 Features

- **User Authentication**: Secure signup and login system
- **Image Analysis**: Classify images as AI-generated or original using DenseNet-121
- **Modern UI**: Responsive React frontend with Tailwind CSS
- **Secure Backend**: Flask API with proper error handling

## 🛠️ Tech Stack

### Backend
- **Python** with **Flask** (API server)
- **TensorFlow/Keras** with **DenseNet-121** (ML model)
- **SQLite** (User database)

### Frontend
- **React** (SPA framework)
- **Tailwind CSS** (Styling)
- **React Router** (Navigation)

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd authentiscan
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the project root directory and install frontend dependencies:
```bash
npm install
```

## ▶️ Running the Application

### Start the Backend Server

1. Make sure you're in the project root directory with the virtual environment activated
2. Run the Flask application:
```bash
python app.py
```
The backend server will start on `http://localhost:5000`

### Start the Frontend Development Server

1. In a new terminal window, navigate to the project root directory
2. Start the React development server:
```bash
npm start
```
The frontend will start on `http://localhost:3000`

## 🧠 Machine Learning Model

The application uses a DenseNet-121 model with transfer learning for image classification:

- **Base Model**: Pre-trained DenseNet-121 on ImageNet
- **Custom Layers**: GlobalAveragePooling2D + Dense(1, sigmoid) for binary classification
- **Input Size**: 224x224 RGB images
- **Preprocessing**: Image resizing and normalization to [0,1]

## 🔐 API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login

### Image Detection
- `POST /api/detect` - Analyze uploaded image (requires authentication)

## 📁 Project Structure

```
authentiscan/
├── app.py                        # Flask application entry point
├── auth.py                       # Authentication routes
├── detection.py                  # Image detection routes
├── ml_model.py                   # DenseNet model implementation
├── train_model.py                # Model training script
├── train_with_kaggle_dataset.py  # Training with Kaggle dataset
├── download_dataset.py           # Dataset download and organization
├── complete_training_pipeline.py # Complete training pipeline
├── robust_training_pipeline.py   # Robust training with error handling
├── simple_download.py           # Simple dataset download script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── public/                       # Static assets
│   └── index.html                # Main HTML template
└── src/                          # React frontend
    ├── components/               # React components
    │   ├── LandingPage.js
    │   ├── SignUp.js
    │   ├── Login.js
    │   └── Dashboard.js
    ├── App.js                    # Main App component
    ├── index.js                  # Entry point
    └── index.css                 # Global styles
```

## 🎨 User Flow

1. **Landing Page**: Introduction to AuthentiScan with signup/login options
2. **Sign Up**: Create a new account
3. **Log In**: Access your account
4. **Dashboard**: Upload images and analyze them
5. **Results**: View classification results (AI Generated vs Original)

## 🤖 Model Details

The DenseNet-121 model is configured as follows:
- Base model frozen (transfer learning)
- Enhanced classification head with dropout and batch normalization
- Image preprocessing (resize to 224x224, normalize)
- Binary classification output

### Improving Model Accuracy

To properly train the model for distinguishing AI-generated from real images:

1. **Dataset Preparation**:
   - Collect a balanced dataset of AI-generated and real images
   - Recommended size: 10,000+ images per class
   - Sources for real images: COCO, ImageNet, Flickr
   - Sources for AI-generated images: Midjourney, DALL-E, Stable Diffusion outputs

2. **Using the Kaggle Dataset**:
   - Download the "AI Generated Images vs Real Images" dataset from Kaggle:
     https://www.kaggle.com/datasets/cashbowman/ai-generated-images-vs-real-images
   - Extract the dataset
   - Run the training script: `python train_with_kaggle_dataset.py`
   - Provide the path to the extracted dataset when prompted

3. **Robust Training Pipeline**:
   - For a more robust approach, use: `python robust_training_pipeline.py`
   - This script includes error handling and automatic dataset organization
   - Handles corrupted downloads and provides fallback options

4. **Training Process**:
   - Fine-tune the top layers while keeping base model frozen initially
   - Use data augmentation (rotation, flips, brightness adjustments)
   - Apply transfer learning with ImageNet pre-trained weights
   - Train for 50+ epochs with early stopping

5. **Model Architecture Enhancements**:
   - Added BatchNormalization layers for stable training
   - Implemented Dropout layers to prevent overfitting
   - Used a lower learning rate (0.0001) for fine-tuning

6. **Enhanced Detection Logic**:
   - Improved thresholding to reduce false positives
   - Added heuristic analysis for uncertain predictions
   - Texture complexity analysis
   - Color distribution analysis
   - Noise pattern detection

7. **Evaluation Metrics**:
   - Monitor accuracy, precision, recall, and F1-score
   - Use validation set to prevent overfitting
   - Test on out-of-sample data for real-world performance

## 📝 Notes

- For production deployment, you would need to add proper authentication middleware
- The current implementation simulates the ML model since the actual trained weights aren't provided
- In a production environment, you would load the actual trained model weights
- To achieve high accuracy, proper training with a large dataset is essential
- The enhanced model includes dropout and batch normalization for better generalization

## 📄 License

This project is for educational purposes and demonstrates a full-stack application with machine learning integration.
=======
# AuthenticScann
"AI Generated Image Detector"
>>>>>>> f87ad9cb2f29b85aa0a95469592faec282a9ce6d
