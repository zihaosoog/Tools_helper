import os
import random
from shutil import copy
from tqdm import tqdm

def copy_file(old_path,new_path,list_file):
    
    if not os.path.isdir(new_path):  # 如果 to_path 目录不存在，则创建
        os.makedirs(new_path)

    for file_name in tqdm(list_file):
        old_path_file = os.path.join(old_path, file_name)
        new_path_file = os.path.join(new_path, file_name)
        copy(old_path_file, new_path_file)


trainval_path_image = '/data6/zihaosong/datasets/tree_data_all/images/'
list_name_image = os.listdir(trainval_path_image)

trainval_path_txt = '/data6/zihaosong/datasets/tree_data_all/labels/'
# list_name_txt = [i.replace('jpg','txt') for i in list_name_image]

ration_train = 0.8
num_train_val = len(list_name_image)
num_train = int(ration_train * num_train_val)
num_val = num_train_val-num_train
# print(num_train)

shuffled_image = list_name_image
random.shuffle(shuffled_image)
# print(shuffled_image[0:10])
shuffled_label = [i.replace('jpg','txt') for i in shuffled_image]
# print(shuffled_label[0:10])

train_data = shuffled_image[0:num_train]
val_data = shuffled_image[num_train:-1]

train_label = shuffled_label[0:num_train]
val_label = shuffled_label[num_train:-1]

train_image_path = '/data6/zihaosong/datasets/tree_data_all/train/images/'
train_label_path = '/data6/zihaosong/datasets/tree_data_all/train/labels/'
copy_file(trainval_path_image,train_image_path,train_data)
copy_file(trainval_path_txt,train_label_path,train_label)

val_image_path = '/data6/zihaosong/datasets/tree_data_all/val/images/'
val_label_path = '/data6/zihaosong/datasets/tree_data_all/val/labels/'
copy_file(trainval_path_image,val_image_path,val_data)
copy_file(trainval_path_txt,val_label_path,val_label)
print('Sussessful')



