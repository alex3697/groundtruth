import xml.etree.ElementTree as ET
import os


#132            54372       2514        140

tree = ET.parse('metadata_google_v5.xml')
root = tree.getroot()  
shots = []

for shot in root.iter('Shot'):
    framelista = []
    for frame in shot.iter('KeyFrame'):
        framelista.append(int(frame.findall('Info')[2].attrib['value']))
    shots.append(framelista)



pos = 2514
N = 140
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
x = 0

for frame in root.iter('KeyFrame'):
    if int(frame.findall('Info')[2].attrib['value']) == vector_buenos[x]:
        captions = False
        faces = False
        for x in frame.iter('Captions'):
            x= ET.tostring(x,encoding="unicode")
            if (x != '<Captions />\n'):
                captions = True
        for y in frame.iter('Faces'):
            y= ET.tostring(y,encoding="unicode")
            if y != '<Faces />\n':
                faces = True


        output = open("frame" + str(frame.findall('Info')[2].attrib['value']).zfill(6) + ".txt", "w")

        if captions:
            for x in frame.iter('Captions'):
                for z in x.findall('caption'):
                    output.write(str(float(z.attrib['y1'])))
                    output.write(' ')
                    output.write(str(float(z.attrib['x1'])))
                    output.write(' ')
                    output.write(str(float(z.attrib['y2'])))
                    output.write(' ')
                    output.write(str(float(z.attrib['x2'])))
                    output.write(' ')
                    foo = z.attrib['string'].rsplit('\n')
                    output.write(' '.join(foo))
                    output.write(' ')
                    output.write('0')
                    output.write('\n')
        if faces:
            for y in frame.iter('Faces'):
                for w in y:
                    output.write(str(float(w.attrib['y1'])))
                    output.write(' ')
                    output.write(str(float(w.attrib['x1'])))
                    output.write(' ')
                    output.write(str(float(w.attrib['y2'])))
                    output.write(' ')
                    output.write(str(float(w.attrib['x2'])))
                    output.write(' ')
                    output.write(w.attrib['person_id'])
                    output.write(' ')
                    output.write('1')
                    output.write('\n')
        output.close()
        x += 1