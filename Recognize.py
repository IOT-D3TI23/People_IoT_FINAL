import datetime
import os
import time
import cv2
import pandas as pd

def recognize_attendence():
    try:
        # Load recognizer and face cascade
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("./TrainingImageLabel/Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        
        if not os.path.exists(harcascadePath):
            print("Kesalahan: File Haarcascade tidak ditemukan.")
            return
        
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        
        # Read Data Mahasiswa
        student_details_path = "DataMahasiswa" + os.sep + "DataMahasiswa.csv"
        if not os.path.exists(student_details_path):
            print(f"Kesalahan: File detail siswa tidak ditemukan di {student_details_path}.")
            return
        
        df = pd.read_csv(student_details_path)
        
        # Initialize attendance DataFrame
        col_names = ['Id', 'Name', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)
        
        # Initialize camera
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Kesalahan: Kamera tidak bisa dibuka.")
            return
        
        cam.set(3, 640)  # Set video width
        cam.set(4, 480)  # Set video height
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)
        
        # Timeout settings
        start_time = time.time()
        time_limit = 30  # Timeout after 30 seconds
        attendance_recorded = False  # Flag to check attendance status
        
        # Font for display
        font = cv2.FONT_HERSHEY_SIMPLEX

        while True:
            ret, im = cam.read()
            if not ret:
                print("Kesalahan: Gagal mengambil frame.")
                break
            
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray, 1.2, 5, minSize=(int(minW), int(minH)), flags=cv2.CASCADE_SCALE_IMAGE)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                
                if conf < 100:
                    aa = df.loc[df['Id'] == Id]['Name'].values
                    confstr = "  {0}%".format(round(100 - conf))
                    tt = str(Id) + "-" + str(aa)
                else:
                    Id = 'Unknown'
                    tt = str(Id)
                    confstr = "  {0}%".format(round(100 - conf))
                
                # Record attendance if confidence > 60%
                if (100 - conf) > 60:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = str(aa)[2:-2]  # Clean up the name string
                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                    print(f"Kehadiran yang tercatat : {Id}, {aa}, {date}, {timeStamp}")
                    attendance_recorded = True
                
                tt = str(tt)[2:-2]
                if (100 - conf) > 60:
                    tt = tt + " [Pass]"
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                
                # Display confidence level
                color = (0, 255, 0) if (100 - conf) > 60 else (0, 0, 255)
                cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, color, 1)
            
            # Check timeout
            elapsed_time = time.time() - start_time
            if elapsed_time > time_limit and not attendance_recorded:
                cv2.putText(im, "Kamu belum terdaftar!", (100, 100), font, 1, (0, 0, 255), 2)
                print("Waktu habis - Kamu belum terdaftar!")
                break
            
            # Break loop if attendance recorded
            if attendance_recorded:
                break
            
            # Show webcam feed
            cv2.imshow('Attendance', im)

            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Save attendance
        if attendance_recorded:
            try:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
                fileName = f"Kehadiran{os.sep}DaftarHadir_{date}.csv"

                if not os.path.exists("Kehadiran"):
                    os.makedirs("Kehadiran")  # Create directory if not exists

                # Check if the file already exists
                if os.path.isfile(fileName):
                    # If the file exists, append the new data to the existing file
                    attendance.to_csv(fileName, mode='a', header=False, index=False)
                    print(f"Kehadiran berhasil dicatat!")
                else:
                    # If the file doesn't exist, create a new one and write the data
                    attendance.to_csv(fileName, mode='w', header=True, index=False)
                    print(f"Kehadiran berhasil dicatat!")
            except Exception as e:
                print(f"Gagal menyimpan kehadiran : {e}")
        
        cam.release()
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        if 'cam' in locals():
            cam.release()
        cv2.destroyAllWindows()

# Call the function
recognize_attendence()
