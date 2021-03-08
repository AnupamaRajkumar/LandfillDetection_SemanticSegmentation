import json
import os
import glob
import collections

def CreateCOCODataset(imagePath, annotationPath):
        JsonDataset = {}
        #info
        infoObj = {
                "year"          : 2021,
                "version"       : "0.1",
                "description"   : "Landfill COCO Dataset",
                "contributor"   : "Anupama Rajkumar",
                "url"           : "https://github.com/AnupamaRajkumar",
                "date_created"  : "2021/03/07"
        }
        JsonDataset["info"] = infoObj

        #licenses
        licenses =  {
                "url"           : "https://creativecommons.org/licenses/by/2.0/",
                "id"            : 2,
                "name"          : "Attribution License"
        }
        JsonDataset["licenses"] = licenses

        #images
        images = []
        imgCount = 1
        print(imagePath)
        for fileName in os.listdir(imagePath):
                imgObj = {
                        "file_name"     :    fileName,   
                        "image_id"      :    imgCount,
                        "height"        :    512,
                        "width"         :    512
                }
                images.append(imgObj)
                imgCount = imgCount+1
        JsonDataset["images"] = images

        #annotations
        annotations = []
        annoCount = 1
        print(annotationPath)
        for fileName in os.listdir(annotationPath):
                #iterate over the anootation jsons to extract the polygon coordinates   
                segmentation = [] 
                if fileName.endswith(".json"):
                        f = open(os.path.join(annotationPath, fileName), 'r')
                        data = json.load(f)
                        #print(data)
                        annotation = []
                        for d in data['geometry']['coordinates']:
                                for c in d:
                                        for coords in c:
                                                annotation.append(coords)
                        segmentation.append(annotation)

                annos = {
                        "image_id"      :       annoCount,
                        "iscrowd"       :       0,
                        "category_id"   :       1,
                        "segmentation"  :       segmentation
                }
                annotations.append(annos)
                annoCount = annoCount + 1
        JsonDataset["annotations"] = annotations

        #categories
        categories = {
                "category_id"           :       1,
                "category_name"         :       "Open landfills"
        }
        JsonDataset["categories"] = categories
        return JsonDataset


fileName = "D:/SZTAKI_Thesis/Code/LandfillTrainingDataset.json"
imagePath = "D:/SZTAKI_Thesis/Images/Dataset/Image/HR_TIF_Files"
annotationPath = "D:/SZTAKI_Thesis/Images/Dataset/Labels/PerImagePolygonCoords"

JSONDataset = CreateCOCODataset(imagePath, annotationPath)
#print(JSONDataset)
with open(fileName, 'a+') as trainFile:
    json.dump(JSONDataset, trainFile)