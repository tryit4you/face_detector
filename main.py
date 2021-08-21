# This is a sample Python script.
from kivymd.app import MDApp
from kivymd.toast.kivytoast.kivytoast import Toast
from kivymd.uix import screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
import cv2
from kivy.uix.image import Image
import sqlite3
from kivy.graphics.texture import Texture
from kivymd.toast import toast
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.screen import Screen
faceDetect=cv2.CascadeClassifier('resources/haarcascade_frontalface_default.xml');
id=0
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (203,23,252)
cam=cv2.VideoCapture(0);
rec=cv2.face.LBPHFaceRecognizer_create();
rec.read("resources/trainningData.yml")

#xem profile hien tai trung voi profile id tiep theo ko
#neu trung se ko hien thi thong bao nua
current_profile_id=0
class KivyCamera(Image):
    current_profile_id=0
    def __init__(self,capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.current_profile_id=current_profile_id;
        Clock.schedule_interval(self.update, 1.0 / fps)

    def toast_show(self,profile):
        if(int(profile[0])!=self.current_profile_id):
            toast("Chào buổi sáng "+ str(profile[1])+"\n"+"Đơn vị:" +str(profile[4]),background=[85/255,86/255,1,1])
        self.current_profile_id=int(profile[0])

    def update(self, dt):
        ret,img=cam.read();
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray,1.3,5);
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            #get profile info
            conn=sqlite3.connect("FaceBase.db")
            cmd="SELECT * FROM People WHERE ID="+"'"+str(id)+"'"
            cursor=conn.execute(cmd)
            profile=None
            for row in cursor:
                profile=row
            self.toast_show(profile)
            conn.close()

            #if(profile!=None):
             #  print(profile)
                #self.profile=profile
        ret,frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()

            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

class FaceDetectorApp(MDApp):
    def build(self):
        screen =Screen()
        self.image=Image()
        layout=MDBoxLayout(orientation='vertical')
        #layout.add_widget(self.image)
        
        self.capture=cam
        self.my_camera= KivyCamera(capture=self.capture, fps=30)
        
        layout.add_widget(self.my_camera)
        icon_button=MDFloatingActionButton(icon='account',pos_hint={'center_x':0.9,'center_y':0.1})
        screen.add_widget(icon_button)
        layout.add_widget(screen)
        return layout
    def on_stop(self):
            #without this, app will not exit even if the window is closed
        self.capture.release()
FaceDetectorApp().run()
