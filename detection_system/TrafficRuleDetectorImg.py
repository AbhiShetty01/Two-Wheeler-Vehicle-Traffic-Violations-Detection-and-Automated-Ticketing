import argparse
import time
from pathlib import Path
from prometheus_client import Counter
import requests
from pprint import pprint
import random
import os
import glob
from sqlalchemy import false
regions = ['mx', 'in'] # Change to your country
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import os
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized





def detect(opt):
    data = {}
    source, weights, view_img, save_txt, imgsz = opt["source"], opt["weights"], opt["view_img"], opt["save_txt"], opt["img_size"]
    
    # Initialize
    set_logging()
    device = select_device(opt["device"])
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    
    cudnn.benchmark = True
    existingOutputs = [] 
    imgCounter = 0

    try:
        
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        print(names)

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
        t0 = time.time()

        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=opt["augment"])[0]


            # Apply NMS
            pred = non_max_suppression(pred, opt["conf_thres"], opt["iou_thres"], classes=opt["classes"], agnostic=opt["agnostic_nms"])
            t2 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    
                    print(det)

                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in det:

                        c = int(cls)  # integer class
                        label = f'{names[c]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[c], line_thickness=3)
                        
                        x1,y1,x2,y2 = int(xyxy[0])-10, int(xyxy[1])-10, int(xyxy[2])+10, int(xyxy[3])+10

                        # print(names[c])
                        if names[c] == 'Rider':
                            print('\n\nProcessing for rider # ',xyxy)
                            rider_helmet_status = None
                            rider_lp_number = None
                            rider_lp_status = None
                            no_of_passengers = 0

                            try:
                                roi = im0s[y1:y2, x1:x2]
                                cv2.imwrite('rider.png',roi)
                            except Exception as e:
                                print("Error",str(e))
                                try:
                                    x1,y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                                    roi = im0s[y1:y2, x1:x2]
                                    cv2.imwrite('rider.png',roi)
                                except Exception as e:
                                    print("Error 1",str(e))

                            
                            rid_dataset = LoadImages('rider.png', img_size=imgsz, stride=stride)
                            rid_t0 = time.time()
                            for rid_path, rid_img, rid_im0s, rid_vid_cap in rid_dataset:
                                rid_img = torch.from_numpy(rid_img).to(device)
                                rid_img = rid_img.half() if half else rid_img.float()  # uint8 to fp16/32
                                rid_img /= 255.0  # 0 - 255 to 0.0 - 1.0
                                if rid_img.ndimension() == 3:
                                    rid_img = rid_img.unsqueeze(0)

                                rid_pred = model(rid_img, augment=opt["augment"])[0]


                                # Apply NMS
                                rid_pred = non_max_suppression(rid_pred, opt["conf_thres"], opt["iou_thres"], classes=opt["classes"], agnostic=opt["agnostic_nms"])

                                # Apply Classifier
                                if classify:
                                    rid_pred = apply_classifier(rid_pred, modelc, rid_img, rid_im0s)

                                # Process detections
                                for rid_i, rid_det in enumerate(rid_pred):  # detections per image
                                    rid_p, rid_s, rid_im0, rid_frame = rid_path, '', rid_im0s.copy(), getattr(rid_dataset, 'frame', 0)

                                    rid_p = Path(rid_p)  # to Path
                                    rid_s += '%gx%g ' % rid_img.shape[2:]  # print string
                                    if len(rid_det):
                                        
                                        # print(rid_det)

                                        # Rescale boxes from img_size to im0 size
                                        rid_det[:, :4] = scale_coords(rid_img.shape[2:], rid_det[:, :4], rid_im0.shape).round()

                                        # Print results
                                        for rid_c in rid_det[:, -1].unique():
                                            rid_n = (rid_det[:, -1] == rid_c).sum()  # detections per class
                                            rid_s += f"{rid_n} {names[int(rid_c)]}{'s' * (rid_n > 1)}, "  # add to string

                                        # Write results
                                        for *xyxy, rid_conf, cls in rid_det:

                                            rid_c = int(cls)  # integer class
                                            rid_label = f'{names[rid_c]} {rid_conf:.2f}'
                                            plot_one_box(xyxy, rid_im0, label=rid_label, color=colors[rid_c], line_thickness=3)
                                            
                                            
                                            if names[rid_c] =="Helmet":
                                                rider_helmet_status = True
                                                no_of_passengers = no_of_passengers + 1


                                            if names[rid_c] =="No Helmet":
                                                rider_helmet_status = False                                            
                                                no_of_passengers = no_of_passengers + 1
                                                

                                            if names[rid_c] =="LP":

                                                try:
                                                    x1,y1,x2,y2 = int(xyxy[0])-50, int(xyxy[1])-50, int(xyxy[2])+50, int(xyxy[3])+50
                                                    lp_roi = roi[y1:y2, x1:x2]
                                                    cv2.imwrite('rider_lp.png',lp_roi)
                                                            
                                                except Exception as e:
                                                    x1,y1,x2,y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
                                                    lp_roi = roi[y1:y2, x1:x2]
                                                    cv2.imwrite('rider_lp.png',lp_roi)
                            
                                                regions = ['mx', 'in'] # Change to your country
                                                with open("rider_lp.png", 'rb') as fp:
                                                    response = requests.post(
                                                        'https://api.platerecognizer.com/v1/plate-reader/',
                                                        data=dict(regions=regions),  # Optional
                                                        files=dict(upload=fp),
                                                        headers={'Authorization': 'Token 5cb2b9e847d8f063dc54b2fc7eac9c769c3ac4c5'})
                                                    try:
                                                        rider_lp_number = response.json()['results'][0]['plate']
                                                    except Exception as e:
                                                        pass
                                                        # print('\nALPR not able to detect',str(e))

                                                fp.close()

                                                os.remove('rider_lp.png')

                                                
                                                rider_lp_status = True

                                            # print(names[rid_c])q
                                            # print(xyxy)


                            if rider_helmet_status:
                                data["helmet_status"] = "Wearing"
                                print('\n\nRider wearing Helmet')
                            else:
                                data["helmet_status"] = "Not Wearing"
                                print('\n\nRider not wearing Helmet')


                            if rider_lp_status:
                                data["lp_status"] = "Found"

                                print('\nRider having LP')
                            else:
                                data["lp_status"] = "Not Found"
                                print('\nRider not having LP\n\n')

                            print('\nPlate Number : ',rider_lp_number )
                            # data["plate_number"] = rider_lp_number
                            data["plate_number"] = rider_lp_number if rider_lp_number else "-"

                            print('\nNo. of passengers : ',no_of_passengers )
                            data["no_of_passengers"] = no_of_passengers



                            # if rider_helmet_status == False or no_of_passengers>=3:
                            print('Voilence found')
                            if str(rider_helmet_status)+'\n'+str(rider_lp_status)+'\n'+str(rider_lp_number)+'\n'+str(no_of_passengers) not in existingOutputs:
                                cv2.imwrite('output/Det_'+str(imgCounter)+'.png',rid_im0)
                                existingOutputs.append(str(rider_helmet_status)+'\n'+str(rider_lp_status)+'\n'+str(rider_lp_number)+'\n'+str(no_of_passengers))
                                lines = 'output/Det_'+str(imgCounter)+'.png\n'+str(rider_helmet_status)+'\n'+str(rider_lp_status)+'\n'+str(rider_lp_number)+'\n'+str(no_of_passengers)+"\nNot"
                                with open('output/Det_'+str(imgCounter)+'.txt', 'w') as f:
                                    f.writelines(lines)


                                imgCounter = imgCounter+1

                    
                print("Hellooooooooooo")
                # cv2.imshow('Output', im0)
                cv2.imwrite(opt["file_name"][0], im0)
                return True, data

                # cv2.waitKey(0)  # 1 millisecond
    
  
    except Exception as e:
        print(e)
        return False, data
    return True, data
    
def start_detecttion(file=None):

    files = glob.glob('output/*')
    for f in files:
        os.remove(f)
        
    opt = {
        'weights': ['./runs/train/finalModel/weights/best.pt'],
        'source': 'dataset/t_image/',
        'img_size': 448,
        'conf_thres': 0.25,
        'iou_thres': 0.45,
        'device': 'cpu',
        'view_img': False,
        'save_txt': False,
        'save_conf': False,
        'save_crop': False,
        'nosave': False,
        'classes': None,
        'agnostic_nms': False,
        'augment': False,
        'update': False,
        'project': 'runs/detect',
        'name': 'exp',
        'exist_ok': False,
        "file_name" : ["./main_app/static/test.png"],
    }

    if file != None:
        opt["source"] = file

        

    is_success, data = detect(opt)
    if is_success:    
        return opt["file_name"][0], data
    return "", data






# start_detecttion(r"F:\Helmet_Number Plate Detection-GUI\final\test_images\498490_1_En_37_Fig2_HTML.png")