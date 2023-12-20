from ultralytics import YOLO
import cv2
from pytube import YouTube
from decouple import config
import numpy as np
from collections import Counter


def download_video(youtube_url, output_path):
    '''
    Downloads a video from YouTube.
    Args:
        youtube_url (str): The YouTube video URL.
        output_path (str): The path to the folder where the video will be saved.
    Returns:
        str: The filename of the downloaded video.
    '''
    yt = YouTube(youtube_url)
    ys = yt.streams.get_highest_resolution()
    ys.download(output_path)
    return ys.default_filename


def process_video_with_model(video_path, model):
    '''
    Processes a video using a YOLOv8 model and displays real-time inference results.
    Args:
        video_path (str): The path to the video file.
        model: The YOLOv8 model object.
    Returns:
        detected_labels (list): A list of lists containing the detected labels for each frame.
    This function displays the video frames with the inference results 
    until the user presses 'q'.
    '''
    cap = cv2.VideoCapture(video_path)

    detected_labels = []

    #Loop through the video frames
    while cap.isOpened():
        #Read a frame from the video
        success, frame = cap.read()

        if success:
            #Run YOLOv8 inference on the frame
            results = model(frame, save_crop=True)

            #Detects the labels of the objects in the frame
            detected_labels.append(results[0].boxes.cls.tolist())

            #Visualize the results on the frame
            annotated_frame = results[0].plot()
            
            #Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            #Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            #Break the loop if the end of the video is reached
            break

    #Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

    return detected_labels


def get_video_report(video_path, video_filename):
    '''
    Gets basic information about the given video.
    Args:
        video_path (str): Path of the video file.
        video_filename (str): Name of the video file.
    Returns:
        duration (float): Duration of the video in seconds.
        frame_rate (float): Frames per second (fps) of the video.
        info_dict (dict): Dictionary with detailed information about the video, including:
        - 'video_filename' (str): Name of the video file.
        - 'duration' (float): Duration of the video in seconds.
        - 'total_frames' (int): Total number of frames in the video.
        - 'frame_rate' (float): Frames per second (fps) of the video.
    '''
    info_dict = {}

    cap = cv2.VideoCapture(video_path)

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / frame_rate

    info_dict['video_filename'] = video_filename
    info_dict['duration'] = duration
    info_dict['total_frames'] = total_frames
    info_dict['frame_rate'] = frame_rate

    cap.release()
    cv2.destroyAllWindows()

    return duration, frame_rate, info_dict


def get_logo_report(labels_list, detected_labels, duration, frame_rate):
    '''
    Generates a report (dictionary) of logo detections in a video.
    Args:
        labels_list (list): List of labels corresponding to the detected logos.
        detected_labels (list): List of lists containing detected logo labels.
        duration (float): Duration of the video in seconds.
        frame_rate (float): Frames per second (fps) of the video.
    Returns:
        list_of_dicts (list): List of dictionaries containing logo detection information, each dictionary includes:
        - 'logo' (str): Name of the detected logo.
        - 'number_of_detections_frames' (int): Number of frames where the logo was detected.
        - 'total_detection_time_in_seconds' (float): Total duration of logo detection in seconds.
        - 'percentage_of_video' (float): Percentage of the video duration covered by logo detection.
    '''

    list_of_dicts = []
    dict_logo_info = {}

    #Flatten the list of lists and convert the elements to int
    #to access later the 'labels list' with the detected numbers
    detected_labels_flat = np.concatenate(detected_labels).astype(int).tolist()

    #Counts the frequency of each label
    frequency = Counter(detected_labels_flat)

    for i, freq in frequency.items():
        dict_logo_info['logo'] = labels_list[i]
        dict_logo_info['number_of_detections_frames'] = freq
        dict_logo_info['total_detection_time_in_seconds'] = freq / frame_rate
        dict_logo_info['percentage_of_video'] = ((freq / frame_rate) / duration)*100
        list_of_dicts.append(dict_logo_info)
        dict_logo_info = {}
    
    return list_of_dicts


def main():

    youtube_url = 'https://www.youtube.com/watch?v=-qNOS_FfWNM'

    output_folder = config('VIDEO_FOLDER')
   
    video_filename = download_video(youtube_url, output_folder)

    video_path = f"{output_folder}/{video_filename}"

    model_path = config('YOLO_PATH')

    model = YOLO(model_path)

    labels_list = list(model.names.values())

    detected_labels = process_video_with_model(video_path, model)

    duration, frame_rate, info_dict = get_video_report(video_path, video_filename)

    info_dict['detections'] = get_logo_report(labels_list, detected_labels, duration, frame_rate)

    print(info_dict)


if __name__ == "__main__":
    main()