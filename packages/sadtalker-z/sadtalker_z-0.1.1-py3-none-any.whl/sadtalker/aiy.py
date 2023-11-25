import shutil
import torch
from time import  strftime
import os, sys

from sadtalker.utils.preprocess import CropAndExtract
from sadtalker.test_audio2coeff import Audio2Coeff  
from sadtalker.facerender.animate import AnimateFromCoeff
from sadtalker.generate_batch import get_data
from sadtalker.generate_facerender_batch import get_facerender_data
from sadtalker.utils.init_path import init_path

import typing
import time

from aiy_log import logger
from aiy_scheduler import Task

import subprocess

def convert_video(video_input, video_output):
    subprocess.run(f"ffmpeg -i {video_input} -c:v libx264 -c:a aac {video_output}".split(' '))

class SadTalkerTask(Task):
    source_image: str
    drive_audio: str

    def __init__(self, image_path: str, audio_path: str) -> None:
        self.source_image = image_path
        self.drive_audio = audio_path
        super().__init__()

    def run(self):
        # generate mp4 by sadtalker
        args = SadTalkerArgs(self.drive_audio, self.source_image, preprocess='full', filename=self.id)
        gen_sad_talker(args)

class SadTalkerArgs:
    source_image: str
    driven_audio: str
    ref_eyeblink: str | None
    ref_pose: str | None
    checkpoint_dir: str
    result_dir: str
    pose_style: int
    batch_size: int
    size: int
    expression_scale: float
    input_yaw: typing.List[int] | None
    input_pitch: typing.List[int] | None
    input_roll: typing.List[int] | None
    enhancer: str | None
    background_enhancer: str | None
    cpu: bool
    face3dvis: bool
    still: bool
    # ['crop', 'extcrop', 'resize', 'full', 'extfull']
    preprocess: str
    verbose: bool
    old_version: bool
    device: str

    # net structure and parameters
    net_recon: str
    init_path: str
    use_last_fc: bool
    bfm_folder: str
    bfm_model: str

    # default renderer parameters
    focal: float
    center: float
    camera_d: float
    z_near: float
    z_far: float

    # filename
    filename: str | None

    def __init__(self, driven_audio, source_image, preprocess: str = 'crop', filename: str | None = None):
        self.device = 'cpu'
        self.driven_audio = driven_audio
        self.source_image = source_image
        self.ref_eyeblink = None
        self.ref_pose = None
        self.checkpoint_dir = './checkpoints'
        self.result_dir = './results'
        self.pose_style = 0
        self.batch_size = 2
        self.size = 256
        self.expression_scale = 1.
        self.input_yaw = None
        self.input_pitch = None
        self.input_roll = None
        self.enhancer = None
        self.background_enhancer = None
        self.cpu = False
        self.face3dvis = False
        self.still = True
        self.preprocess = preprocess
        self.verbose = False
        self.old_version = False

        # net structure and parameters
        self.net_recon = "resnet50"
        self.init_path = None
        self.use_last_fc = False
        self.bfm_folder = './checkpoints/BFM_Fitting/'
        self.bfm_model = 'BFM_model_front.mat'
        # default renderer parameters
        self.focal = 1015.
        self.center = 112.
        self.camera_d = 10.
        self.z_near = 5.
        self.z_far = 15.

        self.filename = filename

