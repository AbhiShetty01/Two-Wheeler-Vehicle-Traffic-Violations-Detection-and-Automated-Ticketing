# Two-Wheeler Vehicle Traffic Violations Detection and Ticketing using YOLO Algorithm



## Introduction

This project aims to detect traffic violations by two-wheeler vehicles using the YOLO (You Only Look Once) object detection algorithm. Traffic violations such as helmet detection, wrong-side driving, and signal jumping by two-wheeler riders are automatically detected from video footage or live streams. Detected violations trigger automated ticketing or alerting mechanisms, aiding law enforcement in maintaining traffic discipline.

## Dataset

Describe the dataset used for training and testing the YOLO model. Include details such as:
- Source of the dataset (if publicly available or collected)
- Annotations or labels provided (e.g., helmet, wrong-side, signal jump)
- Number of images or videos used
- Data augmentation techniques applied (if any)

## Project Structure

- `data/`: Contains dataset files and annotations.
- `models/`: Includes trained YOLO models after training.
- `src/`: Source code for data preprocessing, model training, and detection.
- `videos/`: Directory to store input video footage for real-time or batch processing.

## Installation

To set up the project environment, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/AbhiShetty01/Two-Wheeler-Vehicle-Traffic-Violations-Detection.git
   cd Two-Wheeler-Vehicle-Traffic-Violations-Detection
   
## Technologies Used
Python: Programming language used for the project.
YOLO (You Only Look Once): Real-time object detection algorithm.
OpenCV: Computer vision library for image and video processing.
TensorFlow/Keras: Deep learning framework for model training and inference.
Evaluation
Describe the evaluation metrics used to assess the performance of the YOLO model for traffic violations detection. Include metrics such as precision, recall, and mean average precision (mAP) if applicable.

## Contributing
Contributions to improve the project are welcome! If you have suggestions, bug reports, or want to contribute code, please follow these guidelines:

Fork the repository and create your branch from main.
Ensure your code follows the project's coding style and conventions.
Make sure to test thoroughly before submitting a pull request.
