import cv2
from dbase import choice_human_finder, choice_human_owner
from skimage.metrics import structural_similarity


def selection(person):
    if person.status == 1:
        all = choice_human_finder(person.city, person.type_pet)
    else:
        all = choice_human_owner(person.city, person.type_pet)

    idx = 0
    for hum in all:
        if hum[8] != person.sex_pet or hum[8] is None:
            if hum[7] != person.name_pet or hum[7] is None:
                del all[idx]
        idx += 1

    return all


def compare_images(image1_path, image2_path):
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    img1 = cv2.resize(img1, (800, 800))
    img2 = cv2.resize(img2, (800, 800))

    similarity_index, _ = structural_similarity(img1, img2, full=True)

    return similarity_index * 100


def selection2(person):
    x = 55
    true = []
    image_true = selection(person)
    for i in image_true:
        percent = compare_images(person.photo, i[-1])
        if percent > x:
            true.append(i)

    return true
