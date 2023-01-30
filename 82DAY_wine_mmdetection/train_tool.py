import mmcv
import torch

from mmdet.apis import init_detector, inference_detector
from mmdet.datasets.builder import DATASETS
from mmdet.datasets.coco import CocoDataset
from mmdet.datasets import build_dataset
from mmdet.models import build_detector
from mmdet.apis import set_random_seed
from mmdet.apis import train_detector
from mmdet.utils import collect_env, get_root_logger, setup_multi_processes
from mmcv.runner import get_dist_info, init_dist
from mmcv import Config

# Dataset register
@DATASETS.register_module(force=True) # train위해 등록
class WineLabelsDataset(CocoDataset) :
    CLASSES = ('wine-labels', 'AlcoholPercentage',
               "Appellation AOC DOC AVARegion",
               "Appellation QualityLevel",
               "CountryCountry",
               "Distinct Logo",
               "Established YearYear",
               "Maker-Name",
               "Organic",
               "Sustainable",
               "Sweetness-Brut-SecSweetness-Brut-Sec",
               "TypeWine Type",
               "VintageYear",
               )

# config
config_file = "./configs/dynamic_rcnn/dynamic_rcnn_r50_fpn_1x_coco.py" # 사용할 model 구성 경로
cfg = Config.fromfile(config_file) # config read

# Learning rate setting
# sing GPU -> 0.0025
# cfg.optimizer.lr = 0.02/8
cfg.optimizer.lr = 0.0025 # 논문 디폴트 값의 GPU와 로컬 GPU 갯수 차이에 의해 나누기 8해줌 
# config/_base_/schedules/schedule_1x.py

# dataset setting
cfg.dataset_type = "WineLabelsDataset"
cfg.data_root = "./dataset"
# config/_base_/datasets/coco_detection.py

# train, val test dataset >> type data root ann file img_prefix setting
# train
cfg.data.train.type = "WineLabelsDataset" # == dataset.type
cfg.data.train.ann_file = "./dataset/train/_annotations.coco.json"
cfg.data.train.img_prefix = "./dataset/train/"
# config/_base_/datasets/coco_detection.py

# val
cfg.data.val.type = "WineLabelsDataset"
cfg.data.val.ann_file = "./dataset/valid/_annotations.coco.json"
cfg.data.val.img_prefix = "./dataset/valid/"

# test
cfg.data.test.type = "WineLabelsDataset"
cfg.data.test.ann_file = "./dataset/test/_annotations.coco.json"
cfg.data.test.img_prefix = "./dataset/test/"

# class number
cfg.model.roi_head.bbox_head.num_classes = 13 # class 갯수 / 모델마다 구조가 다르기 때문에 각각 확인해야함
# config/_base_/models/faster_rcnn_r50_fpn.py

# small obj -> change anchor -> df : size 8 -> size 4
cfg.model.rpn_head.anchor_generator.scales = [4] # 이미지 스케일 / 8로 할경우 이미지가 너무 작아짐. 보통 4로 고정

# pretrained call
cfg.load_from = "./dynamic_rcnn_r50_fpn_1x-62a3f276.pth" # mmdetection github에서 일치하는 pretrained 다운

# train model save dir
cfg.work_dir = "./work_dirs/0130" # pt파일 저장 위치

# lr hyp setting
cfg.lr_config.warmup = None
cfg.log_config.interval = 10 # epoch 개념이라 생각. 10마다 확인

# cocodataset evaluation type = bbox
# mAP iou threshold 0.5 ~ 0.95
cfg.evaluation.metric = 'bbox' # mAP 0.5~0.95 설정 값
cfg.evaluation.interval = 10
cfg.checkpoint_config.interval = 10 # 10마다 저장

# epoch setting
# 8 x 12 -> 96
cfg.runner.max_epochs = 88 # 논문 설정 값 12에폭 == 로컬 12*8 에폭 / GPU갯수 차이
cfg.seed = 777
cfg.data.samples_per_gpu = 6 # 고정
cfg.data.workers_per_gpu = 2 # 고정
# print("cfg.data >>" , cfg.data)
cfg.gpu_ids = range(1)
cfg.device = "cuda"
set_random_seed(777, deterministic=False)
# print("cfg info show ", cfg.pretty_text)

datasets = [build_dataset(cfg.data.train)] # 설정 값 데이터셋 실행
# print("dataset[0]", datasets[0])
# mmdet / datasets / builder.py

# datasets[0].__dict__ variables key val
datasets[0].__dict__.keys()

model = build_detector(cfg.model, train_cfg=cfg.get("train_cfg"),
                       test_cfg=cfg.get('test_cfg'))
model.CLASEES = datasets[0].CLASSES
print(model.CLASEES)
# mmdet / models / builder.py

if __name__ == '__main__' :
    train_detector(model, datasets,cfg,distributed=False, validate=True)
    # mmdet / apis / train.py