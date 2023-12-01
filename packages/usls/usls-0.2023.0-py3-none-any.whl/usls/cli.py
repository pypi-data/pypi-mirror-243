import sys
import rich
import re
from omegaconf import OmegaConf, DictConfig
import argparse
from enum import Enum, auto, unique
from rich.panel import Panel
from typing import Dict, List, Union, Optional, Any


from usls import __version__
from usls.src.utils import (
	CONSOLE, IMG_FORMAT, LABEL_FORMAT, VIDEO_FORMAT, gen_emojis
)

from usls.src.labelling import run_marker
from usls.src.spider import run_spider
from usls.src.video_tools import run_play 

# ---------------------------------------------------------------------------------------------



def run(opt: DictConfig):
    task_mapping = {

        # not now
        'mark': run_marker,
        'spider': run_spider,
        'play': run_play,
    }.get(opt.task)(opt)





def cli() -> None:
	if len(sys.argv) == 1:
		sys.argv.append('-h')

	# CONSOLE.print(_logo)
	args = parse_cli()
	args.update({'task': sys.argv[1]})  # add task
	args = OmegaConf.create(args)
	
	# log
	CONSOLE.print(
		Panel(
			f"[b]{OmegaConf.to_yaml(args)}",
			# f"{args}",
			title='args',
			box=rich.box.ROUNDED,
		)
	)

	# run
	run(args) 	



def parse_cli() -> Dict:

	parser = argparse.ArgumentParser(
		prog='usls',
		description=gen_emojis(),
		epilog=f'version: {__version__} '
	)
	parser.add_argument(
		'--version', '-v', '-V', 
		action='version', 
		version=f'version: {__version__}',
		help='get version',
	)

	subparsers = parser.add_subparsers(
		# title='Tasks',
		description=gen_emojis(),
		help=gen_emojis()
	)


	# ---------------------
	# 	spider parser  ✅
	# ---------------------
	spider_parser = subparsers.add_parser(
		name='spider', 
		help=gen_emojis()
	)
	spider_parser.add_argument(
		'--words', 
		default='', nargs="+", required=True, type=str, 
		help='Key words'
	)
	spider_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='baidu-image-spider', help='baidu image spider output dir'
	)	



	# ---------------------------------
	# 	video play & record parser   ✅
	# ---------------------------------
	play_rec_parser = subparsers.add_parser(
		name='play', 
		help=gen_emojis()
	)
	play_rec_parser.add_argument(
		'--source', '--video', '-v',
		required=True, type=str, default=None, 
		help='Video source input'
	)
	play_rec_parser.add_argument(
		'--output-dir',
		required=False, type=str, default='video-records', 
		help='Saveout Directory'
	)	
	play_rec_parser.add_argument(
		'--delay',
		required=False, type=int, default=1, 
		help='Keywait'
	)	
	play_rec_parser.add_argument(
		'--fourcc',
		required=False, type=str, default='mp4v', 
		help='Image clipped format'
	)		
	play_rec_parser.add_argument(
		'--no-view',
		action='store_true',
		required=False, 
		help='Do not view while playing'
	)
	play_rec_parser.add_argument(
		'--rec',
		action='store_true',
		required=False, 
		help='Record at the start'
	)
	play_rec_parser.add_argument(
		'--flip',
		required=False, type=str, default=None,
		choices=['ud', 'lr', 'udlr', 'lrud'],
		help='Flipping video'
	)
	play_rec_parser.add_argument(
		'--rotate',
		required=False, type=int, default=None,
		choices=[90, 180, 270],
		help='Counterwise Rotation'
	)


	# ---------------------
	# 	inspect parser  ✅
	# ---------------------
	inspect_parser = subparsers.add_parser(
		name='mark', # aliases=['label-det'], 
		help=gen_emojis()
	)
	inspect_parser.add_argument(
		'--input', '-i',
		required=True, type=str, default=None, help='input dir'
	)
	inspect_parser.add_argument(
		'--classes', '-c', 
		default=None, nargs="+",
		 required=False, type=str, 
		 help='classes list'
	)
	inspect_parser.add_argument(
		'--kpts-classes', '-kc',
		default=None, nargs="+",
		 required=False, type=str, 
		 help='kpts classes list'
	)


	args = vars(parser.parse_args())
	return args




if __name__ == '__main__':
	cli()
