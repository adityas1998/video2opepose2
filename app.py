import gradio as gr
from controlnet_aux import OpenposeDetector
import os
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import *

openpose = OpenposeDetector.from_pretrained('lllyasviel/ControlNet')

def get_frames(video_in):
    frames = []
    #resize the video
    clip = VideoFileClip(video_in)
    
    #check fps
    if clip.fps > 30:
        print("vide rate is over 30, resetting to 30")
        clip_resized = clip.resize(height=512)
        clip_resized.write_videofile("video_resized.mp4", fps=30)
    else:
        print("video rate is OK")
        clip_resized = clip.resize(height=512)
        clip_resized.write_videofile("video_resized.mp4", fps=clip.fps)
    
    print("video resized to 512 height")
    
    # Opens the Video file with CV2
    cap= cv2.VideoCapture("video_resized.mp4")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("video fps: " + str(fps))
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('kang'+str(i)+'.jpg',frame)
        frames.append('kang'+str(i)+'.jpg')
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()
    print("broke the video into frames")
    
    return frames, fps

def get_openpose_filter(i):
    image = Image.open(i)
    
    #image = np.array(image)

    image = openpose(image)
    #image = Image.fromarray(image)
    # image.save("openpose_frame_" + str(i) + ".jpeg")
    # return "openpose_frame_" + str(i) + ".jpeg"
    return image

def create_video(frames, fps, type):
    print("building video result")
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(type + "_result.mp4", fps=fps)
    
    return type + "_result.mp4"

def convertG2V(imported_gif):
    clip = VideoFileClip(imported_gif.name)
    clip.write_videofile("my_gif_video.mp4")
    return "my_gif_video.mp4"

# def infer_skeleton_images(mmpose, frame_path, output_path = "temp"):
#     output_image_name = f"{os.path.split(frame_path)[-1].split('.')[0]}_pose.jpg"
#     # mmpose_frame = get_mmpose_filter(mmpose, frame)
#     image = mmpose(frame_path, fn_index=0)[1]
#     image = Image.open(image)
#     #image = Image.fromarray(image)
#     image.save(os.path.join(output_path, output_image_name))

# if __name__ == "__main__":
#     img_dir = "/home/adi/work/Dissertation/omnidata/omnidata_tools/torch/assets/extracted_frames_online_class"
#     # mmpose = gr.Interface.load(name="spaces/fffiloni/mmpose-estimation")
#     mmpose_client = Client("https://fffiloni/video2openpose2/")
#     for img_name in os.listdir(img_dir):
#         frame_path = os.path.join(img_dir, img_name)
#         infer_skeleton_images(mmpose, frame_path)

def infer(img_dir, output_path = "temp"):
    # img_dir = "/home/adi/work/Dissertation/omnidata/omnidata_tools/torch/assets/extracted_frames_online_class"
    # mmpose = gr.Interface.load(name="spaces/fffiloni/mmpose-estimation")
    # mmpose_client = Client("https://fffiloni/video2openpose2/")
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    for img_name in os.listdir(img_dir):
        frame_path = os.path.join(img_dir, img_name)
        output_image_name =  f"{img_name.split('.')[0]}_pose.jpg"
        frame_path = os.path.join(img_dir, img_name)
        openpose_frame = get_openpose_filter(frame_path)
        # image = Image.open(openpose_frame)
        openpose_frame.save(os.path.join(output_path, output_image_name))
        # result_frames.append(openpose_frame)
        # print("frame " + i + "/" + str(n_frame) + ": done;")

if __name__ == "__main__":
    infer(img_dir = "/data/scratch/ec23458/ubody_human_crops/", output_path = "/data/scratch/ec23458/ubody_human_crops_pose/")