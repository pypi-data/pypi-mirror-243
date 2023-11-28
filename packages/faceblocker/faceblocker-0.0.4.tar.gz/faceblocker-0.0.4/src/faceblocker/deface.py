#!./envs/bin/python
# Import everything needed to edit video clips
import moviepy
from moviepy.editor import *

import cv2 
from moviepy.video.tools.drawing import blit
import argparse

from pathlib import Path
import numpy as np
from importlib import resources
#
# Reads contents with UTF-8 encoding and returns str.
#eml = files('email.tests.data').joinpath('message.eml').read_text()
from . import models
import pdb

#eml = files(email.tests.data).joinpath('message.eml').read_text()
# def iter_test(vid_in,imagelist,samplerate=10,scalingfactor=0.2):
#     v_fps = vid_in.fps
#     if samplerate == None:
#         samplerate = vid_in.fps
    
#     clip_duration = vid_in.duration
#     n_frames = round(clip.fps*clip_duration)
#     timearray = np.linspace(0,clip_duration,round(n_frames/samplerate),endpoint=True) #adds 1 to size
#     chunk_counter = 0
#     for n_frame, time_frame in enumerate(vid_in.iter_frames(with_times=True,fps=v_fps)):
#         t,frame = time_frame[0],time_frame[1]
#         if t < timearray[chunk_counter]:
#             continue
        
#         else:        
#             print(n_frame,t,timearray[chunk_counter])
            
#             #newframe_scaled = cv2.resize(newframe, None, fx= scalingfactor, fy= scalingfactor, interpolation= cv2.INTER_LINEAR)            
#             superimposed = ImageClip(imagelist[0].as_posix()).resize(width=100)
#             superimposed.pos = lambda t: \
#                 (t % frame.shape[0] ,t % frame.shape[1])
#             superimposed.duration = timearray[chunk_counter+1]-t
#             newframe = superimposed.blit_on(newframe,t)
#             chunk_counter += 1
# #    absolute_mono_volume_array = np.fromiter(
# #        (absolute_mono_volume(frame) for
# #         frame in vid_in.audio.iter_chunks(fps=a_bitrate,chunksize=chunk_size)
# #         ),count=-1,dtype="float32")

#     return(vid_in)

def get_yunet_model_path():
    with resources.as_file(resources.files(models).joinpath("face_detection_yunet_2023mar.onnx")) as f:
        print(f)
        data_file_path = f
    return data_file_path



def detect_face_video_at_t(video,t,model,model_detection_lambda):
    faces = ()
    faces = model_detection_lambda(video.get_frame(t),model)
    return(faces)

def cliploop(vid_in,imagelist,model,model_detection_lambda,samplerate=10,scalingfactor=0.1,face_block_factor=1.5,save_detection_frames=False,blurflag=False):
    if samplerate == None:
        samplerate = vid_in.fps
    clip_duration = vid_in.duration
    nframes_lambda = lambda clip: round(clip.fps*clip.duration)
    n_frames = nframes_lambda(vid_in)
    working_vid = vid_in.resize(scalingfactor)
    timearray = np.linspace(0,clip_duration,round(n_frames/samplerate),endpoint=True) #adds 1 to size
    durationarray = np.array(
            [timearray[[i,i+1]] for i in np.arange(timearray.size-1)])
    #cliplist = [vid_in.subclip(t0,t1) for t0]
    working_cliplist = np.apply_along_axis(
            lambda timeslice: working_vid.subclip(timeslice[0],timeslice[1]),
        1,durationarray)
    cliplist = np.apply_along_axis(
            lambda timeslice: vid_in.subclip(timeslice[0],timeslice[1]),
        1,durationarray)
    finalcliplist = []
    for i,c in enumerate(working_cliplist):
        coords = detect_face_video_at_t(c,0,model,model_detection_lambda)
        c_out = cliplist[i].copy()
        if coords[1] is not None:
            facesdata = coords[1]
            for face_row in range(facesdata.shape[0]):
                this_face = (facesdata[face_row,:]*(1/scalingfactor)).astype("int32")
                nx,ny = this_face[8],this_face[9]
                facewidth = round(this_face[3]*face_block_factor)
                posx,posy = nx - facewidth/2, ny - facewidth/2
                print("frame {},time {} size{}*{}, face at {} ".format(i*samplerate,durationarray[i],cliplist[i].size,scalingfactor,(nx,ny)))
                if len(imagelist) >= 1:
                    superimposed = ImageClip(imagelist[face_row % len(imagelist)].as_posix()).resize(width=facewidth).set_position((posx,posy)) #has to be declared in the constructor due to pass by reference shenanigans
                else:
                    black_box = np.zeros((80,80,3))
                    superimposed = ImageClip(black_box).resize(width=facewidth).set_position((posx,posy))
                
                superimposed.duration = c.duration                
                c_out = CompositeVideoClip([c_out,superimposed])
                
                
        c_out.duration = c.duration
        c_out.fps = c.fps
        finalcliplist.append(c_out)
        if save_detection_frames == True:
            c_out.save_frame("detectionframe_" + str(i+1)+ ".png",t=0) #each clip has its own t
        #print([[cs.pos(1) for cs in c.clips] if hasattr(c,"clips") else c.pos(1) for c in finalcliplist])

    final_clip = concatenate_videoclips(finalcliplist,method="chain") #this is an upstream bug?
    #print(newcliplist)
    return(final_clip)



