
# 说明
# Market 1501 的命名格式为：0001_c1s1_001051_00.jpg
# 0001: 行人ID号，一共 1501 个ID，bounding_box_train 中 751 个，bounding_box_test 中 750 个
# 
# 在原始下载的 http://188.138.127.15:81/Datasets/Market-1501-v15.09.15.zip 中，有如下内容
#   bounding_box_train 的 ID 号 分散于 0002-1500 之间，共 751 个ID
#   bounding_box_test  有 750 个与训练集不同的 ID，其中包含了 -1 和 0000
#       -1 开头的图片被认为是 junks
#       0000 开头的图片被认为是 distractors
#       junks 和 distractors 的评价标准：我们通过人手工地在原始视屏上绘制 bounding box
#       计算 DPM-bounding-box 和 ground-truth bounding box 的 IoU 
#       IoU > 50% : marked as good; IoU < 20% : marked as distractor; otherwise, marked as junk
#       文章中写到：junk images are neither good nor bad DPM bboxs ?? why??
#                 distractor images have a negative impact on accuracy ?? why??
#   query 750 个行人的图片，针对一个行人，从每个摄像头上随机选择一张图片，因此每个人最多有6张查询图片
#       由于有的摄像头没有记录某个行人的图像，因此有的行人图片数少于 6 张
#   gt_query 该文件夹中的内容不用了
#   gt_bbox 我们所提供的人工绘制的 bbox，用于判断DPM bbox 属于 distractor, junk, good

#   处理后：
#   bounding_box_train 中的内容被分类到 train_all 下，其中 选出 751 作为 val, 剩余的作为 train
#   bounding_box_test 中的内容被分类到 gallery 下
#   gt_bbox 中的内容被分类到 multi_query 下
#   query 中的内容被分类到 query 下


import os
from shutil import copyfile

market_dir = "/home/linux_fhb/data/market-1501/Market-1501-v15.09.15"
bounding_box_test = os.path.join(market_dir, 'bounding_box_test')
bounding_box_train = os.path.join(market_dir, 'bounding_box_train')
gt_bbox = os.path.join(market_dir, 'gt_bbox')
query = os.path.join(market_dir, 'query')

target_dir = os.path.join(market_dir, 'f_target')

if os.path.isdir(target_dir):
    print(f'{target_dir} has existed')
    exit()
else:
    os.mkdir(target_dir)

def classify_images(source_dir, cur_dir):
    print(f'deal with {cur_dir}')
    if not os.path.isdir(cur_dir):
        os.mkdir(cur_dir)
    files = [file for file in os.listdir(source_dir) if file.endswith('jpg')]
    cnt = 1
    for file in files:
        filename = os.path.splitext(file)[0]
        person_id = filename.split('_')[0]
        tp_dir = os.path.join(cur_dir, person_id)
        if not os.path.isdir(tp_dir):
            os.mkdir(tp_dir)
        copyfile(os.path.join(source_dir, file),
                os.path.join(tp_dir, file))
        cnt += 1
        print(f"processing : {len(files)} / {cnt}", end='\r')
    print()

# deal with bounding_box_test
classify_images(bounding_box_test, os.path.join(target_dir, 'gallery'))
        
# deal with query
classify_images(query, os.path.join(target_dir, 'query'))

# deal with gt_bbox
classify_images(gt_bbox, os.path.join(target_dir, 'multi-query'))

# deal with bounding_box_train, create train_all directory
# classify_images(bounding_box_train, os.path.join(target_dir, 'train_all'))

# deal with bounding_box_train, create val and train
train_all = os.path.join(target_dir, 'train_all')
train_dir = os.path.join(target_dir, 'train')
val_dir = os.path.join(target_dir, 'val')

if not os.path.isdir(train_dir):
    os.mkdir(train_dir)

if not os.path.isdir(val_dir):
    os.mkdir(val_dir)

if not os.path.isdir(train_all):
    os.mkdir(train_all)

cnt = 0
print('deal with train and val')
files = [file for file in os.listdir(bounding_box_train) if file.endswith('jpg')]
for file in files:
    filename = os.path.splitext(file)[0]
    person_id = filename.split('_')[0]
    train_all_pid_dir = os.path.join(train_all, person_id)
    if not os.path.isdir(train_all_pid_dir):
        os.mkdir(train_all_pid_dir)
    source_file = os.path.join(bounding_box_train, file)
    copyfile(source_file, os.path.join(train_all_pid_dir, file))
    if not os.path.isdir(os.path.join(val_dir, person_id)):
        val_pid_dir = os.path.join(val_dir, person_id)
        os.mkdir(val_pid_dir)
        os.mkdir(os.path.join(train_dir, person_id))
        copyfile(source_file, os.path.join(val_pid_dir, file))
    else:
        train_pid_dir = os.path.join(train_dir, person_id)
        copyfile(source_file, os.path.join(train_pid_dir, file))
    cnt += 1
    print(f"processing : {len(files)} / {cnt}", end='\r')

print()
        
        


