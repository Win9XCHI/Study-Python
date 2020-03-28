import os
import paramiko
import psutil
import pickle
import socket
from multiprocessing import Process, Lock

class progress(object):
    def __init__(self, files_list):
        self.done = []
        self.error = []
        self.total = files_list

    def AddDone(self, filename):
        self.done.append(filename)
        self.total.remove(filename)
        
    def AddError(self, filename):
        self.error.append(filename)
        self.total.remove(filename)

    def SetTotal(self, files_list):
        self.total = files_list

    def GetDone(self):
        return self.done

    def GetError(self):
        return self.error

    def GetTotal(self):
        return self.total


def doubler(number, files_list, lock):

    sock = socket.socket()
    sock.connect(('localhost', 9432))
    sdata = dict()
    sdata["data"] = files_list[number]
    '''
    ftp_client = self.client.open_sftp()

    try:
        lock.acquire()
        ftp_client.put ("my_directory/" + files_list[number])      
        sdata["bool"] = True
    except:
        sdata["bool"] = False
        
    finally:
        sock.send(pickle.dumps(sdata))
        sock.close()
        lock.release()

    ftp_client.close()
    '''

    lock.acquire()
    try:
        sdata["bool"] = True

    finally:
        sock.send(pickle.dumps(sdata))
        sock.close()
        lock.release()
    

class Uploader(object):
 
    def __init__(self, files_list, number):
        '''
        host = '192.168.0.8'
        user = 'login'
        secret = 'password'
        port = 22

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname = host, username = user, password = secret, port = port)
        '''

        self.files_list = files_list
        self.number = number
        self.procs = []
    
    def start(self):
        lock = Lock()
        i = self.number - 1
        
        while i != -1:
            proc = Process(target=doubler, args=(i, self.files_list, lock, ))
            self.procs.append(proc)
            proc.start()
            i -= 1

        for proc in self.procs:
            proc.join()

        '''
        self.client.close()
        '''
        return 0
    
    def is_active(self):
        for procG in psutil.process_iter():
            for proc in self.procs:
                if proc.pid == procG.pid:
                    return True
        return False

    def killAllProcess(self):
        for proc in self.procs:
            proc.terminate()