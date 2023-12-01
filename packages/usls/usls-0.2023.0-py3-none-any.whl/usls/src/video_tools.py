import cv2
import os
import rich
from tqdm import tqdm
import argparse
from pathlib import Path
import sys
from omegaconf import OmegaConf, DictConfig
from datetime import datetime

from usls.src.utils import CONSOLE, IMG_FORMAT, VIDEO_FORMAT, LABEL_FORMAT, smart_path



def play_and_record(
        source,
        delay=1, 
        flip=None,
        rotate=None,
        view=True,
        fourcc='mp4v',
        record=False,
        output_dir=None,
    ):
    # video play & record

    # check file
    if Path(source).is_file():
        # raise TypeError(f"{source} is not a valid file.")
        # sys.exit()
        
        # check format
        if not Path(source).suffix in VIDEO_FORMAT:
            raise TypeError(f"{source} is supported video format: {VIDEO_FORMAT}.")
            sys.exit()



    CONSOLE.print(f"Source: {Path(source).resolve()}")


    # flip and rotate
    if flip:
        if flip == 'ud':
            flipCode = 0
        elif flip == 'lr':
            flipCode = 1
        elif flip in('udlr', 'lrud'):
            flipCode = -1


    if rotate:
        if rotate == 90:
            rotateCode = cv2.ROTATE_90_CLOCKWISE
        elif rotate == 180:
            rotateCode = cv2.ROTATE_180
        elif rotate == 270:
            rotateCode = cv2.ROTATE_90_COUNTERCLOCKWISE


    videoCapture = cv2.VideoCapture(source)  # video capture
    fps = int(videoCapture.get(cv2.CAP_PROP_FPS))
    w = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # video_size = (w, h)
    # fourcc_ = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc_ = cv2.VideoWriter_fourcc(*fourcc)
    CONSOLE.print(f"Info: width={w}, height={h}, fps={fps}, fourcc={fourcc_}")


    # record flag
    do_rec = record

    # rec 
    if do_rec:
        CONSOLE.print(f"Rec...")
        save_dir = smart_path(
            Path(output_dir) / datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 
            exist_ok=False, 
            sep='-'
        )  # increment dir
        save_dir.mkdir(parents=True, exist_ok=True)
        saveout = save_dir / 'rec.mp4' 
        video_writer = cv2.VideoWriter(str(saveout), fourcc_, fps, (w, h))  # build video writer


    while True:
        ret, frame = videoCapture.read()
        if ret:

            if flip:
                frame = cv2.flip(frame, flipCode)
            if rotate:
                frame = cv2.rotate(frame, rotateCode)
            if view:
                frame_s = frame
 
                cv2.imshow('frame', frame_s)
            
            # rec
            if do_rec:
                video_writer.write(frame)

            # key detect
            key = cv2.waitKey(delay)

            # esc -> quit
            if key == 27:

                if do_rec:    
                    CONSOLE.print(f"Record saved at: {saveout.resolve()}")

                break

            # r -> record
            if key == ord('r'):
                do_rec = not do_rec   # ~  

                # rec 
                if do_rec:
                    CONSOLE.print(f"Rec...")

                    save_dir = smart_path(
                        Path(output_dir) / datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), 
                        exist_ok=False, 
                        sep='-'
                    )  # increment dir
                    save_dir.mkdir(parents=True, exist_ok=True)
                    saveout = save_dir / 'rec.mp4' 
                    video_writer = cv2.VideoWriter(str(saveout), fourcc_, fps, (w, h))

                else:
                    CONSOLE.print(f"Record saved at: {saveout.resolve()}")
        else:
            break


    # release cap & video cap
    videoCapture.release()
    if view:
        cv2.destroyAllWindows()




def run_play(args: DictConfig):
    with CONSOLE.status("[green]Playing...\n") as status:

        play_and_record(
            source=args.source,
            delay=args.delay, 
            flip=args.flip,
            rotate=args.rotate,
            view=not args.no_view,
            fourcc=args.fourcc,
            record=args.rec,
            output_dir=args.output_dir,
        )



