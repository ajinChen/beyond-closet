import os
from skimage import io
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

import numpy as np
from PIL import Image

from data_loader import RescaleT
from data_loader import ToTensor
from data_loader import ToTensorLab
from data_loader import SalObjDataset

from model import U2NET # full size version 173.6 MB


def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d-mi)/(ma-mi)
    return dn


def mode_color(idx,image,prdimg):
    inarray = io.imread(image[idx])
    prdarray = prdimg[idx]
    inarray_copy =inarray.reshape((-1,3))
    prdarray_copy = prdarray.reshape((-1,3))
    temp = np.where(prdarray_copy!=0,inarray_copy,0)
    tst = np.any(temp != 0, axis=-1)
    unique, counts = np.unique(temp[tst],axis = 0,return_counts = True)
    idx = np.argmax(counts)
    mode = unique[idx]
    return mode

def get_color(url):
    # --------- 1. get image path and name ---------
    model_name='u2net'
    # add model path here
    model_dir = os.path.join(os.getcwd(), 'saved_models', model_name, model_name + '.pth')
    img_name_list = url
    # --------- 2. dataloader ---------
    test_salobj_dataset = SalObjDataset(img_name_list = img_name_list,
                                        lbl_name_list = [],
                                        transform=transforms.Compose([RescaleT(320),
                                                                      ToTensorLab(flag=0)])
                                        )
    test_salobj_dataloader = DataLoader(test_salobj_dataset,
                                        batch_size=1,
                                        shuffle=False,
                                        num_workers=1)
    # --------- 3. model define ---------
    if(model_name=='u2net'):
        print("...load U2NET---173.6 MB")
        net = U2NET(3,1)
    elif(model_name=='u2netp'):
        print("...load U2NEP---4.7 MB")
        net = U2NETP(3,1)

    if torch.cuda.is_available():
        net.load_state_dict(torch.load(model_dir))
        net.cuda()
    else:
        net.load_state_dict(torch.load(model_dir, map_location='cpu'))
    net.eval()

    # --------- 4. inference for each image ---------
    prediction = []
    for i_test, data_test in enumerate(test_salobj_dataloader):

        print("inferencing:",img_name_list[i_test].split(os.sep)[-1])

        inputs_test = data_test['image']
        inputs_test = inputs_test.type(torch.FloatTensor)

        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)

        d1,d2,d3,d4,d5,d6,d7= net(inputs_test)

        # normalization
        pred = d1[:,0,:,:]
        pred = normPRED(pred)
        predict = pred.squeeze()
        predict_np = predict.cpu().data.numpy()
        im = Image.fromarray(predict_np*255).convert('RGB')
        img_name = img_name_list[i_test]
        image = io.imread(img_name)
        imo = im.resize((image.shape[1],image.shape[0]),resample=Image.BILINEAR)
        prediction.append(np.array(imo))
        del d1,d2,d3,d4,d5,d6,d7
       
    # --------- 5. get colors ---------
    color = [mode_color(i,url,prediction) for i in range(len(url))]
    print(color)
    return color

if __name__ == "__main__":
    main()