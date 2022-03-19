import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

class FruitClass():
    # we need input the fruit image, its initial position and size
    def __init__(self, fruit, position, size = [200, 196]):
        self.fruit = fruit
        self.position = position
        self.size = size

    # Once the finger is in the area of fruit, update its postion
    def Update(self, cursor):
        ox, oy = self.position
        w, h = self.size
        if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
            ox, oy = cursor[0] - w//2, cursor[1] - h//2
            self.position = ox, oy     
        

cap = cv2.VideoCapture(0) #open default camera
cap.set(3, 1280) #set video width
cap.set(4, 720) #set video height
detector = HandDetector(detectionCon=0.8)

pathBasket = '/Users/sean/workspace/opencv/cvzone/virtual_drag_and_drop/basket.png'  # shape: 1005, 2092, 4
pathApple = '/Users/sean/workspace/opencv/cvzone/virtual_drag_and_drop/apple1.png'  # shape: 490, 500, 4
imgBasket = cv2.imread(pathBasket, cv2.IMREAD_UNCHANGED)
imgApple = cv2.imread(pathApple, cv2.IMREAD_UNCHANGED)
basket = cv2.resize(imgBasket, (418, 201), interpolation = cv2.INTER_AREA)
apple = cv2.resize(imgApple, (200, 196), interpolation = cv2.INTER_AREA)

ix, iy = 50, 30  #initial x, initial y
numberOfFruits = 3 # how many fruits do you want?
listFruits = []
for num in range(numberOfFruits):
    listFruits.append(FruitClass(apple, [ix + 210 * num, iy])) #210 to avoid overlap between each other

while True:
     success, img = cap.read()
     img = cv2.flip(img, 1)
     hands, img = detector.findHands(img, flipType = False)

     if hands:
         lmList = hands[0]['lmList']
         length, info, img = detector.findDistance(lmList[8], lmList[12], img)
         if length < 40:
             cursor = lmList[8]
             for fruit in listFruits:
                 fruit.Update(cursor)
                 
     img = cvzone.overlayPNG(img, basket, [10, 510])
     for fruit in listFruits:
         img = cvzone.overlayPNG(img, fruit.fruit, fruit.position)

     cv2.imshow("Hands", img)
     cv2.waitKey(1)