import cv2
from pytube import YouTube
from transformers import DetrForObjectDetection, DetrImageProcessor
import supervision as sv
import torch
from decouple import config


def get_model_and_image_processor():
    '''
    Retrieves the DETR image processor and the model trained with the custom dataset.
    Returns:
        Tuple[DetrImageProcessor, DetrForObjectDetection]: A tuple containing the DETR image processor and model.
    '''    
    MODEL_PATH = config('MODEL_PATH')
    CHECKPOINT = 'facebook/detr-resnet-50'

    image_processor = DetrImageProcessor.from_pretrained(CHECKPOINT)
    model = DetrForObjectDetection.from_pretrained(MODEL_PATH)
    return image_processor, model


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


def process_video_with_model(video_path, image_processor, model):
    '''
    Processes a video using a DETR model and displays real-time object detection results.
    Args:
        video_path (str): The path to the video file.
        image_processor: The DETR image processor.
        model: The pretrained DETR model for object detection.
    Returns:
        None
    '''
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    frames_to_skip = 50

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        #Skips frames to speed up inference
        frame_count += 1
        if frame_count % (frames_to_skip + 1) != 0:
            continue
        
        #Process the frame with DETR and obtain detections
        with torch.no_grad():
            
            inputs = image_processor(images=frame, return_tensors='pt')
            outputs = model(**inputs)
            
            #Post-process
            target_sizes = torch.tensor([frame.shape[:2]])
            results = image_processor.post_process_object_detection(outputs=outputs,
                                                                    threshold=0.40,
                                                                    target_sizes=target_sizes)[0]


            #Draw the detections on the frame
            detections = sv.Detections.from_transformers(transformers_results=results)
            labels = [f"{model.config.id2label[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in detections]

            box_annotator = sv.BoxAnnotator()
            
            annotated_frame = box_annotator.annotate(scene=frame, detections=detections, labels=labels)
            
            #Display the frame with detections
            cv2.imshow('Detected Objects', annotated_frame)

            #Wait for a key press or a short delay
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def main():

    youtube_url = 'https://www.youtube.com/watch?v=G_-B8fPkgb0'

    output_folder = config('VIDEO_FOLDER')

    video_filename = download_video(youtube_url, output_folder)

    video_path = f"{output_folder}/{video_filename}"

    image_processor, model = get_model_and_image_processor()   

    process_video_with_model(video_path, image_processor, model)


if __name__ == "__main__":
    main()
