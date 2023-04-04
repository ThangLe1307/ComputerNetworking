import tkinter as tk
from tkinter import ttk
import socket
import time
import time as time

HOST = ""
PORT = 5050
FORMAT = "utf-8"
DICONNECT_MESSAGE = "DISCONNECT"
SIGN_UP = "1"
SIGN_IN = "2"
CHECK_WORLD = "3"
CHECK="4"
 
client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def dcn():
    window1 = tk.Tk()
    window1.geometry("400x200")
    window1.resizable(False,False)
    window1.title("Error")
    aa=tk.Label(window1,text="không thể kết nối với server",font=(10))
    aa1=tk.Label(window1,text="Vui lòng tắt Client và mở lại!",font=(10))
    aa.pack()
    aa1.pack()
    window1.mainloop()

def log_out():
    time.sleep(0.1)
    l = [' ', ' ']
    try:
        #sẽ không thể đăng nhập bằng " ", " "
        #đây là tín hiệu đăng xuất
        #khi ấn nút đăng xuất sẽ gởi " ", " "
        client.sendall(SIGN_IN.encode(FORMAT))
    except:
        dcn()
        window.destroy()
    #gởi list [' ', ' ']
    sendList(client, l)
    client.recv(1024)

#Ham gui 1 list qua server
def sendList(client, list): 
    for item in list:
        client.sendall(item.encode(FORMAT))
        client.recv(1024)
    end="end"
    client.send(end.encode(FORMAT))
#hàm nhận 1 list
def recvList(client):
    list = []
    
    item = client.recv(1024).decode(FORMAT)
    
    while item != "end":
        list.append(item)
        
        client.sendall(item.encode(FORMAT))
        item=client.recv(1024).decode(FORMAT)
        
    return list


def Check_conecton(IP_in,cur_frame,err):
    text=IP_in.get()

    if text!="":
        try:    
            
            client.connect((text,PORT))

            cur_frame.destroy()
            login_fr()
        except :
            err["text"]="Không thể kết nối đến Sever!"
def Conection_fr():
    Conection_frame=tk.Frame(window,bg='#F5F5DC')
    hi=tk.Label(Conection_frame,text="Nhập IP Sever cần kết nối:",font=(10),bg='#F5F5DC')
    IP_in=tk.Entry(Conection_frame,font=(10))
    err=tk.Label(Conection_frame,text="",bg='#F5F5DC')
    cn_btn = tk.Button(
    Conection_frame,
    text="Kết nối",
    bg='#E0E0E0',
    font=(10),
    command=
    lambda:[

        Check_conecton(IP_in,Conection_frame,err)

      ]
)

    hi.pack()
    IP_in.pack()
    cn_btn.pack()
    err.pack()
    Conection_frame.pack()

def check_world(client):
    try:

        #gởi tín hiệu để lấy thông tin tên nước
        client.sendall(CHECK_WORLD.encode(FORMAT))
    except:
        dcn()
    #nhận danh sách tên nước
    listCountry=[]
    listCountry=recvList(client)
    return listCountry

#chạy Frame trang chủ
def home_fr():
    home=tk.Frame(window,bg='#F5F5DC')
    hi=tk.Label(home,text="Trang chủ",bg='#F5F5DC',font=(10))
    hi1=tk.Label(home,text="",bg='#F5F5DC',font=(10))
    hi2=tk.Label(home,text="",bg='#F5F5DC',font=(10))
    log_out_btn = tk.Button(
    home,
    bg='#E0E0E0',font=(10),
    text="Đăng xuất",
    command=
    lambda:[home.destroy(),log_out(),login_fr()]
    )
    vn_btn = tk.Button(
    home,
    bg='#E0E0E0',font=(10),
    text="kiểm tra số liệu covid trên thế giới",
    command=
    lambda:[home.destroy(),vn_fr()]
    )
    hi.pack()
    hi1.pack()
    vn_btn.pack()
    hi2.pack()
    log_out_btn.pack()
    home.pack()
 
