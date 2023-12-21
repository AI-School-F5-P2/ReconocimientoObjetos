# 🚀 Advertisement Logo Detection System

## Overview

This project addresses the needs of an advertising company seeking to assess the visibility of logos for the brands they represent in videos. The goal is to develop an intelligent system capable of detecting and analyzing brand logos in videos, providing detailed reports on the duration and percentage of time each logo appears. The system will also store these detections in a MongoDB database.

## Problem Statement

The advertising company wants to evaluate the effectiveness of their brand representation in videos and determine where to focus their advertising efforts. They have enlisted two AI experts (us) to create a logo detection model to analyze videos and generate comprehensive reports on logo appearances.

## Solution

In less than two weeks, we have successfully implemented a proof-of-concept solution using two state-of-the-art AI models: DETR (including transformers) and YOLOv8. The models were trained on a dataset from Roboflow, consisting of over 4000 images. To keep the proof of concept flexible, we allow the selection of logos for detection.

## Features

- **Logo Detection Models:**
  - Utilized both DETR with transformers and YOLOv8 for logo detection.
  - Trained on a diverse dataset obtained from Roboflow.

- **Streamlit Interface:**
  - Developed a user-friendly interface using Streamlit.
  - Users provide a YouTube video link, and the system generates a detailed report on detected brands and their durations.

- **Real-time Detection:**
  - Near real-time display of logo detections with corresponding labels and confidence percentages.

- **Report Generation:**
  - Detailed reports include the duration and percentage of time each brand logo appears in the video.

- **MongoDB Integration:**
  - All detection data is stored in a MongoDB database for future analysis.

## Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/AI-School-F5-P2/ReconocimientoObjetos.git
    cd your_repo
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Streamlit app:**

    ```bash
    streamlit run str_app.py
    ```

4. **Access the Streamlit app in your browser and provide a YouTube video link for analysis.**

## Description of Files

- **notebooks/:**
  - `DETR_COCO_format_cars.ipynb`: Notebook for training the DETR model with a COCO format dataset.
  - `YOLOV8_cars.ipynb`: Notebook for training the YOLOv8 model.

- **mongo_database/:**
  - `mongo.py`: Python file establishing connection with MongoDB.

- **video_processing/:**
  - `video_processing_DETR.py`: Functions for processing videos with the DETR model.
  - `video_processing_YOLOv8.py`: Functions for processing videos with the YOLOv8 model.

- **str_app.py:** Python file with the code for the Streamlit application user interface.

- **requirements.txt:** List of project dependencies.

- **README.md:** Main project documentation.

## Future Enhancements

- **Expand Logo Selection:**
  - Allow users to choose from an expanding list of logos for detection.

- **Improve Training Data:**
  - Continuously enhance the models by incorporating more diverse and extensive training datasets.

- **Enhance User Interface:**
  - Improve the aesthetics and functionality of the Streamlit interface.

- **Real-time Video Analysis:**
  - Explore options for real-time video analysis to meet potential future requirements.

## Contributors

- [Alexa Montenegro](https://www.linkedin.com/in/alexa-montenegro-047b3a252/)
- [Ana Gómez](https://www.linkedin.com/in/ana-milena-gomez-giraldo/)

## Acknowledgments

We would like to express our gratitude to the Bootcamp we are part of for providing this opportunity to develop and showcase our logo detection system.

Feel free to contribute to this project by forking and submitting pull requests. Thank you for your interest!