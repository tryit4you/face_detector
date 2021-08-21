from sqlite3.dbapi2 import Date
import cv2
import sqlite3

cam = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier("resources/haarcascade_frontalface_default.xml")


# insert/update data to sqlite
def createDataSample(Id, Name,Org,Identify):
    status=False
    conn = sqlite3.connect("FaceBase.db")
    print(conn)
    cmd = "SELECT * FROM People WHERE ID="+"'" + str(Id)+"'"
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if (isRecordExist == 1):
        cmd = "UPDATE People SET Name=" + "'" + str(Name) + "'" + " WHERE ID=" + str(Id)
    else:
        cmd = "INSERT INTO People(Id,Name,Organization,Identify) Values("+"'" + str(Id)+"'" + "," +  "'"+str(Name)+ "'"+"," +  "'"+str(Org)+"'"+ "," +  "'"+str(Identify) + "'"+ ")"
    print(cmd)
    conn.execute(cmd)
    conn.commit()
    is_insert_or_update=True;
    conn.close()
    status=True

    return (status,Id)

def diemDanhNgay(Id,UserId,Name,Org,Ngay):
    status=False
    conn = sqlite3.connect("FaceBase.db")
    print(conn)
    cmd = "SELECT * FROM DiemDanh WHERE UserId="+"'" + str(UserId)+"'"
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if (isRecordExist == 0):
        cmd = "INSERT INTO DiemDanh(ID,UserId,UserName,ThoiGian,Org) Values("+"'"+ str(Id)+"'" + "," + "'"+str(UserId)+ "'"+","+ "'"+str(Name)+ "'"+"," +"'"+str(Ngay)+ "'"+"," +  "'"+str(Org) + "'"+ ")"
    print(cmd)
    conn.execute(cmd)
    conn.commit()
    is_insert_or_update=True;
    conn.close()
    status=True

    return (status,Id)


def getSample(id):
    sampleNum = 0
    while (True ):
        # camera read
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # incrementing sample number
            sampleNum = sampleNum + 1
            # saving the captured face in the dataset folder
            cv2.imwrite("resources/dataSet/User." + str(id) + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            print("write success: "+ str(sampleNum))
            cv2.imshow('frame', img)
        # wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 20
        elif sampleNum > 10:
            break
    cam.release()
    cv2.destroyAllWindows()
