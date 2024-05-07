import cv2
import numpy as np

# # Funktion zur Anwendung von HSV-Begrenzungen auf ein Bild
# def apply_hsv_limits(hsv_image, h_min, s_min, v_min, h_max, s_max, v_max):
#     lower_limit = np.array([h_min, s_min, v_min])
#     upper_limit = np.array([h_max, s_max, v_max])
#     mask = cv2.inRange(hsv_image, lower_limit, upper_limit)
#     result = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
#     return cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

# # Leerer Callback für die Schieberegler (wird nicht verwendet)
# def empty_callback(value):
#     pass

# # Laden eines Beispielbildes (ersetze 'example.jpg' durch deinen Bildpfad)
# img_rgb = cv2.imread('testbild_Color.png')
# img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
# img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

# # Erstellen eines OpenCV-Fensters
# cv2.namedWindow('HSV Color Range Selector', 0)

# # Erstellen von Schiebereglern für HSV-Werte
# # cv2.createTrackbar('Hue Min', 'HSV Color Range Selector', 0, 179, empty_callback)
# # cv2.createTrackbar('Saturation Min', 'HSV Color Range Selector', 0, 255, empty_callback)
# # cv2.createTrackbar('Value Min', 'HSV Color Range Selector', 0, 255, empty_callback)
# # cv2.createTrackbar('Hue Max', 'HSV Color Range Selector', 179, 179, empty_callback)
# # cv2.createTrackbar('Saturation Max', 'HSV Color Range Selector', 255, 255, empty_callback)
# # cv2.createTrackbar('Value Max', 'HSV Color Range Selector', 255, 255, empty_callback)

# while True:
#     # Lesen der aktuellen Schiebereglerwerte
#     # h_min = cv2.getTrackbarPos('Hue Min', 'HSV Color Range Selector')
#     # s_min = cv2.getTrackbarPos('Saturation Min', 'HSV Color Range Selector')
#     # v_min = cv2.getTrackbarPos('Value Min', 'HSV Color Range Selector')
#     # h_max = cv2.getTrackbarPos('Hue Max', 'HSV Color Range Selector')
#     # s_max = cv2.getTrackbarPos('Saturation Max', 'HSV Color Range Selector')
#     # v_max = cv2.getTrackbarPos('Value Max', 'HSV Color Range Selector')

#     h_min = 13 
#     s_min = 161
#     v_min = 0
#     h_max = 25
#     s_max = 255
#     v_max = 255
    

#     # Anwenden der HSV-Begrenzungen auf das Bild
#     masked_image = apply_hsv_limits(img_hsv, h_min, s_min, v_min, h_max, s_max, v_max)

#     # Konvertieren in Graustufen und Kanten erkennen (Canny-Kantenbildung)
#     gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
#     _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     edges = cv2.Canny(thresholded, threshold1=50, threshold2=150)

#     # Kreiserkennung mit dem Hough Circle Transform auf dem kantenbetonten Bild
#     circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=2, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=100)

#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         for circle in circles[0, :]:
#             center = (circle[0], circle[1])
#             radius = circle[2]
#             print("center x: ", circle[0], " center y: ", circle[1])
#             # Kreis und Mittelpunkt zeichnen
#             cv2.circle(masked_image, center, radius, (0, 255, 0), 3)
#             cv2.circle(masked_image, center, 2, (0, 0, 255), 3)

    


#     # Anzeigen des Bildes im OpenCV-Fenster
#     cv2.imshow('HSV Color Range Selector', masked_image)

#     # Auf 'q' drücken, um das Programm zu beenden
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Fenster schließen und Ressourcen freigeben
# cv2.destroyAllWindows()

class CylinderDedecter:

    def __init__(self):
        self.h_min = 13 
        self.s_min = 161
        self.v_min = 0
        self.h_max = 25
        self.s_max = 255
        self.v_max = 255
        # cv2.namedWindow('HSV Color Range Selector', 0)

    # Funktion zur Anwendung von HSV-Begrenzungen auf ein Bild
    def apply_hsv_limits(self, hsv_image):
        lower_limit = np.array([self.h_min, self.s_min, self.v_min])
        upper_limit = np.array([self.h_max, self.s_max, self.v_max])
        mask = cv2.inRange(hsv_image, lower_limit, upper_limit)
        result = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
        return cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
    
    def calculateCenter(self, img_to_dedect):
        self.img_rgb = cv2.cvtColor(img_to_dedect, cv2.COLOR_BGR2RGB)
        self.img_hsv = cv2.cvtColor(self.img_rgb, cv2.COLOR_RGB2HSV)

        # Anwenden der HSV-Begrenzungen auf das Bild
        masked_image = self.apply_hsv_limits(self.img_hsv)

        # Konvertieren in Graustufen und Kanten erkennen (Canny-Kantenbildung)
        gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        edges = cv2.Canny(thresholded, threshold1=50, threshold2=150)

        # Kreiserkennung mit dem Hough Circle Transform auf dem kantenbetonten Bild
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=2, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=100)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                center = (circle[0], circle[1])
                # radius = circle[2]
                print("center x: ", circle[0], " center y: ", circle[1])
                # # Kreis und Mittelpunkt zeichnen
                # cv2.circle(masked_image, center, radius, (0, 255, 0), 3)
                # cv2.circle(masked_image, center, 2, (0, 0, 255), 3)
                return center
            



# dedecter = CylinderDedecter()


# while True:
#     dedecter.calculateCenter(cv2.imread('testbild_Color.png'))