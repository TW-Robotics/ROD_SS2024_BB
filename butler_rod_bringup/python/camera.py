import pyrealsense2 as rs
import numpy as np
import cv2 as cv
import time
import geometry_msgs.msg

class camera:
    def __init__(self):
        
        #Hier eintragen wo rot und grün ist (Weltkoordinaten in Meter)
        self.x_rot_world = 0.47012
        self.y_rot_world = 0.43683
        self.x_gruen_world = 0.62080
        self.y_gruen_world = 0.43684
        
        
        #Realsense Init (wenn Kamera nicht vorhanden auskommentieren)
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        time.sleep(0.1)
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper) 

    def foto(self):
        

        self.config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
        self.pipeline.start(self.config)
    
        sensor = self.pipeline.get_active_profile().get_device().query_sensors()[1]
        sensor.set_option(rs.option.gain, 64)
        sensor.set_option(rs.option.enable_auto_exposure, True)
        sensor.set_option(rs.option.enable_auto_white_balance, True)
    
        time.sleep(2)
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        
        return color_image
        
    def saveFoto(self,foto):
       
        if foto is not None:
            print("Foto gespeichert unter bild.png")	
            cv.imwrite("bild.png",foto)
            
            
    def loadFoto(self,pfad):
        foto = cv.imread(pfad)
        return foto             

    def returnPose(self,foto):
    
        help = 0
        
        #Initialisieren Ziel Pose Gelber Zylinder
        goal = geometry_msgs.msg.Pose()
        goal.position.x = 0.4870
        goal.position.y = 0.1105
        goal.position.z = 0.4309
        goal.orientation.x = 0.707
        goal.orientation.y = -0.707
        goal.orientation.z = 0
        goal.orientation.w = 0
        
          
        #Masken für Erkennung
        l_rot1 = np.array([0, 70, 50]) 
        h_rot1 = np.array([5, 191, 255])
        
        l_rot2 = np.array([175, 70, 50]) 
        h_rot2 = np.array([180, 191, 255])

        l_gelb = np.array([18, 120, 50]) 
        h_gelb = np.array([26, 255, 255])
        
        l_gruen = np.array([72, 100, 50]) 
        h_gruen = np.array([80, 220, 255])
        
        #Kernel
        kernelsize = 5        
        
        #Bearbeiten
        hsv = cv.cvtColor(foto, cv.COLOR_BGR2HSV)
        
        maske_rot1 = cv.inRange(hsv, l_rot1, h_rot1)
        maske_rot2 = cv.inRange(hsv, l_rot2, h_rot2)
        maske_rot = cv.bitwise_or(maske_rot1,maske_rot2)
        
        
        
        maske_gelb = cv.inRange(hsv, l_gelb, h_gelb)
        maske_gruen = cv.inRange(hsv, l_gruen, h_gruen)
        
        maske_rot = cv.medianBlur(maske_rot, kernelsize)
        maske_gelb = cv.medianBlur(maske_gelb, kernelsize)
        maske_gruen = cv.medianBlur(maske_gruen, kernelsize)
        
        maske_rot = cv.erode(maske_rot, np.ones((kernelsize, kernelsize), np.uint8))
        maske_gelb = cv.erode(maske_gelb, np.ones((kernelsize, kernelsize), np.uint8))
        maske_gruen = cv.erode(maske_gruen, np.ones((kernelsize, kernelsize), np.uint8))
        
        #cv.imshow('fenster1', maske_rot)
        #cv.imshow('fenster2', maske_gelb)
        #cv.imshow('fenster3', maske_gruen)
        cv.imwrite("maske_gruen.png",maske_gruen)
        cv.imwrite("maske_gelb.png",maske_gelb)
        cv.imwrite("maske_rot.png",maske_rot)
        #cv.waitKey(10000)
        #cv.destroyAllWindows()
        
        
        konturen_rot,_ = cv.findContours(maske_rot, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        konturen_gruen,_ = cv.findContours(maske_gruen, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        
        if konturen_rot is not None and konturen_gruen is not None:
            #print(konturen_rot)
            #print("Teiler")
            #print(konturen_gruen)
        
            for r in konturen_rot:
                #print("Rote Konturenfläche: ",cv.contourArea(r))
                if (cv.contourArea(r) > 500):
                    approx_rot = cv.approxPolyDP(r, 0.004*cv.arcLength(r, True), True)
                    moments_rot = cv.moments(approx_rot)
                    X_rot = int(moments_rot["m10"] / moments_rot["m00"])
                    Y_rot = int(moments_rot["m01"] / moments_rot["m00"])
                    center_rot = (X_rot, Y_rot)
                    cv.circle(foto, center_rot, 1, (0, 255, 255), 3)
                    help = help + 1
            
            for g in konturen_gruen:
                #print("Gruene Konturenfläche: ",cv.contourArea(g))
                if (cv.contourArea(g) > 500):
                    approx_gruen = cv.approxPolyDP(g, 0.004*cv.arcLength(g, True), True)
                    moments_gruen = cv.moments(approx_gruen)
                    X_gruen = int(moments_gruen["m10"] / moments_gruen["m00"])
                    Y_gruen = int(moments_gruen["m01"] / moments_gruen["m00"])
                    center_gruen = (X_gruen, Y_gruen)
                    cv.circle(foto, center_gruen, 1, (0, 255, 255), 3)
                    help = help + 1
        
        
        circles = cv.HoughCircles(maske_gelb, cv.HOUGH_GRADIENT, 1, 1000, param1=20, param2=10, minRadius=30, maxRadius=60)
        if circles is not None:
            print("Objekt gefunden")
            #print(circles)
            center = (int(circles[0][0][0]), int(circles[0][0][1]))
            #print(center)
            for i in circles[0, :]:
                center = (int(i[0]), int(i[1]))
                cv.circle(foto, center, 1, (0, 100, 100), 3)
                radius = int(i[2])
                cv.circle(foto, center, radius, (255, 0, 255), 3)
                help = help + 1
            #cv.imshow('fenster1', foto)
            cv.imwrite("bild_erkannt.png",foto)
            #cv.waitKey(5000)
            #cv.destroyAllWindows()
        else:
            print("kein Objekt gefunden")
            
        if help == 3:
            #print(center_rot)
            #print(center_gruen)
            #print(center)
            
            mmpropixel = (150/(abs(center_rot[1] - center_gruen[1])))           
            
            #print("Millimeter pro Pixel",mmpropixel)
            
                        
            y_gelb_mm = ((center_gruen[0]- center[0])  * mmpropixel)
            x_gelb_mm = ((center_gruen[1] - center[1]) * mmpropixel)
            
            x_gelb_world = self.x_gruen_world + x_gelb_mm/1000
            y_gelb_world = self.y_gruen_world + y_gelb_mm/1000
            
            goal.position.x = x_gelb_world
            goal.position.y = y_gelb_world
            goal.position.z = 0.1
            

            
            #print("X: ",x_gelb_mm)
            #print("Y: ",y_gelb_mm)
            
            
        
        else:
            print("Etwas ist schiefgelaufen!")
            
                      
        return goal
        
        
if __name__ == "__main__":
    c = camera()
    c.returnPose(c.foto())        
        