def check_login(client, user,password,current_frame,next_frame,err):
    ten=user.get()
    mk=password.get()
    if (ten==' ' and mk==' ') or ten=='' or mk=='':
        err["text"]="Không được chứa dấu cách hoặc để rỗng!"
    else:
        try:
            #gởi tín hiệu muốn đăng nhập
            client.sendall(SIGN_IN.encode(FORMAT))
        except:
            dcn()
        account = []
        
    #gởi tên đăng nhập và , mật khẩu
        account.append(ten)
        account.append(mk)  # account[ten, mk]
        sendList(client, account) # ham gui list qua server
        res = client.recv(1024).decode(FORMAT)
        if  res == '1':
            current_frame.destroy()
            next_frame()
        elif res == '2':
            err["text"]="Tài khoản đang được đăng nhập ở nơi khác"
        else:
            err["text"]="Sai thông tin đăng nhập"
            
 
def disconnect():
    try:
        #gởi tín hiệu ngắt kết nối
        client.sendall(DICONNECT_MESSAGE.encode(FORMAT))
        
    except:
        dcn()
    

def login_fr():
    log_frame=tk.Frame(window,bg='#F5F5DC')
    user=tk.Label(log_frame,text="Tên đăng nhập",bg='#F5F5DC',font=(10))
    password=tk.Label(log_frame,text="Mật khẩu",bg='#F5F5DC',font=(10))
    err=tk.Label(log_frame,text="",bg='#F5F5DC',font=(10))
    intry=tk.Entry(log_frame,font=(10))
    intry1=tk.Entry(log_frame,font=(10))
    button = tk.Button(
    log_frame,bg='#E0E0E0',font=(10),
    text="Đăng nhập",
    width=10,
    command=lambda:[
        check_login(client,intry,intry1,log_frame,home_fr,err)]
    )  
    signup = tk.Button(
    log_frame,
    bg='#E0E0E0',font=(10),
    text="Đăng ký",
    width=10,
    command=lambda:[ signup_fr(), log_frame.destroy()]
    )  
    dcn_btn = tk.Button(
    log_frame,
    bg='#E0E0E0',font=(10),
    text="Ngắt kết nối",
    width=10,
    command=
    lambda:[ # gởi tín hiệu disconect  
    des(),
    disconnect()
    ]
)
    user.pack()
    intry.pack()
    password.pack()
    intry1.pack()
    err.pack()
    button.pack()
    signup.pack()
    dcn_btn.pack()
    log_frame.pack()


def check_signup(client, user, password, err):
    ten=user.get()
    mk=password.get()
    if (ten==' ' and mk==' ') or ten =='' or mk=='':
        err["text"]="Không được chứa dấu cách hoặc để rỗng!"
    else:
        try:
            #gởi tín hiêu đăng ký
            client.sendall(SIGN_UP.encode(FORMAT))
        except:
            dcn()

        account = []
        
    #gởi  tên đăng nhập và mật khẩu
        account.append(ten) # account[ten]
        account.append(mk)
        sendList(client, account)
    #sever kiểm tra thông tin đăng ký
    # Server kiem tra co trung ten ko. Quy dinh phan hoi 0: trung, 1: khong trung
    #nhận [kết quả(0 hoặc 1)]
        res = client.recv(1024).decode(FORMAT)
        if  res == '1':
            err["text"]="Đăng ký thành công!"
        else:
            err["text"]="Tên đăng nhập đã được sử dụng"
 
 
 
