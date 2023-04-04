import socket
import threading
import time
import tkinter as tk
from tkinter import ttk
import json
import requests
import time as time
import os



HOST = ""
PORT = 5050
FORMAT = "utf-8"
DICONNECT_MESSAGE = "DISCONNECT"
SIGN_UP = "1"
SIGN_IN = "2"
CHECK_WORLD = "3"
CHECK="4"
SoClient = 10


#hàm gởi list
def sendList(conn, list): 
    for item in list:
        conn.sendall(item.encode(FORMAT))
        conn.recv(1024)
    end="end"
    conn.send(end.encode(FORMAT))


#hàm nhận list
def recvList(conn):
    list = []
    
    item = conn.recv(1024).decode(FORMAT)
    
    while item != "end":
        list.append(item)
        
        conn.sendall(item.encode(FORMAT))
        item=conn.recv(1024).decode(FORMAT)
        
    return list

global dcn_btn
global refresh_btn
global disconnect 
disconnect = False
global socli
socli=0
global ktall
ktall=[]

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()
        
    def run(self): 
        getCovidData()
        with open("Account_Connected.json") as file:
            file_data = json.load(file)
            for i in range(-1,len(file_data["username"])-1):
                del file_data["username"][0]
                del file_data["pass"][0]
                del file_data["address"][0]
            file.close()
            with open("Account_Connected.json", "w") as data_file:
                data = json.dump(file_data, data_file, indent=3)
                file.close()   
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.resizable(False,False)
        self.window.title("Server")

        global client_box
        global log_box
        client_box = tk.Listbox(self.window,width=40,height=20,font = ("Times New Roman", 10),bg='#F5F5DC',fg='#000000')
        log_box = tk.Text(self.window,width=41,height=21,font = ("Times New Roman", 10),bg='#F5F5DC')

        log=tk.Label(self.window, text = "Nhật ký kết nối:",font = ("Times New Roman", 15))
        cli=tk.Label(self.window, text = "Tài khoản đang hoạt động:",font = ("Times New Roman", 15))

        #
        log_box.config(state='normal'),
        log_box.insert('end',"[LISTENING] SERVER IS LISTENING ON:"+'\n'+str(HOST)+'\n')
        log_box.insert('end',"WAITING FOR CLIENT"+'\n')
        log_box.config(state='disable')
        #
        global dcn_btn
        refresh_btn = tk.Button(
            self.window,
            text="Làm mới",
            bg='#E0E0E0',
            command=
            lambda:[  
                print_account_connecting()
            ]
        )
        
        dcn_btn = tk.Button(
            self.window,
            text="Ngắt kết nối tất cả Client",
       
            bg='#E0E0E0',
            command=
            lambda:[
                log_box.config(state='normal'),
                log_box.insert('end','Chưa kết nối với Client\n'),
                log_box.config(state='disable'),
                ]
        )
        
        cli.grid(column=0,row=0,sticky='w')
        log.grid(column=1,row=0,sticky='w')
        refresh_btn.grid(column=0,row=2)
        client_box.grid(column=0,row=1)
        log_box.grid(column= 1,row= 1)
        log_box.config(state='disable')
        dcn_btn.grid(column=0,row=3)
        self.window.grid()
        
        self.window.mainloop()
        self.window.protocol("WM_DELETE_WINDOW",os._exit(0))

def print_account_connecting():
    with open("Account_Connected.json", "r+") as file:
        file_data = json.load(file)
        a=file_data["address"]
        b=file_data["username"]
        file.close()
    client_box.delete(0,client_box.size())

    for i in range(0,len(a)):
        client_box.insert('end',"User : "+b[i])
        client_box.insert('end',"Address: "+a[i],'\n' )
        client_box.itemconfig(i*3, {'fg': '#8A2BE2'})

global arrarr
arrarr=[]

def trydcn(ktall,arrarr,dcn_btn,log_box):
    try:
        all1(ktall,arrarr),
        print_account_connecting()
    except:
        pass

def all1(ktall,arrarr):
    with open("Account_Connected.json") as file:
        file_data = json.load(file)
        file.close()
        while (file_data["username"]):
            del file_data["username"][0]
            del file_data["pass"][0]
            del file_data["address"][0]

    with open("Account_Connected.json", "w") as data_file:
        data = json.dump(file_data, data_file, indent=3)
        file.close()

    while (ktall):
            ktall[0].close()
            del ktall[0]

