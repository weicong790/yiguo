
'''
for name in os.listdir(data_dir):
    img = Image.open(os.path.join(data_dir, name))
    img = img.convert('RGB')
    img = data_transforms(img)
    img = img.unsqueeze(0)
    if use_gpu:
        img = Variable(img.cuda())
    else:
        img = Variable(img)
    output = model(img)
    _, preds = torch.max(output.data, 1)
    print('The pic {} is {}.'.format(name, classes[preds.data[0]]))
    '''
import torch
from torchvision import transforms, datasets, models
from polls import model
from torch.autograd import Variable
import os
from PIL import Image

import time

from yiguoman.settings import PICRECON_ROOT

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

data_dir = PICRECON_ROOT+'/test_new'  # change the dir path to your images
PATH=''
value = ''
key = ''
weights_path = PICRECON_ROOT+'/weights'
class_path = PICRECON_ROOT+'/training_set'

classes = os.listdir(class_path)
classes.sort()
use_gpu = torch.cuda.is_available()

transforms_op = [
    transforms.Resize((100, 100), interpolation=3),
    # transforms.RandomHorizontalFlip(p=0.5),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ]
data_transforms = transforms.Compose(transforms_op)

# model = mymodel(len(classes))
model1 = model.mymodel(95)
model1.load_state_dict(torch.load(os.path.join(weights_path, 'net_2.pth')))
if use_gpu:
    model1.cuda()
model1.train(False)

def image_classification(PATH):
        my_dict = {"Apple Braeburn": "苹果", "Apple Golden 1": "苹果", "Apple Golden 2": "苹果","Apple Golden 3":"苹果","Apple Granny Smith":"苹果","Apple Red 1":"苹果",
                   "Apple Red 2":"苹果","Apple Red 3":"苹果","Apple Red Delicious":"苹果","Apple Red Yellow 1":"苹果","Apple Red Yellow 2":"苹果","Apricot":"杏","Avocado":"鳄梨",
                   "Avocado ripe":"鳄梨","Banana":"香蕉","Banana Lady Finger":"香蕉","Banana Red":"香蕉","Cactus fruit":"仙人掌果实","Cantaloupe 1":"哈密​​瓜","Cantaloupe 2":"哈密​​瓜",
                   "Carambula":"杨桃","Cherry 1":"樱桃","Cherry 2":"樱桃","Cherry Rainier":"樱桃","Cherry Wax Black":"樱桃","Cherry Wax Red":"樱桃","Cherry Wax Yellow":"樱桃",
                    "Chestnut":"栗","Clementine":"小柑橘","Cocos":"椰子","Dates":"枣子","Granadilla":"百香果","Grape Blue":"葡萄","Grape Pink":"葡萄","Grape White":"葡萄","Grape White 2":"葡萄","Grape White 3":"葡萄",
                   "Grape White 4":"葡萄","Grapefruit Pink":"葡萄柚","Grapefruit White":"葡萄柚","Guava":"石榴","Hazelnut":"榛子","Huckleberry":"蓝莓","Kaki":"柿子",
                   "Kiwi":"猕猴桃","Kumquats":"金桔","Lemon":"柠檬","Lemon Meyer":"柠檬","Limes":"酸橙","Lychee":"荔枝","Mandarine":"柑橘"}
        piece = PATH.split('/')
        data_dir1 = []
        for n in range(len(piece) - 1):
            data_dir1.append(piece[n])
        # print(data_dir1)
        data_dir = '/'.join(data_dir1)
        num = len(piece) - 1
        name = piece[num]
        print(data_dir)
        print(name)
        print(os.path.join(data_dir, name))
        img = Image.open(os.path.join(data_dir,name))

        print(type(img))
        img = img.convert('RGB')
        img = data_transforms(img)
        img = img.unsqueeze(0)

        if use_gpu:
            img = Variable(img.cuda())
        else:
            img = Variable(img)
        output = model1(img)
        _, preds = torch.max(output.data, 1)
        #print('The pic {} is {}.'.format(name, classes[preds.data[0]]))
        key=classes[preds.data[0]]
        value = my_dict[key]
        return value