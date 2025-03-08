import tkinter as tk

def get_user_inputs():
    window = tk.Tk()

    window.title('face-match') #创建窗口
    size = window.maxsize() #获取终端分辨率
    k , g = size
    print(k,g)
    window.geometry(f'{int(k * 0.5)}x{int(g * 0.5)}') #界面大小

    window.resizable(False, False) #锁定界面大小
    window.iconbitmap('favicon.ico') #窗口图标
    window.attributes('-topmost', True) #窗口置顶



    tk.Label(window, text='匹配目录地址:', font=('黑体', int(k*0.012))).place(x=k * 0.03, y=g * 0.05)
    location_1 = tk.StringVar()
    Entry_1=tk.Entry(window, textvariable=location_1, width=int(k*0.045))
    Entry_1.place(x=k * 0.15, y=g * 0.05)                                   #匹配目录输入框


    tk.Label(window, text='目标图片地址:', font=('黑体', int(k*0.012))).place(x=k * 0.03, y=g * 0.13)
    location_2 = tk.StringVar()
    Entry_2=tk.Entry(window, textvariable=location_2, width=int(k*0.045))
    Entry_2.place(x=k * 0.15, y=g * 0.13)       #目标图片输入框



    def on_button_click():
        global images
        images = location_1.get()
        global target_person
        target_person = location_2.get()
        window.quit()


    tk.Button(window,command=on_button_click,text='match',font=('黑体' , int(k*0.01)), width=int(k*0.01)).place(x=k * 0.2, y=g * 0.4)  #匹配按钮

    window.mainloop()

    return target_person, images