def handle_client(conn : socket, addr,dcn_btn):
    log_box.config(state='normal'),
    log_box.insert('end',"client address: "+str(addr)+" connected\n"),
    log_box.config(state='disable')
    option=""
    ktall.append(conn)
    arrarr.append(addr)
    dcn_btn.config(command=lambda:[
               trydcn(ktall,arrarr,dcn_btn,log_box)
            ])
    
    try:
        while True:

            
            option = conn.recv(1024).decode(FORMAT)
            if  option == SIGN_UP:
                account = recvList(conn)
                user, pswd = account
                account = manageAccount(user, pswd)
                check1 = manageAccount.checkSignupAccount(account)
                if check1=='1':
                    conn.sendall("1".encode(FORMAT))
                    account.createAccount() #them acc vao file account
                else:
                    conn.sendall('0'.encode(FORMAT))    
            if  option == SIGN_IN:
                account = recvList(conn)
                user, pswd = account
                if user==' ' and pswd==' ':
                    removeExistenceAccount(addr)
                    print_account_connecting()
                a=manageAccount(user, pswd)
                k=manageAccount.checkAccount(a)
                if k=='1' :                
                    conn.sendall("1".encode(FORMAT))
                    manageAccount(user, pswd).save_Created_Account(str(addr)) #them acc vao file conected account
                    print_account_connecting()
                elif k=='2':
                    conn.sendall("2".encode(FORMAT))
                else: 
                    conn.sendall('0'.encode(FORMAT))

            if  option == CHECK_WORLD:
                a1=takeCountryData()
                sendList(conn,a1)
            
            if option==CHECK:
                received_Country_Name = conn.recv(1024).decode(FORMAT)
                conn.sendall("100".encode(FORMAT))
                nameCountry = received_Country_Name
                dataCovid = manageData(nameCountry,"covid_Infor.json")
                newConfirmed = dataCovid.NewConfirmed()
                totalConfirmed = dataCovid.TotalConfirmed()
                newDeaths = dataCovid.NewDeaths()
                totalDeaths = dataCovid.TotalDeaths()
                newRecovered = dataCovid.NewRecovered()
                totalRecovered = dataCovid.TotalRecovered()
                list_info = []
                list_info=[str(newConfirmed),str(totalConfirmed),str(newDeaths),str(totalDeaths),str(newRecovered),str(totalRecovered)]
                sendList(conn,list_info)
            if option == DICONNECT_MESSAGE:
                removeExistenceAccount(addr)
                print_account_connecting()
                log_box.config(state='normal'),
                log_box.insert('end',"Disconnected to "+str(addr)+ '\n'),
                log_box.config(state='disable')  
                conn.close() 
                break
    except:
        try:
            removeExistenceAccount(addr)
        except:
            pass
        print_account_connecting()
        log_box.config(state='normal'),
        log_box.insert('end',"Disconnected to "+str(addr)+ '\n'),
        log_box.config(state='disable')
  

    
def main():
    server.listen()
    app = App()
    while True:
        try:
            conn, addr = server.accept()
            thread=threading.Thread(target=handle_client, args=(conn,addr,dcn_btn))
            thread.daemon=True
            thread.start()
            time.sleep(0.5)
        except:
            break
    input()
    server.close() 

#xử lý các thông tin về tài khoản
class manageAccount:
    def __init__(self, username, password):
        self.username = username
        self.pwd = password

    # Tạo account mới
    def createAccount(self):
        with open("Account.json", "r+") as file:
            file_data = json.load(file)
            # Gom username và pass vào 1 biến data
            data = {
                "username": self.username,
                "pass": self.pwd
            }
            # Thêm biến data vào file
            file_data.append(data)
            # Đặt lại vị trí con trỏ lên đầu file
            file.seek(0)
            # Cập nhật và lưu lại file
            json.dump(file_data, file, indent=3)
            file.close()


    def checkSignupAccount(self):
            with open("Account.json") as file:
                file_data = json.load(file)
                file.close()
            for i in range(len(file_data)):
                if self.username == file_data[i]["username"]:
                        return "0"  # account đã có trong dữ liệu
            return "1"  # account chưa có trong dữ liệu


    # Ktra account có trong dữ liệu hay chưa
    def checkAccount(self):
        with open("Account.json") as file:
            file_data = json.load(file)
            file.close()
        if self.check_Already_Account() == "1":
           # file.close()
            return "2"  # account đã kết nối với server

        for i in range(len(file_data)):
            if self.username == file_data[i]["username"]:
                if self.pwd == file_data[i]["pass"]:
                   # file.close()
                    return "1"  # account đã có trong dữ liệu
        #file.close()
        return "0"  # account chưa có trong dữ liệu

    # Lưu account mới tạo vào danh sách các account đã kết nối với server
    def save_Created_Account(self, addr):
        with open("Account_Connected.json", "r+") as file:
            file_data = json.load(file)
            file_data["username"].append(self.username)
            file_data["pass"].append(self.pwd)
            file_data["address"].append(addr)

            file.seek(0)
            json.dump(file_data, file, indent=3)
            file.close()

    # Ktra các account đã kết nối với server chưa
    def check_Already_Account(self):
        with open("Account_Connected.json") as file:
            file_data = json.load(file)
            file.close()
        for row in file_data["username"]:
            if self.username == row:
                i = file_data["username"].index(row)
                if self.pwd == file_data["pass"][i]:
        
                    return "1"
                    
        
        return "0"

