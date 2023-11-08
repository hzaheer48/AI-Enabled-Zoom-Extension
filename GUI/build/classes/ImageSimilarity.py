import cv2
from skimage.metrics import structural_similarity as ssim

class ImageSimilarityCalculator:
    def struct_similarity(self, imageA, imageB):
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        s = ssim(imageA, imageB)
        return s