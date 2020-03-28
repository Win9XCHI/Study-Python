import os
import socket
import keyboard
import uploader
import pickle

if __name__ == '__main__':
    path = "my_directory/"
    files_list = os.listdir(path)

    ObjectProgress = uploader.progress(files_list)
    sock = socket.socket()
    sock.bind(('', 9432))
    sock.listen(len(files_list))

    uploader = uploader.Uploader(files_list, len(files_list))
    uploader.start()

    keyboard.hook(uploader.killAllProcess)
    while uploader.is_active():
        conn, addr = sock.accept()
        data = conn.recv(1024)
        data = pickle.loads(data)
        if data["bool"] == True:
            ObjectProgress.AddDone(data["data"])
        else:
            ObjectProgress.AddError(data["data"])
        print(ObjectProgress.GetDone(), ObjectProgress.GetError(), ObjectProgress.GetTotal())

    print("Done uploaded:")
    print(ObjectProgress.GetDone())
    print("Error uploaded:")
    print(ObjectProgress.GetError())

    raise SystemExit
