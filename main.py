import os  
import Capture_Image
import Train_Image
import Recognize


# creating the title bar function

def title_bar():
    os.system('cls')  # for windows

    # title of the program

    print("*********************************************")
    print("***** Sistem Kehadiran Pengenalan Wajah *****")
    print("*********************************************")


# creating the user main menu function

def mainMenu():
    title_bar()
    print()
    print(19 * "*", " MENU", 19 * "*")
    print("[1] Tangkap Gambar")
    print("[2] Latih Gambar")
    print("[3] Pengenalan & Catat Kehadiran")
    print("[4] Keluar")

    while True:
        try:
            choice = int(input("Masukan pilihan: "))

            if choice == 1:
                CaptureFaces()
                break
            elif choice == 2:
                Trainimages()
                break
            elif choice == 3:
                RecognizeFaces()
                break
            elif choice == 4:
                print("Terima Kasih")
                break
            else:
                print("Pilihan tidak tepat. Pilih 1-4")
                mainMenu()
        except ValueError:
            print("Pilihan tidak tepat. Pilih 1-4\n Coba lagi!")
    exit


# --------------------------------------------------------------
# calling the take image function form capture image.py file

def CaptureFaces():
    Capture_Image.takeImages()
    key = input("Klik Enter untuk kembali ke halaman Menu")
    mainMenu()


# -----------------------------------------------------------------
# calling the train images from train_images.py file

def Trainimages():
    Train_Image.TrainImages()
    key = input("Klik Enter untuk kembali ke halaman Menu")
    mainMenu()


# --------------------------------------------------------------------
# calling the recognize_attendance from recognize.py file

def RecognizeFaces():
    Recognize.recognize_attendence()
    key = input("Klik Enter untuk kembali ke halaman Menu")
    mainMenu()


# ---------------main driver ------------------
mainMenu()
