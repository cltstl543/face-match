import tkinter as tk
from tkinter import filedialog

def get_user_inputs():
    window = tk.Tk()

    window.title('face-match')  # 创建窗口
    size = window.maxsize()  # 获取终端分辨率
    k, g = size
    print(k, g)
    window.geometry(f'{int(k * 0.5)}x{int(g * 0.5)}')  # 界面大小

    window.resizable(False, False)  # 锁定界面大小
    window.iconbitmap('favicon.ico')  # 窗口图标
    window.attributes('-topmost', True)  # 窗口置顶

    tk.Label(window, text='匹配目录地址:', font=('黑体', int(k * 0.012))).place(x=k * 0.03, y=g * 0.05)
    location_1 = tk.StringVar()
    Entry_1 = tk.Entry(window, textvariable=location_1, width=int(k * 0.045))
    Entry_1.place(x=k * 0.15, y=g * 0.05)  # 匹配目录输入框

    # 添加选择目标文件夹的按钮
    def select_image_directory():
        # 打开文件夹选择对话框，限制用户只能选择文件夹
        directory = filedialog.askdirectory(title="选择匹配目录")
        location_1.set(directory)  # 将选择的文件夹路径设置到输入框中

    tk.Button(window, text="选择匹配目录", command=select_image_directory).place(x=k * 0.05, y=g * 0.085)  # 添加选择匹配目录的按钮

    tk.Label(window, text='目标图片地址:', font=('黑体', int(k * 0.012))).place(x=k * 0.03, y=g * 0.13)
    location_2 = tk.StringVar()
    Entry_2 = tk.Entry(window, textvariable=location_2, width=int(k * 0.045))
    Entry_2.place(x=k * 0.15, y=g * 0.13)  # 目标图片输入框

    def select_target_images():
        # 打开文件选择对话框，允许用户选择多张图片
        target_images = filedialog.askopenfilenames(title="选择目标人物的多张照片", filetypes=[("Image Files", "*.jpg *.png")])
        location_2.set(",".join(target_images))  # 将选择的文件路径用逗号分隔并设置到输入框中

    tk.Button(window, text="选择目标图片", command=select_target_images).place(x=k * 0.05, y=g * 0.17)  # 添加选择目标图片的按钮

    def on_button_click():
        # 获取用户输入的匹配目录和目标图片路径
        images = location_1.get()  # 匹配目录（文件夹路径）
        target_person = location_2.get().split(",")  # 将目标图片路径拆分为列表
        window.quit()  # 关闭窗口
        return target_person, images  # 返回目标图片路径和匹配目录

    tk.Button(window, command=on_button_click, text='match', font=('黑体', int(k * 0.01)), width=int(k * 0.01)).place(x=k * 0.2, y=g * 0.4)  # 匹配按钮

    window.mainloop()

    # 返回目标图片路径和匹配目录
    return on_button_click()