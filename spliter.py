import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET


tree = ET.parse('C:\\Users\\Alex\\Desktop\\Ugiat\\groundtruth\\groundtruth\\autocatalogador\\prueba\\metadata_google_v5.xml')
root = tree.getroot()  
shots = []

for shot in root.iter('Shot'):
    framelista = []
    for frame in shot.iter('KeyFrame'):
        framelista.append(int(frame.findall('Info')[2].attrib['value']))
    shots.append(framelista)



pos = 2514
N = 193
vector_buenos = []
for shot in shots:
    for (i, line) in enumerate(shot):
        # if len(shot) == i+1 :
        #     vector_buenos.append(line)
        #     continue
        # if i == 0:
        #     pos = line
        #     vector_buenos.append(line)
        #     continue
        if line >= pos + N:
            pos = line
            vector_buenos.append(line)
            continue
vector_buenos[len(vector_buenos) - 1] = vector_buenos[len(vector_buenos) - 1] - 2

# for shot in root.iter('Shot'):
#     framelista = []
#     for frame in shot.iter('KeyFrame'):
#         framelista.append(int(frame.findall('Info')[2].attrib['value']))
#     shots.append(framelista)

# N = 26
# vector_buenos = []
# for shot in shots:
#     for (i, line) in enumerate(shot):
#         if len(shot) == i+1 :
#             vector_buenos.append(line)
#             continue    
#         if i == 0:
#             pos = line
#             vector_buenos.append(line)
#             continue
#         if line >= pos + N:
#             pos = line
#             vector_buenos.append(line)
#             continue

# Playing video from file:

cap = cv2.VideoCapture('C:\\Users\\Alex\\Desktop\\Ugiat\\groundtruth\\groundtruth\\autocatalogador\\video.mp4')
length = cap.get(cv2.CAP_PROP_FRAME_COUNT)
currentFrame = 1
ret, frame = cap.read()
name = 'C:\\Users\\Alex\\Desktop\\Ugiat\\groundtruth\\groundtruth\\autocatalogador\\data\\frame' + str(currentFrame).zfill(6) + '.jpg'

print ('Creating...' + name)

cv2.imwrite(name, frame)


try:

    if not os.path.exists('data'):

        os.makedirs('data')

except OSError:

    print ('Error: Creating directory of data')




x = 0

while(x < len(vector_buenos)):

    # Capture frame-by-frame

    ret, frame = cap.read()



    # Saves image of the current frame in jpg file
    if vector_buenos[x] == currentFrame:
        name = 'C:\\Users\\Alex\\Desktop\\Ugiat\\groundtruth\\groundtruth\\autocatalogador\\data\\frame' + str(currentFrame).zfill(6) + '.jpg'

        print ('Creating...' + name)

        cv2.imwrite(name, frame)
        x += 1



    # To stop duplicate images

    currentFrame += 1



# When everything done, release the capture

cap.release()

cv2.destroyAllWindows()