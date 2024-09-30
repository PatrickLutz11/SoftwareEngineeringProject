"""
@data:      webcam.py
@author:    Markus Hewel
@versions:  ver 1.0.0 - 20.05.2024 - Markus Hewel
@desc: 
    handel camera and take snapshot.
    also combine multiple snapshots to one image.
"""
import numpy as np
import cv2
import platform
import os
from src.graphics_service import GraphicsService

SELECTION_HEIGHT = 0

def Bild_aufnehmen(DEVICE_ID=1):    # change here, to open your preferred webcam
    
    if platform.system() == 'Windows':
        videoBackend = cv2.CAP_DSHOW
    else:
        videoBackend = cv2.CAP_ANY
    cap = cv2.VideoCapture(DEVICE_ID, videoBackend);
    
    if not cap.isOpened():
        print('ERROR: could not open webcam');
    
    # Überprüfe und drucke die maximale Auflösung der Kamera default 640x480
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3000)#1280
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)#480
    max_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    max_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Maximale Auflösung der Kamera: {max_width} x {max_height}")

    images=[]
    run=True
    while(run):
        ret, frame = cap.read()
        if not ret:
            print('ERROR: could not read data from webcam')
            break;
        scale=0.3
        frame_resize = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        cv2.imshow("'a': naechsten Ausschnitt waehlen / '0': Kamerasettings / 'q': Auswahl beenden, weiter ", frame_resize)
        ch = cv2.waitKey(20);

        if ch==ord('a'):
            image=frame.copy()
            images=Ausschnitt_wahlen(image, images)
        if ch==ord('0'):
            cap.set(cv2.CAP_PROP_SETTINGS,0);
        if ch==ord('q'):
            run=False

    cap.release()
    cv2.destroyAllWindows()
    return images

def Ausschnitt_wahlen(image, images): 
    grs = GraphicsService()
    global SELECTION_HEIGHT
    image=image.copy()  
    # Skalieren des Bildes für die Auswahl
    scale = 0.3  # Skalierungsfaktor, kann nach Bedarf angepasst werden
    small_image = cv2.resize(image, None, fx=scale, fy=scale)
    # Select a region of interest (ROI)
    roi = cv2.selectROI("Select ROI and press Enter to confirm", small_image)
    x, y, w, h = roi
    if SELECTION_HEIGHT == 0:
        SELECTION_HEIGHT = h
    #Auf Originalbild umrechnen
    x = int(x / scale)
    y = int(y / scale)
    w = int(w / scale)
    h = int(SELECTION_HEIGHT / scale)
    # Bild ausschneiden
    cropped_img = image[y:y+h, x:x+w]
    rotate=cv2.rotate(cropped_img,cv2.ROTATE_90_COUNTERCLOCKWISE)  #Bild drehen
    rotate=grs.deskew(rotate)    #Bild nach Zeile ausrichten
    img_show=cv2.resize(rotate, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    cv2.imshow("Bildausschnitt, weiter 'w'",img_show)    
    while True: #Anzeige abbrechen
        key = cv2.waitKey(0)
        if key == ord('w'):
            cv2.destroyAllWindows(); 
            break     
    images.append(rotate)
    return images

def Zusammenfugen(save_path, images):
    # Stitch images vertically
    stitched_image = None
    for img in images:
        if stitched_image is None:
            stitched_image = img
        else:
            stitched_image = cv2.vconcat([stitched_image, img])        
    # Bild abspeichern
    file_path = os.path.join(save_path, "stiched_image.tif")
    cv2.imwrite(file_path, stitched_image)
    return stitched_image