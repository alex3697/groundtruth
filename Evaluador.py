import  xml.etree.ElementTree as ET
import sys
import re

def get_levels_from_scene(scene):
    # Iteramos todos los elementos del shot 0
    for shot in scene:
        print('Level 0 ', shot.tag)
        for key_frame_decomposition in shot:
            print('\tLevel 1 ', key_frame_decomposition.tag)
            for key_frame in key_frame_decomposition:
                print('\t\tLevel 2 ', key_frame.tag)
                for child in key_frame:
                    print('\t\t\tLevel 3 ', child.tag)


def get_scenes(root):
    return root[-1][0]


def get_key_frame_information(key_frame):

    # Key Frame Information
    info_key_frame_id = key_frame[0]
    info_file_name = key_frame[1]
    info_frame_position = key_frame[2]

    return info_key_frame_id, info_file_name, info_frame_position


def get_descriptors(key_frame):

    # Key Frame Descriptors
    image_descriptors = key_frame[3]
    objects = image_descriptors[0][0]
    places = image_descriptors[1][0]
    faces = image_descriptors[2]
    captions = image_descriptors[3] 
    aesthetics = image_descriptors[4][0]
    return objects, places, faces, captions, aesthetics



def print_key_frame(key_frame):
    # Key Frame Information
    info_key_frame_id, info_file_name, info_frame_position = get_key_frame_information(key_frame)

    # Key Frame Descriptors
    objects, places, faces, captions, aesthetics = get_descriptors(key_frame)

    # KeyFrame Information
    print(info_key_frame_id.attrib)
    print(info_file_name.attrib)
    print(info_frame_position.attrib)
    print('-------------------\n')

    # Objects
    for child in objects:
        print(child.attrib)
    print('-------------------\n')

    # Places
    for child in places:
        print(child.attrib)
    print('-------------------\n')

    # Faces
    for level in faces:
        for child in level:
            print(child.attrib)
    print('-------------------\n')

    # Captions
    for level in captions:
        for child in level:
            print(child.attrib)
    print('-------------------\n')

    # Aesthetics
    for child in aesthetics:
        print(child.attrib)
    print('-------------------\n')


def check_metadata_structure(scenes, scenes_ref):
    for scene, scene_ref in zip(scenes, scenes_ref):
        if scene.attrib['id'] != scene_ref.attrib['id']:
            print('The scene id doesn\'t match: (%s, %s)' % (scene.attrib['id'], scene_ref.attrib['id']))
            sys.exit()
        for shot, shot_ref in zip(scene.findall('Shot'), scene_ref.findall('Shot')):
            if shot.attrib['id'] != shot_ref.attrib['id']:
                print('The shots id doesn\'t match: (%s, %s)' % (shot.attrib['id'], shot_ref.attrib['id']))
                sys.exit()
            # for frame, frame_ref in zip(shot[0], shot_ref[0]):
            #     if frame[2].attrib['value'] != frame_ref[2].attrib['value']:
            #         print('The frame id doesn\'t match: (%s, %s)' % (frame.attrib['id'], frame_ref.attrib['id']))
            #         sys.exit()




if __name__ == '__main__':

    # Load reference
    metadata_name_ref = 'metadata.xml'
    folder_path = 'C:\\Users\\Alex\\Desktop\\Ugiat\\groundtruth\\groundtruth\\autocatalogador\\prueba\\'

    xml_file_name_ref = folder_path + metadata_name_ref

    tree_ref = ET.parse(xml_file_name_ref)
    root_ref = tree_ref.getroot()

    # Obtenemos el conjunto de escenas
    scenes_ref = get_scenes(root_ref)
    scene_0_ref = scenes_ref[0]

    # Load model
    metadata_name = 'metadata_google_v5.xml'
    folder_path = 'C:\\Users\\Alex\\Desktop\\Ugiat\\groundtruth\\groundtruth\\autocatalogador\\prueba\\'

    xml_file_name = folder_path + metadata_name

    tree = ET.parse(xml_file_name)
    root = tree.getroot()

    # Obtenemos el conjunto de escenas
    scenes = get_scenes(root)
    scene_0 = scenes[0]
    score_vector = []
    key_frame_count=0
    shot_count = 0
    scene_count = 0
    matched_count = 0
    good_words_count = 0

    # We iterate over KeyFrames comparing them
    for scene, scene_ref in zip(scenes,scenes_ref):
        scene_count += 1
        for shot, shot_ref in zip(scene, scene_ref[:]):
            shot_count += 1
            key_frame_ref_iter = iter(shot_ref[0][:])
            try:
                key_frame_ref = next(key_frame_ref_iter)
            except StopIteration:
                continue
            for key_frame in shot[0]:
                try:
                    if key_frame.findall('Info')[2].attrib['value'] == key_frame_ref.findall('Info')[2].attrib['value']:
                        key_frame_count +=1
                        # KeyFrame information
                        info_key_frame_id, info_file_name, info_frame_position = get_key_frame_information(key_frame)
                        info_key_frame_id_ref, info_file_name_ref, info_frame_position_ref = get_key_frame_information(key_frame_ref)

                        # Descriptors
                        objects, places, faces, captions, aesthetics = get_descriptors(key_frame)
                        objects_ref, places_ref, faces_ref, captions_ref, aesthetics_ref = get_descriptors(key_frame_ref)


                        # Compare captions
                        n_captions = captions[0][0].attrib['value']
                        if n_captions != '0':
                            string = captions[1][0].attrib['string']
                        elif n_captions == '0':
                            continue
                        string = string.lower()
                        data = re.findall(r"[\w']+", string)

                        n_captions_ref = captions_ref[0][0].attrib['value']
                        string_ref = captions_ref[1][0].attrib['string']
                        string_ref = string_ref.lower()
                        data_ref = re.findall(r"[\w']+", string_ref)

                        n_common_words = 0
                        data_or = data_ref[:]
                        good_words_count = good_words_count + len(data_ref)

                        for word in data:
                            if word in data_ref:
                                n_common_words += 1
                                idx = []
                                idx.append(data_ref.index(word))
                                i = idx[0]
                                del data_ref[i]
                                matched_count = matched_count + 1


                        score = n_common_words / len(data_or)
                        score_vector.append(score)

                        print('Number of captions KeyFrame %s: %s' % (info_frame_position.attrib['value'], n_captions))
                        print('Content:\n%s' % data)
                        print('Ref:\n%s' % data_or)
                        print('Score:\n%s' % score)
                        key_frame_ref = next(key_frame_ref_iter)


                except StopIteration:
                    continue



    score_total = 0
    for score in score_vector:
        score_total = score + score_total
    score_total = score_total/len(score_vector)
    print(f'el score total promediado es {score_total}')
    
    
    minpos = score_vector.index(min(score_vector))
    print(minpos)  
    print(f'el numero de frames en cuenta es {key_frame_count}')
    print(f'el numero de shots es {shot_count}')
    print(f'el numero de scenes es {scene_count}')
    ratio_por_palabras = matched_count/good_words_count
    print(f'el porcentaje de acierto por palabras es {ratio_por_palabras}')