from json import dumps, loads
import os
from glob import glob

import dlib
import sys
from skimage import io, color
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import imutils
import heapq


dataset = None
d_name = None
d_desc = None
d_country = None
dots = None
detector = None
sp = None
facerec = None

def load_data():
    global dataset, detector, sp, facerec
    dataset = pd.read_json("fifadescriptors.json")
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
    facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
    update_arrays()


def update_arrays():
    global dataset, d_name, d_desc, dots, d_country
    d_name = dataset.name
    d_country = dataset.country
    d_desc = np.asarray(dataset.descriptor)
    dots = np.random.rand(d_desc.shape[0], 128)
    for i in range(dots.shape[0]):
        dots[i] = np.asarray(d_desc[i])


def save_data():
    global dataset
    dataset.to_json("fifadescriptors.json", orient="index", force_ascii=False, )


# def updateDescriptors(desc, name, country):
#     global savedDescriptors
#     desc = list(desc)
#     if len(desc) == 128:
#         record = {
#             "name": name,
#             "descriptor": desc,
#             "country": country
#         }
#         try:
#             savedDescriptors.append(record)
#         except AttributeError:
#             print("error")


# def loadDescriptors():
#     with open("fifadescriptors.json", 'r') as file:
#         savedDescriptors = loads(file.read())
#         file.close()
#     return savedDescriptors


# def saveDescriptors(savedDescriptors):
#     with open("fifadescriptors.json", 'w') as file:
#         file.write(dumps(savedDescriptors))
#         file.close()


# def img_parse(path, country):
#     dirpath = os.path.join(path, country)
#     people_files = glob(os.path.join(dirpath, "*"))
#     global savedDescriptors
#     print("Starting")
#     for people in people_files:
#         img = io.imread(people)
#         img = img[:, :, :3].copy()
#         tag = people.split('\\')[-1].split('_')
#         try:
#             updateDescriptors(extract_descriptor(img), "{} {}".format(tag[0], tag[1]), country)
#         except Exception as e:
#             print(people, e)
#     saveDescriptors(savedDescriptors)
#     print("Finished")


# def extract_descriptor(img):
#     try:
#         face_face = []
#         dets_webcam = detector(img)
#         for k, d in enumerate(dets_webcam):
#             shape = sp(img, d)
#             face_face = facerec.compute_face_descriptor(img, shape, 100)
#         return face_face
#     except RuntimeError:
#         print('error')


def detect(frame):
    dets_webcam = detector(frame, 1)
    for k, d in enumerate(dets_webcam):
        shape = sp(frame, d)
        face = facerec.compute_face_descriptor(frame, shape)
        t_ans = find(face, length=1)
        return t_ans


def find(desc, length=1):
    if length > 0:
        names = []
        try:
            cs = cosine_similarity([desc], dots)
            answer = heapq.nlargest(1, range(len(cs[0])), cs.take)
            for ans in answer:
                #if np.max(cs) > 0.94:
                elem = {
                    "mn": np.max(cs),
                    "name": d_name[ans],
                    "country": d_country[ans]
                }
                names.append(elem)
            if len(names) > length:
                return names[:length]
            else:
                return names
        except Exception as e:
            print(e)
            return []
    else:
        return []

# detector = dlib.get_frontal_face_detector()
# sp = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
# facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

# try:
#     savedDescriptors = loadDescriptors()
# except:
#     savedDescriptors = list()