def signup_fr():
    signup_frame=tk.Frame(window,bg='#F5F5DC')
    user=tk.Label(signup_frame,text="Tên đăng nhập",bg='#F5F5DC',font=(10))
    password=tk.Label(signup_frame,text="Mật khẩu",bg='#F5F5DC',font=(10))
    err=tk.Label(signup_frame,text="",bg='#F5F5DC',font=(10))
    intry=tk.Entry(signup_frame,font=(10))
    intry1=tk.Entry(signup_frame,font=(10))
    signup = tk.Button(
    signup_frame,
    bg='#E0E0E0',font=(10),
    text="Đăng ký",
    width=10,
    command=lambda: [
        check_signup(client,intry, intry1, err)
        ]
 
)  
    back_btn = tk.Button(
    signup_frame,
    text="Quay lại",
    bg='#E0E0E0',font=(10),
    width=10,
    command=
    lambda:[signup_frame.destroy(),login_fr()]
)
    user.pack()
    intry.pack()
    password.pack()
    intry1.pack()
    err.pack()
    signup.pack()
    back_btn.pack()
    signup_frame.pack()
 
 
def show_covid_info(label,btn,T):
    text = btn.get()
  
    if text != "":
        list = []
        try:
            #gởi tín hiệu muốn check thông tin covid
            client.sendall(CHECK.encode(FORMAT))
            #gởi tiếp tên quốc gia
            time.sleep(0.01)
            client.sendall(text.encode(FORMAT))
        except:
            dcn()
        client.recv(1024)
        #nhận thông tin covid
        list = recvList(client)
        T.config(state='normal')
        T.delete('0.0', tk.END)

        newConfirmed, totalConfirmed, newDeaths, totalDeath, newRecovered, totalRecovered =list

        #hiển thị kết quả nhận được
        label["text"]="thông tin COVID tại "+text+": "
        T.insert('end', 'Số ca nhiễm mới: '+newConfirmed+'\n')
        T.insert('end', 'Tổng số ca nhiễm: '+totalConfirmed+'\n')
        T.insert('end', 'Số ca tử vong mới: '+newDeaths+'\n')
        T.insert('end', 'Tổng số ca tử vong: '+totalDeath+'\n')
        T.insert('end', 'Số ca phục hồi mới: '+newRecovered+'\n')
        T.insert('end', 'Tổng số ca phục hồi: '+totalRecovered+'\n')
        T.config(state='disabled')
   
 
#chạy Frame tra cứu thông tin
def vn_fr():
    vn_frame=tk.Frame(window,bg='#F5F5DC')
    tk.Label(vn_frame, text = "Chọn quốc gia:", font = (10),bg='#F5F5DC').grid(column=0,row=0)
    n = tk.StringVar()
    countrychoosen = ttk.Combobox(vn_frame, width = 15,textvariable = n,state='readonly',font=(10))
    label = tk.Label( vn_frame ,bg='#F5F5DC',font=(5), text = "" )
    T = tk.Text(vn_frame, height = 14, width = 45,font = (10))
    country = []


    #lấy thông tin tên nước bằng hàm check_world
    country=check_world(client)
  

    countrychoosen['values'] = country
    check_btn = tk.Button( vn_frame,font=(10),bg='#E0E0E0' , text = "Kiểm tra" ,height=1, command =lambda:[show_covid_info(label,countrychoosen,T)] )
    T.grid(column=0,row=4)
    back_btn = tk.Button(
    vn_frame,
    bg='#E0E0E0',
    font=(10),
    text="Quay lại",
    command=
    lambda:[vn_frame.destroy(),home_fr()]
    )
    countrychoosen.grid(column=0,row=1)
    countrychoosen.current(0)
    check_btn.grid(column=0,row=2)
    label.grid(column=0,row=3)
    back_btn.grid(column=0,row=5)
    vn_frame.grid(sticky='e')
    


def des():
    global window
    window.destroy()


#chạy chương trình
try:
    global window
    window = tk.Tk()
    window.geometry("500x500")
    window.resizable(False,False)
    window.title("Client")
    window.config(bg='#F5F5DC')
    Conection_fr()
    
    window.mainloop()
    try: 
        client.sendall(DICONNECT_MESSAGE.encode(FORMAT))
    except:
        pass
except:
    pass


 
