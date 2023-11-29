import pandas as pd
import os, glob
import numpy as np
import pickle
import cv2
import itertools

from simba.mixins.geometry_mixin import GeometryMixin
from simba.utils.read_write import get_fn_ext, get_video_meta_data
from simba.utils.enums import Formats
from simba.utils.lookups import get_color_dict

PROJECT_DIR = '/Users/simon/Desktop/envs/troubleshooting/ARES_data/Termite Test/project'
SHAPES_DIR = os.path.join(PROJECT_DIR, 'project_data/shapes')
FPS = 25


TRACK_COL = 'track'
FRAME_COL = 'frame_idx'
SCORE_SUFFIX = 'score'
COLORS = list(get_color_dict().values())[5:]

#CREATE SHAPES
BUFFER_PX = 20
for file_path in glob.glob(os.path.join(PROJECT_DIR, 'input_data') + '/*.csv'):
    video_name = get_fn_ext(filepath=file_path)[1]
    df = pd.read_csv(file_path).head(500).fillna(0)
    score_cols = [c for c in df.columns if c.endswith(f'.{SCORE_SUFFIX}')]
    score_df = df[score_cols]
    track_frm_df = df[[TRACK_COL, FRAME_COL]]
    df = df.drop(score_cols + [TRACK_COL, FRAME_COL], axis=1).astype(np.int32)
    data = df.values.reshape(len(df), -1, 2)
    shapes = GeometryMixin().multiframe_bodyparts_to_polygon(data=data, parallel_offset=BUFFER_PX, video_name=video_name)
    track_frm_df['shape'] = GeometryMixin().multiframe_minimum_rotated_rectangle(shapes=shapes, video_name=video_name)
    shapes = {}
    for track in track_frm_df[TRACK_COL].unique():
        shapes[track] = list(track_frm_df[track_frm_df[TRACK_COL] == track].drop(TRACK_COL, axis=1).set_index(FRAME_COL).to_dict().values())[0]
    with open(os.path.join(SHAPES_DIR, f'{video_name}.pickle'), 'wb') as h:
        pickle.dump(shapes, h, protocol=pickle.HIGHEST_PROTOCOL)

#VISUALIZE SHAPES
# VIDEO_NAME = 'Termite Test'
# with open(os.path.join(SHAPES_DIR, f'{VIDEO_NAME}.pickle'), 'rb') as handle:
#     shapes = pickle.load(handle)
# fourcc = cv2.VideoWriter_fourcc(*Formats.MP4_CODEC.value)
# video_input_path = os.path.join(PROJECT_DIR, 'videos', f'{VIDEO_NAME}.mp4')
# video_output_path = os.path.join(PROJECT_DIR, 'project_data/videos', f'{VIDEO_NAME}.mp4')
# video_meta_data = get_video_meta_data(video_path=video_input_path)
# writer = cv2.VideoWriter(video_output_path, fourcc, video_meta_data['fps'], (video_meta_data['width'], video_meta_data['height']))
# cap = cv2.VideoCapture(video_input_path)
#
# frm_cnt = 0
# while (cap.isOpened()):
#     ret, img = cap.read()
#     try:
#         for trk_cnt, trk in enumerate(shapes.keys()):
#             cv2.polylines(img, [np.array(shapes[trk][frm_cnt].exterior.coords).astype(np.int64)], True, COLORS[trk_cnt][::-1], 2)
#         writer.write(img.astype(np.uint8))
#         frm_cnt += 1; print(frm_cnt)
#     except:
#         break
# cap.release();  writer.release()
#

#COMPUTE OVERLAPS:
VIDEO_NAME = 'Termite Test'
with open(os.path.join(SHAPES_DIR, f'{VIDEO_NAME}.pickle'), 'rb') as handle:
    shapes = pickle.load(handle)
results = {}
for c in itertools.combinations(shapes.keys(), 2):
    animal_1, animal_2 = list(shapes[c[0]].values()), list(shapes[c[1]].values())
    results[(c[0], c[1])] = GeometryMixin().multiframe_compute_shape_overlap(shape_1=animal_1, shape_2=animal_2, names=(c[0], c[1], VIDEO_NAME))

results_bins = {}
WINDOW_SIZE = int(1 * FPS)
for k, v in results.items():
    results_bins[k] = [sum(v[i:i + WINDOW_SIZE]) for i in range(0, len(v), WINDOW_SIZE)]











