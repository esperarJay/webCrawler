import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from fake_useragent import UserAgent  # 导入 UserAgent 类，用于生成随机的 User-Agent

def download_page(url, user_agent):
    headers = {'User-Agent': user_agent}  # 设置请求头中的 User-Agent
    response = requests.get(url, headers=headers)  # 发送带有自定义 User-Agent 的请求
    if response.status_code == 200:
        return response.content
    else:
        return None

def download_resources(url, save_path):
    user_agent = UserAgent().random  # 生成随机的 User-Agent
    page_content = download_page(url, user_agent)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        img_tags = soup.find_all('img')
        img_folder = os.path.join(save_path, 'images')
        os.makedirs(img_folder, exist_ok=True)
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url and img_url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                img_url = urljoin(url, img_url)
                img_data = download_page(img_url, user_agent)
                img_name = img_url.split('/')[-1]
                img_path = os.path.join(img_folder, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
        text_content = soup.get_text()
        text_file_path = os.path.join(save_path, 'text_content.txt')
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text_content)
        result_label.config(text="页面内容和图片已成功保存！", fg="green")
    else:
        result_label.config(text="页面请求失败！", fg="red")

def browse_folder():
    folder_path = filedialog.askdirectory()
    save_path_entry.delete(0, tk.END)
    save_path_entry.insert(0, folder_path)

def download():
    url = url_entry.get()
    save_path = save_path_entry.get()
    download_resources(url, save_path)

# 创建主窗口
root = tk.Tk()
root.title("网页内容下载器")

# 创建输入网址的标签和文本框
url_label = tk.Label(root, text="网址:")
url_label.grid(row=0, column=0, padx=10, pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

# 创建选择保存路径的标签、文本框和浏览按钮
save_path_label = tk.Label(root, text="保存路径:")
save_path_label.grid(row=1, column=0, padx=10, pady=5)
save_path_entry = tk.Entry(root, width=50)
save_path_entry.grid(row=1, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="浏览", command=browse_folder)
browse_button.grid(row=1, column=2, padx=5, pady=5)

# 创建下载按钮
download_button = tk.Button(root, text="下载", command=download)
download_button.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

# 创建结果标签
result_label = tk.Label(root, text="", fg="green")
result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# 运行窗口
root.mainloop()
