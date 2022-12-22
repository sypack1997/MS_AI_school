# train loop
# val loop
# 모델 save
# 평가 함수
import torch
import os
import torch.nn as nn


def calculate_acc(output, target): # output : 모델에서 예측한 결과값, target : 정답지
    # 평가 함수
    output = torch.sigmoid(output) >= 0.5
    target = target == 1.0
    return torch.true_divide((output == target).sum(dim=0), output.size(0)).item()


def save_model(model, save_dir, file_name="last.pt"):
    # save model
    os.makedirs(save_dir, exist_ok=True)
    output_path = os.path.join(save_dir, file_name)
    if isinstance(model, nn.DataParallel): # 멀티 GPU쓰는데 싱글 GPU에 저장하면 오류 발생할 수 있음. 반대도 동일
        torch.save(model.module.state_dict(), output_path)
    else:
        print("싱글 GPU 저장 !! ")
        torch.save(model.state_dict(), output_path)
