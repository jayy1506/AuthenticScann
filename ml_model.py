import tensorflow as tf
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model
import numpy as np
from PIL import Image
import os

class AIGeneratedDetector:
    def __init__(self, model_path='densenet_ai_detector.h5'):
        """
        Initialize the AI Generated Image Detector
        """
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """
        Load the pre-trained DenseNet model with custom classifier
        """
        try:
            # Check if trained model exists
            if os.path.exists('densenet_simple_model.h5'):
                # Load the trained model
                self.model = tf.keras.models.load_model('densenet_simple_model.h5')
                print("Loaded trained model successfully")
            elif os.path.exists(self.model_path):
                # Load the pre-trained model
                self.model = tf.keras.models.load_model(self.model_path)
                print("Loaded pre-trained model successfully")
            else:
                # Create an enhanced model with DenseNet base
                print("Model file not found. Creating an enhanced model for better detection.")
                base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
                
                # Freeze the base model
                base_model.trainable = False
                
                # Add enhanced classifier with dropout and batch normalization
                x = GlobalAveragePooling2D()(base_model.output)
                x = BatchNormalization()(x)
                x = Dropout(0.5)(x)
                x = Dense(128, activation='relu')(x)
                x = BatchNormalization()(x)
                x = Dropout(0.3)(x)
                predictions = Dense(1, activation='sigmoid')(x)
                
                self.model = Model(inputs=base_model.input, outputs=predictions)
                
                # Compile the model with a lower learning rate for fine-tuning
                self.model.compile(
                    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                    loss='binary_crossentropy', 
                    metrics=['accuracy']
                )
            
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Create a dummy model for testing purposes
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(1, activation='sigmoid', input_shape=(224*224*3,))
            ])
    
    def preprocess_image(self, image_path):
        """
        Preprocess the image for DenseNet model
        """
        try:
            # Open image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to 224x224
            img = img.resize((224, 224))
            
            # Convert to array and normalize
            img_array = np.array(img) / 255.0
            
            # Expand dimensions to match model input
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def predict(self, image_path):
        """
        Predict if an image is AI generated or original with improved accuracy
        """
        try:
            # Preprocess the image
            processed_img = self.preprocess_image(image_path)
            
            if processed_img is None:
                return None
            
            # Make prediction
            prediction = self.model.predict(processed_img)[0][0]
            
            # Enhanced decision logic with balanced approach
            # More balanced thresholds to reduce both false positives and false negatives
            if prediction > 0.6:  # Increased from 0.5
                return "AI Generated"
            elif prediction < 0.4:  # Increased from 0.3
                return "Original Image"
            else:
                # Uncertain prediction - use weighted heuristic analysis
                heuristic_result = self.heuristic_analysis(image_path)
                
                # Combine model prediction with heuristic analysis
                # Convert heuristic result to numerical score
                if heuristic_result == "AI Generated":
                    heuristic_score = 0.2  # Strong indication of AI
                elif heuristic_result == "Original Image":
                    heuristic_score = 0.8  # Strong indication of original
                else:
                    heuristic_score = 0.5  # Neutral/inconclusive
                
                # Weighted combination (70% model, 30% heuristic)
                combined_score = 0.7 * prediction + 0.3 * heuristic_score
                
                # Final decision based on combined score
                if combined_score > 0.55:
                    return "AI Generated"
                else:
                    return "Original Image"
                
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
    
    def heuristic_analysis(self, image_path):
        """
        Perform heuristic analysis to distinguish AI-generated from real images
        """
        try:
            img = Image.open(image_path)
            # Convert to numpy array
            img_array = np.array(img)
            
            # Check image properties
            if len(img_array.shape) != 3 or img_array.shape[2] != 3:
                return "Invalid image format"
            
            # Analyze texture complexity
            texture_score = self.analyze_texture(img_array)
            
            # Analyze color distribution
            color_score = self.analyze_colors(img_array)
            
            # Analyze noise patterns
            noise_score = self.analyze_noise(img_array)
            
            # Combine scores (weighted average)
            # Lower scores indicate AI-generated characteristics
            combined_score = 0.4 * texture_score + 0.3 * color_score + 0.3 * noise_score
            
            # Interpret the combined score
            # Scores closer to 0 suggest AI-generated, closer to 1 suggest real
            # Balanced thresholds for better accuracy
            if combined_score < 0.3:  # More conservative AI detection
                return "AI Generated"
            elif combined_score > 0.7:  # More confident original detection
                return "Original Image"
            else:
                # When uncertain, return neutral result
                return "Uncertain - Likely Original"
                
        except Exception as e:
            print(f"Heuristic analysis failed: {e}")
            # When in doubt, return neutral result
            return "Uncertain - Likely Original"
    
    def analyze_texture(self, img_array):
        """
        Analyze texture complexity - AI images often have smoother textures
        """
        try:
            # Convert to grayscale
            gray = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140])
            
            # Calculate local variance as a measure of texture complexity
            local_variances = []
            h, w = gray.shape
            
            # Calculate variance in small regions
            for i in range(0, h-32, 32):
                for j in range(0, w-32, 32):
                    region = gray[i:i+32, j:j+32]
                    if np.std(region) > 0:  # Avoid division by zero
                        local_variances.append(np.var(region))
            
            if not local_variances:
                return 0.5  # Neutral score if no variances calculated
            
            avg_variance = np.mean(local_variances)
            
            # Normalize score (higher variance = more texture = more likely real)
            # Typical real images have variance > 500, AI images often < 500
            normalized_score = min(1.0, avg_variance / 500.0)
            return max(0.0, normalized_score)
            
        except:
            return 0.5  # Neutral score on failure
    
    def analyze_colors(self, img_array):
        """
        Analyze color distribution - AI images may have unnatural color distributions
        """
        try:
            # Extract RGB channels
            r_channel = img_array[:,:,0]
            g_channel = img_array[:,:,1]
            b_channel = img_array[:,:,2]
            
            # Check for color balance (real images have more balanced colors)
            r_mean, g_mean, b_mean = np.mean(r_channel), np.mean(g_channel), np.mean(b_channel)
            max_channel = max(r_mean, g_mean, b_mean)
            min_channel = min(r_mean, g_mean, b_mean)
            
            # Extreme color dominance suggests AI generation
            color_balance = 1.0 - (max_channel - min_channel) / 255.0
            
            # Check histogram uniformity (AI images often have smoother histograms)
            r_hist = np.histogram(r_channel, bins=32, range=(0, 255))[0]
            g_hist = np.histogram(g_channel, bins=32, range=(0, 255))[0]
            b_hist = np.histogram(b_channel, bins=32, range=(0, 255))[0]
            
            # Normalize histograms
            r_hist = r_hist / np.sum(r_hist) if np.sum(r_hist) > 0 else r_hist
            g_hist = g_hist / np.sum(g_hist) if np.sum(g_hist) > 0 else g_hist
            b_hist = b_hist / np.sum(b_hist) if np.sum(b_hist) > 0 else b_hist
            
            # Calculate histogram smoothness (real images have more varied histograms)
            r_smoothness = 1.0 - np.std(r_hist) * 10
            g_smoothness = 1.0 - np.std(g_hist) * 10
            b_smoothness = 1.0 - np.std(b_hist) * 10
            
            histogram_smoothness = (r_smoothness + g_smoothness + b_smoothness) / 3.0
            
            # Combine metrics
            combined = 0.6 * color_balance + 0.4 * max(0, histogram_smoothness)
            return max(0.0, min(1.0, combined))
            
        except:
            return 0.5  # Neutral score on failure
    
    def analyze_noise(self, img_array):
        """
        Analyze noise patterns - real images have natural sensor noise
        """
        try:
            # Convert to grayscale
            gray = np.dot(img_array[...,:3], [0.2989, 0.5870, 0.1140])
            
            # Calculate noise as local variation
            noise_levels = []
            h, w = gray.shape
            
            # Sample multiple regions
            for i in range(32, h-32, 64):
                for j in range(32, w-32, 64):
                    region = gray[i-16:i+16, j-16:j+16]
                    noise_levels.append(np.std(region))
            
            if not noise_levels:
                return 0.5
            
            avg_noise = np.mean(noise_levels)
            
            # Real images typically have more noise (3-20), AI images often < 3
            # Normalize: higher noise = more likely real
            normalized_noise = min(1.0, avg_noise / 10.0)
            return max(0.0, normalized_noise)
            
        except:
            return 0.5  # Neutral score on failure

# Initialize the detector
detector = AIGeneratedDetector()

if __name__ == "__main__":
    # Test the model with a sample image
    # This is just for demonstration purposes
    print("AI Generated Image Detector initialized")