def main():
    print(__name__)
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', '-i', type=str, help='Path to the input video.')
    parser.add_argument('--pictures', '-p', type=str, default = [], action = "append", nargs="*", help='Path to pictures used to obscure faces.')
    parser.add_argument('--output_video', '-o', type=str, help='Path to the output video.')
    parser.add_argument('--scale', '-sc', type=float, default=0.4, help='Scale factor used to resize input video frames. Smaller is faster, but less accurate.')
    parser.add_argument('--score', type=float, default=0.3, help='Filtering out faces of score < score_threshold.')
    parser.add_argument('--nms_threshold', type=float, default=0.1, help='Suppress bounding boxes of iou >= nms_threshold.')
    parser.add_argument('--n_kboundboxes', type=int, default=1000, help='Keep top_k bounding boxes before NMS. Bigger is more accurate and slower. Smaller is less accurate and faster.')
    parser.add_argument('--samplerate', type=int, default=5, help='how often (in frames) should this scan for a face and paste an image over it? Higher is slower')
    parser.add_argument('--blockfactor', type=float, default=1.5, help='how much bigger should an image be than the detected facewidth? higher numbers (ie. >=1.5 for transparent images')
    parser.add_argument('--unstretch', type=bool, default=False, help='has moviepy made your vertical video horizontal and W I D E?  enable this flag to fix that and restore the original vertical size. ')

    #video, scale, score, nmsthld, n_kboundboxes = parser.parse_args("--video ./testdata/in/newyork.mp4".split())
    args = parser.parse_args()
    #args = parser.parse_args("-i /home/river/Videos/test_lsoh.mp4 -p /home/river/Pictures/fox_1f98a.png".split(" "))
    if args == None:
        print("AAAHHH")
    print(args)
    video = args.input
    output_video = args.output_video
    pictures = args.pictures
    scale = args.scale
    score = args.score
    nmsthld = args.nms_threshold
    n_kboundboxes = args.n_kboundboxes
    rate = args.samplerate
    blockfactor = args.blockfactor
    unstretch = args.unstretch
    input_path = Path(video)
    if type(output_video) != str:
        output_name = input_path.stem + str(hash(input_path.name)) + input_path.suffix
        output_path = Path(output_name)
    else:
        output_path = Path(output_video)
    print("saving output to", output_path.as_posix())
    threshold = 0.0001
    
    if len(pictures[0]) < 1 or pictures == None:
        image_path = []
        print("no images provided, black-blocking faces instead")
        blur_flag=True
    else:
        image_path = [Path(p) for p in args.pictures[0]]
    print("model found at ", get_yunet_model_path().as_posix())
    print("saving output to", output_path.as_posix())
    threshold = 0.0001
    # Load myHolidays.mp4 and select the subclip 00:00:50 - 00:00:60
    clip = VideoFileClip(input_path.as_posix())
    if unstretch == True:
        clip = clip.resize((clip.h,clip.w))
        print("clip unstretched!")
    detector = cv2.FaceDetectorYN.create(get_yunet_model_path().as_posix(),
                                         "",                                     
                                         [int(coord * scale) for coord in clip.size],
                                         score, #score threshold
                                         nmsthld, #nmsthreshold
                                         n_kboundboxes #top k bounding boxes
                                         )
    detector_detect_lambda = lambda frame,m: m.detect(frame)
    vid_out = cliploop(clip,image_path,detector,detector_detect_lambda,scalingfactor=scale,samplerate=rate,face_block_factor=blockfactor)
    #vid_out = clip
    #pdb.set_trace()
    # Write the result to a file (many options available !)
    vid_out.write_videofile(output_path.as_posix())
    return(0)

# if __name__ == "__main__":
#     main()