def gen_sad_talker(args: SadTalkerArgs):
    logger.info('Start to generate sad-talker video')
    pic_path = args.source_image
    audio_path = args.driven_audio
    filename = strftime("%Y_%m_%d_%H.%M.%S") if args.filename is None else args.filename
    save_dir = os.path.join(args.result_dir, filename)
    os.makedirs(save_dir, exist_ok=True)
    pose_style = args.pose_style
    device = args.device
    batch_size = args.batch_size
    input_yaw_list = args.input_yaw
    input_pitch_list = args.input_pitch
    input_roll_list = args.input_roll
    ref_eyeblink = args.ref_eyeblink
    ref_pose = args.ref_pose

    current_root_path = os.path.split(sys.argv[0])[0]

    sadtalker_paths = init_path(args.checkpoint_dir, os.path.join(current_root_path, 'sadtalker/config'), args.size, args.old_version, args.preprocess)

    #init model
    preprocess_model = CropAndExtract(sadtalker_paths, device)
    audio_to_coeff = Audio2Coeff(sadtalker_paths,  device)
    animate_from_coeff = AnimateFromCoeff(sadtalker_paths, device)

    #crop image and extract 3dmm from image
    first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
    os.makedirs(first_frame_dir, exist_ok=True)
    logger.info('3DMM Extraction for source image')
    first_coeff_path, crop_pic_path, crop_info =  preprocess_model.generate(pic_path, first_frame_dir, args.preprocess,\
                                                                             source_image_flag=True, pic_size=args.size)
    if first_coeff_path is None:
        print("Can't get the coeffs of the input")
        return

    if ref_eyeblink is not None:
        ref_eyeblink_videoname = os.path.splitext(os.path.split(ref_eyeblink)[-1])[0]
        ref_eyeblink_frame_dir = os.path.join(save_dir, ref_eyeblink_videoname)
        os.makedirs(ref_eyeblink_frame_dir, exist_ok=True)
        logger.info('3DMM Extraction for the reference video providing eye blinking')
        ref_eyeblink_coeff_path, _, _ =  preprocess_model.generate(ref_eyeblink, ref_eyeblink_frame_dir, args.preprocess, source_image_flag=False)
    else:
        ref_eyeblink_coeff_path=None

    if ref_pose is not None:
        if ref_pose == ref_eyeblink: 
            ref_pose_coeff_path = ref_eyeblink_coeff_path
        else:
            ref_pose_videoname = os.path.splitext(os.path.split(ref_pose)[-1])[0]
            ref_pose_frame_dir = os.path.join(save_dir, ref_pose_videoname)
            os.makedirs(ref_pose_frame_dir, exist_ok=True)
            logger.info('3DMM Extraction for the reference video providing pose')
            ref_pose_coeff_path, _, _ =  preprocess_model.generate(ref_pose, ref_pose_frame_dir, args.preprocess, source_image_flag=False)
    else:
        ref_pose_coeff_path=None

    #audio2ceoff
    batch = get_data(first_coeff_path, audio_path, device, ref_eyeblink_coeff_path, still=args.still)
    coeff_path = audio_to_coeff.generate(batch, save_dir, pose_style, ref_pose_coeff_path)

    # 3dface render
    if args.face3dvis:
        from sadtalker.face3d.visualize import gen_composed_video
        gen_composed_video(args, device, first_coeff_path, coeff_path, audio_path, os.path.join(save_dir, '3dface.mp4'))
    
    #coeff2video
    data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path, 
                                batch_size, input_yaw_list, input_pitch_list, input_roll_list,
                                expression_scale=args.expression_scale, still_mode=args.still, preprocess=args.preprocess, size=args.size)
    
    result = animate_from_coeff.generate(data, save_dir, pic_path, crop_info, \
                                enhancer=args.enhancer, background_enhancer=args.background_enhancer, preprocess=args.preprocess, img_size=args.size)
    
    video_path = save_dir+'.mp4'
    shutil.move(result, video_path)
    logger.info('The generated video is named:' + video_path)

    if not args.verbose:
        shutil.rmtree(save_dir)

    time.sleep(1)

    # 不做此转换，则不能在 HTML 中播放
    # https://stackoverflow.com/questions/59670331/converting-mp4-aac-to-avc-using-python
    video_path_avc = video_path + '.avc.mp4'
    convert_video(video_path, video_path_avc)
    os.remove(video_path)
    os.rename(video_path_avc, video_path)

    logger.info(f'Generate {video_path}')