# Khi ngắt kết nối thì xóa account khỏi danh sách các account đã kết nối tới server
def removeExistenceAccount(addr):
    with open("Account_Connected.json") as file:
        file_data = json.load(file)
        file.close()
    try:
        i = 0
        for row in file_data["address"]:
            if str(addr) == row:
                file_data["address"].remove(str(addr))
                break
            else:
                i = i + 1

        del file_data["username"][i]
        del file_data["pass"][i]
        #file.close()
        with open("Account_Connected.json", "w") as data_file:
            data = json.dump(file_data, data_file, indent=3)
            file.close()   
    except:
        pass


#Data of Covid
#Lấy dữ liệu trên web và lưu vào file json
def reloadapi():
    threading.Timer(3600.0, reloadapi).start()
    try:
        x = requests.get('https://api.covid19api.com/summary')
        data = x.json()
        get_data = json.dumps(data, indent=3)
        with open("covid_Infor.json", "w") as outfile:
            outfile.write(get_data)
    except:
        pass
def getCovidData():
    reloadapi()
    

#xử lý các thông tin về covid
class manageData:
    def __init__(self,name, file):
        self.check_name = name
        self.filename = file
    # Kiểm tra tên, nếu đúng thì trả về vị trí trong mảng dữ liệu
    def Country(self):
        with open(self.filename) as file:
            file_data = json.load(file)
            file.close()

        dataCovid = file_data['Countries']
        for row in range(len(dataCovid)):
            if dataCovid[row]["Country"] == self.check_name:
                return row
        return -1

    # Trả về các số liệu tương ứng với vị trí của đất nước lấy ở hàm Country
    def NewConfirmed(self):
        idx = self.Country()
        with open(self.filename) as file:
            file_data = json.load(file)
            file.close()
        dataCovid = file_data['Countries']
        return dataCovid[idx]["NewConfirmed"]

    def TotalConfirmed(self):
        idx = self.Country()
        with open(self.filename) as file:
            file_data = json.load(file)
            file.close()
        dataCovid = file_data['Countries']
        return dataCovid[idx]["TotalConfirmed"]

    def NewDeaths(self):
        idx = self.Country()
        with open(self.filename) as file:
            file_data = json.load(file)
            file.close()
        dataCovid = file_data['Countries']
        return dataCovid[idx]["NewDeaths"]

    def TotalDeaths(self):
        idx = self.Country()
        with open(self.filename) as file:
            file_data = json.load(file)
            file.close()
        dataCovid = file_data['Countries']
        return dataCovid[idx]["TotalDeaths"]

    def NewRecovered(self):
        idx = self.Country()
        with open(self.filename) as file:
            file_data = json.load(file)
            file.close()
        dataCovid = file_data['Countries']
        return dataCovid[idx]["NewRecovered"]

    def TotalRecovered(self):
        idx = self.Country()
        with open(self.filename) as file:
            file_data = json.load(file)
            file.close()
        dataCovid = file_data['Countries']
        return dataCovid[idx]["TotalRecovered"]

#lấy danh sách tên nước
def takeCountryData():
    with open("covid_Infor.json") as file:
        file_data = json.load(file)
        file.close()
    list_name = []
    dataCovid = file_data["Countries"]
    for row in range(len(dataCovid)):
        list_name.append(dataCovid[row]["Country"])
    file.close()
    return list_name

# Tra cứu thông tin covid
def lookup_Infor(conn):
    try:
        # Nhận tên đất nước và kiểm tra có hợp lệ không, nếu không thì thông báo không tồn tại tên như thế
        received_Country_Name = conn.recv(2048).decode(FORMAT)
        #conn.sendall("Received Country Name".encode(FORMAT))

        nameCountry = received_Country_Name
        dataCovid = manageData(nameCountry,"covid_Infor.json")

        check = dataCovid.Country()
        conn.sendall(str(check).encode(FORMAT))
        if check == "-1":
            return
    except Exception as e:
        print(str(e))

#lấy host ip
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host1 = socket.gethostname()
HOST = socket.gethostbyname(host1)
server.bind((HOST, PORT))   
#chạy chương trình
main()
