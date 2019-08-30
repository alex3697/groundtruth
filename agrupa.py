import glob
import xml.etree.ElementTree as ET

txts = glob.glob('C:/Users/Alex/Desktop/Ugiat/groundtruth/groundtruth/autocatalogador/Data/*.txt')
vector_buenos = []
for txt in txts:
   f = open(txt,"r")
   keyframe = int(f.name[-10:-4])
   vector_buenos.append(keyframe)

x = 0

# Save XML
f = open('C:/Users/Alex/Desktop/Ugiat/groundtruth/groundtruth/autocatalogador/prueba/metadata.xml','w')
tree = ET.parse('C:/Users/Alex/Desktop/Ugiat/groundtruth/groundtruth/autocatalogador/prueba/metadata_google_v5.xml')
root = tree.getroot()  
#f.write('<?xml version="1.0" encoding="utf-8"?>\n')
f.write('<VideoDescription>\n')
f.write('\t')
f.write(ET.tostring(root[0],encoding='unicode'))
f.write('<TemporalGlobalDescriptors />\n')
f.write('\t<HierchicalDecomposition>\n')
f.write('\t\t<SceneDecomposition>\n')

for scene in root[-1][0]:
   f.write(f'\t\t\t<Scene')
   f.write(f' category="')
   f.write(scene.attrib['category'])
   f.write('" id="')
   f.write(scene.attrib['id'])
   f.write('" tcin="')
   f.write(scene.attrib['tcin'])
   f.write('" tcout="')
   f.write(scene.attrib['tcout'])
   f.write('"')
   f.write('>\n')
   for shot in scene:
      f.write(f'\t\t\t\t<Shot')
      f.write(f' category="')
      f.write(shot.attrib['category'])
      f.write('" id="')
      f.write(shot.attrib['id'])
      f.write('" tcin="')
      f.write(shot.attrib['tcin'])
      f.write('" tcout="')
      f.write(shot.attrib['tcout'])
      f.write('"')
      f.write('>\n')
      for keyframeDecomposition in shot:
         f.write('\t\t\t\t\t<KeyFrameDecomposition>\n')
         for keyframe in keyframeDecomposition:
            if x >= len(vector_buenos):
               continue

            elif int(keyframe.findall('Info')[2].attrib['value']) == vector_buenos[x]:
               f.write('\t\t\t\t\t\t<KeyFrame>\n')
               f.write(f'\t\t\t\t\t\t\t<Info name="')
               f.write(keyframe.findall('Info')[0].attrib['name'])
               f.write('" value="')
               f.write(keyframe.findall('Info')[0].attrib['value'])
               f.write('" />')
               f.write('\n')
               f.write(f'\t\t\t\t\t\t\t<Info name="')
               f.write(keyframe.findall('Info')[1].attrib['name'])
               f.write('" value="')
               f.write(keyframe.findall('Info')[1].attrib['value'])
               f.write('" />')
               f.write('\n')
               f.write(f'\t\t\t\t\t\t\t<Info name="')
               f.write(keyframe.findall('Info')[2].attrib['name'])
               f.write('" value="')
               f.write(keyframe.findall('Info')[2].attrib['value'])
               f.write('" />')
               f.write('\n')
               f.write('\t\t\t\t\t\t\t<ImageDescriptors>\n')
               with open('C:/Users/Alex/Desktop/Ugiat/groundtruth/groundtruth/autocatalogador/Data/frame'+keyframe.findall('Info')[2].attrib['value'].zfill(6)+'.txt','r') as datos:
                  captions = 0
                  captionList = []
                  for (i, line) in enumerate(datos):
                    if i == 0:
                        continue
                    tmp = [t.strip() for t in line.split()]
                    if tmp[5] == '0':
                       captions += 1
                       captionList.append(tmp[:-1])
               #f.write(f'\t\t\t\t\t\t\t\t<ObjectsDescripor>\n')
               f.write(f'\t\t\t\t\t\t\t\t')
               f.write(ET.tostring(keyframe[3][0],encoding='unicode'))
               #f.write(f'\t\t\t\t\t\t\t\t</ObjectsDescripor>\n')
               #f.write(f'\t\t\t\t\t\t\t\t<PlacesDescripor>\n')
               f.write(ET.tostring(keyframe[3][1],encoding='unicode'))
               #f.write(f'\t\t\t\t\t\t\t\t</PlacesDescripor>\n')
               #f.write(f'\t\t\t\t\t\t\t\t<FaceDescripor>\n')
               f.write(ET.tostring(keyframe[3][2],encoding='unicode'))
               #f.write(f'\t\t\t\t\t\t\t\t</FaceDescripor>\n')
               f.write(f'<CaptionsDescripor>\n')
               f.write('\t\t\t\t\t\t\t\t\t<CaptionsInformation><Info name="NumberOfCaptions" value="')
               if captions != 0:
                  f.write(str(captions + 1))
               elif captions == 0:
                  f.write(str(captions))
               f.write('" />')
               f.write('</CaptionsInformation>')
               if captions != 0:
                  f.write('<Captions>')
                  id = 1
                  f.write('<caption id="')
                  f.write(str(id) + '" string="')
                  for capt in captionList:
                     f.write(capt[4])
                     f.write('&#10;')
                  f.write('" x1="')
                  f.write(str(capt[3])+ '" x2="')
                  f.write(str(capt[2]) + '" y1="')
                  f.write(str(capt[1]) + '" y2="')
                  f.write(str(capt[0]) + '" />')

                  id = 2
                  for capt in captionList:
                     f.write('<caption id="')
                     f.write(str(id) + '" string="' + capt[4]+'" x1="')
                     f.write(str(capt[3])+ '" x2="')
                     f.write(str(capt[2]) + '" y1="')
                     f.write(str(capt[1]) + '" y2="')
                     f.write(str(capt[0]) + '" />')
                     id +=1
                  f.write('</Captions>\n')
               f.write(f'\t\t\t\t\t\t\t\t</CaptionsDescripor>\n')
               #f.write(f'\t\t\t\t\t\t\t\t<AestheticsDescriptor>\n')
               f.write(f'\t\t\t\t\t\t\t\t')
               f.write(ET.tostring(keyframe[3][4],encoding='unicode'))
               #f.write(f'\t\t\t\t\t\t\t\t</AestheticsDescriptor>\n')
               f.write('</ImageDescriptors>\n')
               f.write('\t\t\t\t\t\t</KeyFrame>\n')
               x += 1
         f.write('\t\t\t\t\t</KeyFrameDecomposition>\n')
      f.write(f'\t\t\t\t</Shot>\n')
   f.write(f'\t\t\t</Scene>\n')
f.write('\t\t</SceneDecomposition>\n')
f.write('\t</HierchicalDecomposition>\n')
f.write('</VideoDescription>')
f.close()
