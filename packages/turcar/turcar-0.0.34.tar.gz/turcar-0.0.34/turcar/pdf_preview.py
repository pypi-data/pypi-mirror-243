from tkinter import messagebox

from turcar import get_workbench, tktextext, ui_utils
from turcar.ui_utils import scrollbar_style
import tkinter as tk
from pdf2image import convert_from_path
from PIL import ImageTk, Image

class PdfView(tktextext.TextFrame):
    def __init__(self, master):
        tktextext.TextFrame.__init__(
            self,
            master,
            vertical_scrollbar_style=scrollbar_style("Vertical"),
            horizontal_scrollbar_style=scrollbar_style("Horizontal"),
            horizontal_scrollbar_class=ui_utils.AutoScrollbar,
            read_only=True,
            font="TkDefaultFont",
            padx=10,
            pady=0,
            insertwidth=0,
        )
        self.title = 'pdf预览'
        self.pages = None
        self.current_page_number = 0
        self.current_page_image = None
        self.image_label = None
        self.prev_page_button = None
        self.next_page_button = None
        self.pdf_name = None
        get_workbench().bind("PdfView", self.show_browser)
        get_workbench().bind("HideView", self.hidden_browser)

    def hidden_browser(self, event):
        # self.unbind("PdfView")
        self.unbind("HideView")
        get_workbench().get_view("PdfView").destroy()
        get_workbench().add_view(PdfView, self.title, "se", visible_by_default=False)
    def re_size(self):
        screen_height = self.winfo_screenheight()
        image_height = min(800, screen_height * 0.8)  # 占用80%的屏幕高度
        p_h = screen_height * 0.8
        w = self.pages[self.current_page_number].size[0]
        h = self.pages[self.current_page_number].size[1]
        resized_image = self.pages[self.current_page_number].resize((int(w / (h / image_height)), int(p_h)),
                                                                    Image.LANCZOS)
        return resized_image
    def show_browser(self, event):
        path = event.content
        self.pages = convert_from_path(path)
        self.current_page_number = 0
        self.current_page_image = ImageTk.PhotoImage(self.re_size())
        self.image_label = tk.Label(self.text, image=self.current_page_image)
        self.image_label.grid(row=1, column=0, columnspan=3)

        # 创建“上一个”和“下一个”按钮
        self.prev_page_button = tk.Button(self.text, text="上一页", command=self.prev_page)
        self.prev_page_button.grid(row=0, column=0)

        self.next_page_button = tk.Button(self.text, text="下一页", command=self.next_page)
        self.next_page_button.grid(row=0, column=1)
    def prev_page(self):
        # 显示上一页PDF图像
        if self.current_page_number > 0:
            self.current_page_number -= 1
            self.current_page_image = ImageTk.PhotoImage(self.re_size())
            self.image_label.config(image=self.current_page_image)
        else:
            messagebox.showinfo('第一页', '已经是第一页了哦')

    def next_page(self):
        # 显示下一页PDF图像
        if self.current_page_number < len(self.pages) - 1:
            self.current_page_number += 1
            self.current_page_image = ImageTk.PhotoImage(self.re_size())
            self.image_label.config(image=self.current_page_image)
        else:
            messagebox.showinfo('最后一页', '已经是最后一页了哦')
def init():
    get_workbench().add_view(PdfView, 'pdf预览', "se", visible_by_default=False)


class Tabs(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        # TODO: implement tabs
