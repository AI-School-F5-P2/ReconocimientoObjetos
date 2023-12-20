import streamlit as st
from decouple import config
from video_processing.video_processing_YOLOv8 import download_video, process_video_with_model
from video_processing.video_processing_YOLOv8 import get_video_report, get_logo_report
from ultralytics import YOLO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json


#Function to check if the URL is a valid YouTube link
def valid_youtube_link(url):
    return "youtube.com" in url or "youtu.be" in url


def save_data_to_mongodb(info_dict):

   url = 'http://localhost:5000/upload_report'
   headers = {'Content-Type': 'application/json'}
   data_to_send = json.dumps(info_dict)
   
   try:
      response = requests.request('POST', url, data=data_to_send, headers=headers)
      
      if response.status_code == 200:
         st.success('Results successfully saved in MongoDB.')
      else:
         st.error(f'Error while saving the results in MongoDB. Status Code: {response.status_code}')
   
   except requests.RequestException as e:
      st.error(f'Error during the request to the server: {e}')


def main():
   st.title('Brand Logo Detection')

   video_url = st.text_input('Insert video URL')

   if video_url and valid_youtube_link(video_url):
      st.success("The link is valid.")
      st.video(video_url)
            
      if st.button(label=':sparkles::sparkles::sparkles::sparkles::sparkles: Get Report and Save in MongoDB :sparkles::sparkles::sparkles::sparkles::sparkles:',
                   type='primary', use_container_width=True):
         output_folder = config('VIDEO_FOLDER')
         video_filename = download_video(video_url, output_folder)
         video_path = f"{output_folder}/{video_filename}"
            
         model_path = config('YOLO_PATH')
         model = YOLO(model_path)
         labels_list = list(model.names.values())
         detected_labels = process_video_with_model(video_path, model)

         duration, frame_rate, info_dict = get_video_report(video_path, video_filename)
         info_dict['detections'] = get_logo_report(labels_list, detected_labels, duration, frame_rate)
         print(info_dict)

         st.title('Video')
         st.markdown(f"**Name:** {info_dict['video_filename']}")
         st.markdown(f"**Duration:** {info_dict['duration']:.2f} seconds")
         st.markdown(f"**Frame rate:** {info_dict['frame_rate']:.2f} fps")
         st.markdown(f"**Total frames:** {info_dict['total_frames']:.2f} frames")

         st.title('Detections')
         df = pd.DataFrame(info_dict['detections'])
         st.dataframe(df)

         plt.figure(figsize=(10, 6))
         barplot = sns.barplot(x='logo', y='total_detection_time_in_seconds', data=df, hue='logo')
         st.pyplot(barplot.figure)

         save_data_to_mongodb(info_dict)

   else:
      st.error("Please, enter a valid YouTube link.")


if __name__ == "__main__":
    main()