"""
reads XML generated by Colabeler tool and converts it to YOLO format txt file.

example: 
    python xml_to_yolo.py --help
"""

import xml.etree.ElementTree as ET
import os
import argparse

YOLO_FILE_PATH = 'train.txt'
XML_PATH = '/mnt/86093cf7-b6cb-48dd-b350-1102eba44f05/Downloads/DataSets/projectK/S1/output'
CLASSES_PATH = '/mnt/86093cf7-b6cb-48dd-b350-1102eba44f05/Downloads/DataSets/projectK/S1/output/voc_custom_classes.txt'

def getClasses(classes_path):
    with open(classes_path) as f:
            classes = f.readlines()
            classes = [clase_name.replace('\n', '') for clase_name in classes]
    f.close()
    return classes


def getYoloContents(xml_path):
    files = []
    yolo_boxes = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(xml_path):
        for file in f:
            if '.xml' in file:
                files.append(os.path.join(r, file))

    for xml_file in files:
        print(f)
        with open(xml_file) as f:
            tree=ET.parse(f)
            root = tree.getroot()
            img_file_name = root.find('path').text
            lines_text = img_file_name    
            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls not in classes or int(difficult)==1:
                    continue
                cls_id = classes.index(cls)
                xmlbox = obj.find('bndbox')
                b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
                lines_text += (" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
                pass

            yolo_boxes.append(lines_text + '\n')

    return yolo_boxes

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument(
        '--classes_path', type=str,
        help='path to class definitions, default ' + CLASSES_PATH
    )

    parser.add_argument(
        '--xml_path', type=str,
        help='path to XML files folder, default ' + XML_PATH
    )

    parser.add_argument(
        '--yolo_file_path', type=str,
        help='path to train.txt, default ' + YOLO_FILE_PATH
    )


    FLAGS = parser.parse_args()
    classes = getClasses(FLAGS.classes_path)
    yolo_boxes = getYoloContents(FLAGS.xml_path)

    with open (FLAGS.yolo_file_path,'w') as w:
        w.writelines(yolo_boxes)
        w.close()
