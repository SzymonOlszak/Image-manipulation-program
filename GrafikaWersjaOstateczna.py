# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 23:04:31 2023

@author: SO2
"""

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import customtkinter
import customtkinter as ctk
import os
import torchvision.transforms.functional as F
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk, ExifTags, ImageEnhance
from customtkinter import CTkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import UnivariateSpline

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def open_file():
    file_path = filedialog.askopenfilename(filetypes = (("JPEG Files", "*.jpeg;*.jpg"), ("PNG Files", "*.png"), ("BMP Files", "*.bmp")))
    if file_path:
        print("Chosen file:", file_path)
        show_image(file_path)   
        
def show_image(file_path):
    
    image = Image.open(file_path)
                
    print(image.size)
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == "Orientation":
            break
    exif = image._getexif()
    if exif is not None:
        exif_dict = dict(exif)
        if orientation in exif_dict:
            if exif_dict[orientation] == 3:
                image = image.rotate(180, expand = True)
            elif exif_dict[orientation] == 6:
                image = image.rotate(270, expand = True)
            elif exif_dict[orientation] == 8:
                image = image.rotate(90, expand = True)
    
    image.thumbnail((640, 480)) 
    
    new_window = tk.Toplevel(root)
    new_window.title("MyGraphicsManager")
    new_window.state("zoomed")
    
    middle_area = tk.Frame(new_window, bg = "gray31")
    middle_area.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

    top_area = tk.Frame(middle_area, bg = "grey19")
    top_area.configure(height = 40)
    top_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = 0, padx = 0)
    top_area.pack_propagate(0)
    
    left_area = tk.Frame(middle_area, borderwidth = 1, relief = tk.SOLID, bg = "grey19")
    left_area.configure(width = 400)
    left_area.pack(side = tk.LEFT, fill = tk.BOTH, expand = False, pady = (20, 4), padx = 10)
    left_area.pack_propagate(0)
    
    right_area = tk.Frame(middle_area, borderwidth = 1, relief = tk.SOLID, bg = "grey19")
    right_area.configure(width = 400)
    right_area.pack(side = tk.RIGHT, fill = tk.BOTH, expand = False, pady = (20, 4), padx = 10)
    right_area.pack_propagate(0)
    
    bottom_area = tk.Frame(middle_area, borderwidth = 1, relief = tk.SOLID, bg = "grey19")
    bottom_area.configure(height = 20)
    bottom_area.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = False, pady = 4, padx = (10, 0))
    bottom_area.pack_propagate(0)
    
    tools_area= tk.Frame(right_area, borderwidth = 0, relief = tk.SOLID, bg = "#919191")
    tools_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = 0, padx = 0)
    
    tools_label = tk.Label(tools_area, text="Tools", fg="white", bg="#919191", font=tool_font)
    tools_label.pack()
    
    _,file_extansion = os.path.splitext(file_path)
    file_name = os.path.basename(file_path)
    
    info_label = tk.Label(bottom_area, text="File Information:  |Location:| {};  |File Name:| {};  |Resolution:| {}x{};  |File Type:| {};".format(file_path, file_name, image.width, image.height, file_extansion), bg="gray19", fg="white")
    info_label.pack(side = tk.LEFT, padx = 10)
    
    preview_area= tk.Frame(left_area, borderwidth = 0, relief = tk.SOLID, bg = "#919191")
    preview_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = 0, padx = 0)
    
    preview_label = tk.Label(preview_area, text="Preview", fg="white", bg="#919191", font=tool_font)
    preview_label.pack()

    histogramlebel_frame= tk.Frame(left_area, borderwidth = 1, relief = tk.SOLID, bg = "gray31")
    histogramlebel_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (50, 10), padx = 10)
   
    histogram_label = tk.Label(histogramlebel_frame, text="RGB Channels", fg="white", bg="gray31", font=tool_font)
    histogram_label.pack()
    
    histogram_area = tk.Frame(left_area, borderwidth = 3, relief = tk.SOLID, bg = "grey19")
    histogram_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = 0, padx = 10)
    bottom_area.pack_propagate(0)
    
    rg_arealabel= tk.Frame(left_area, borderwidth = 1, relief = tk.SOLID, bg = "gray31")
    rg_arealabel.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (50, 5), padx = 10)
    
    rg_label = tk.Label(rg_arealabel, text="Underexposed areas (red) and overexposed areas (green)", fg="white", bg="gray31", font=tool_font)
    rg_label.pack()
    
    rg_area = tk.Frame(left_area, bg = "grey19")
    rg_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = 0, padx = 10)
    bottom_area.pack_propagate(0)
    
    
    histogram = image.histogram()
    hist_r, hist_g, hist_b = np.array_split(histogram, 3)
    
    f, ax = plt.subplots()
    ax.set_facecolor("#909080")
    plt.grid()
    ax.plot(hist_r, color = "red")
    ax.plot(hist_g, color = "green")
    ax.plot(hist_b, color = "blue")
    plt.xlabel("Pixel value", **histogram_font)
    plt.ylabel("Number of pixels", **histogram_font)
    plt.tight_layout()
    plt.tick_params(axis='x', colors='grey')
    plt.tick_params(axis='y', colors='grey')
    ax.set_xlim([-5, 260])
    ax.set_ylim([0, max(max(hist_r) + max(hist_r) / 10 , max(hist_g) + max(hist_g) / 10, max(hist_b) + max(hist_b) / 10)])
    for i in ['top', 'bottom', 'left', 'right']:
       ax.spines[i].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    global canvas
    canvas = FigureCanvasTkAgg(f, master = histogram_area)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    def save_file():
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG Files", "*.png"),))
        if save_path:
            try:
                if new_img_label.image == photo or new_img_label.image == photo2:
                    save_image.save(save_path)
                    print("File saved successfully:", save_path)
            except NameError:
                pass
            
            try:
                if  new_img_label.image == photo3:
                        auto_image.save(save_path)
                        print("File saved successfully:", save_path)
            except NameError:
                pass
            try:
                if new_img_label.image == photo4:
                    auto_image.save(save_path)
                    print("File saved successfully:", save_path)
            except NameError:
                pass
            try:
                if new_img_label.image == reset_image:
                    imgg.save(save_path)
                    print("mhm")
            except NameError:
                print("no nie")
                
    savefile_button = customtkinter.CTkButton(master = top_area, text = "Save", command = save_file, fg_color = "#303133")
    savefile_button.configure(width = 80, height = 30)
    savefile_button.pack(pady = 1, padx = 1, side = "left")
    
    openfile_button = customtkinter.CTkButton(master = top_area, text = "Open new file", command = open_file, fg_color = "#303133")
    openfile_button.configure(width = 80, height = 30)
    openfile_button.pack(pady = 1, padx = 1, side = "left")
    
    quit_button = customtkinter.CTkButton(master = top_area, text = "Quit programme", command = root.destroy, fg_color = "#303133")
    quit_button.configure(width = 80, height = 30)
    quit_button.pack(pady = 1, padx = 1, side = "left")
    
    img = image.convert("RGB")
    d = img.getdata()
    new_image = []
    for item in d:
        if item[0] in [255]:
            new_image.append((0, 255, 0))
        elif item[0] in [1]:
            new_image.append((255,0,0))
        else:
            new_image.append(item)

    img.putdata(new_image)
    img.thumbnail((370,300))
    
    left_img_label = tk.Label(rg_area)
    left_img_label.pack(side = tk.TOP, pady = 10)
    tkk = ImageTk.PhotoImage(img)
    left_img_label.configure(image = tkk)
    left_img_label.image = tkk
    
    global resized_image
    resized_image = image
    
    def hide(widget):
        widget.pack_forget() 
    
    def reset():
        brightness.set(150)
        contrast.set(150)
        color_saturation.set(150)
        hue.set(0)
        sharpness.set(50)
        warm.set(0)
        global canvas
        canvas.get_tk_widget().forget()
        global reset_image
        global imgg
        global resized_image
        resized_image = image.resize((640, 480))
        imgg = image
        reset_image = ImageTk.PhotoImage(image)

        new_img_label.configure(image = reset_image)
        new_img_label.image = reset_image
        
        histogram = image.histogram()
        hist_r, hist_g, hist_b = np.array_split(histogram, 3)
        
        f, ax = plt.subplots()
        ax.set_facecolor("#909080")
        plt.grid()
        ax.plot(hist_r, color = "red")
        ax.plot(hist_g, color = "green")
        ax.plot(hist_b, color = "blue")
        plt.xlabel("Pixel value", **histogram_font)
        plt.ylabel("Number of pixels", **histogram_font)
        plt.tight_layout()
        plt.tick_params(axis='x', colors='grey')
        plt.tick_params(axis='y', colors='grey')
        ax.set_xlim([-5, 260])
        ax.set_ylim([0, max(max(hist_r) + max(hist_r) / 10 , max(hist_g) + max(hist_g) / 10, max(hist_b) + max(hist_b) / 10)])
        for i in ['top', 'bottom', 'left', 'right']:
           ax.spines[i].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        
        canvas = FigureCanvasTkAgg(f, master = histogram_area)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    def scale():
        try:
            x = int(sizex.get())
        except ValueError:
            x = "not int"

        try:
            y = int(sizey.get())
        except ValueError:
            y = "not int"
            
        global label_info
        global label_info2   
        
        if (isinstance(x, int) and isinstance(y, int)) == True:
            if 0 < x <=1100 and 0 < y <= 1000:
                
                img_label.pack_forget()
                img_label.place_forget()
                global canvas
                
                try:
                    hide(label_info)
                    hide(label_info2)
                except NameError:
                    pass
                    
                canvas.get_tk_widget().forget()
                
                brightness.set(150)
                contrast.set(150)
                color_saturation.set(150)
                hue.set(0)
                sharpness.set(50)
                warm.set(0)
                 
                global resized_image
                global save_image
                
                resized_image = image.resize((int(x),int(y)))
                save_image = resized_image
                
                global photo
                photo = ImageTk.PhotoImage(resized_image)
                new_img_label.pack(expand = True, fill = tk.BOTH)
                new_img_label.place(anchor = "center", relx = 0.5, rely = 0.5)
                new_img_label.configure(image = photo)
                new_img_label.image = photo  
                new_img_label.place(relx = 0.5, rely = 0.5, anchor = "center")
                new_img_label.lower()
                
                histogram2 = resized_image.histogram()
                hist_r, hist_g, hist_b = np.array_split(histogram2, 3)
                g, bx = plt.subplots()
                bx.set_facecolor("#909080")
                plt.grid()
                bx.plot(hist_r, color = "red")
                bx.plot(hist_g, color = "green")
                bx.plot(hist_b, color = "blue")
                plt.title("RGB Channels", **histogram_font)
                plt.xlabel("Pixel value", **histogram_font)
                plt.ylabel("Number of pixels", **histogram_font)
                plt.tick_params(axis='x', colors='grey')
                plt.tick_params(axis='y', colors='grey')
                plt.tight_layout()
                bx.set_xlim([-5, 260])
                bx.set_ylim([0, max(max(hist_r) + max(hist_r) / 10 , max(hist_g) + max(hist_g) / 10, max(hist_b) + max(hist_b) / 10)])
                
                for i in ['top', 'bottom', 'left', 'right']:
                   ax.spines[i].set_visible(False)
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')
                
                canvas = FigureCanvasTkAgg(g, master = histogram_area)
                canvas.draw()
                canvas.get_tk_widget().pack()
            else:
                try: 
                    hide(label_info)
                    
                except NameError:
                    pass
                
                try:
                    hide(label_info2)
                except NameError: 
                    pass    
                
                label_info2 = customtkinter.CTkLabel(master = size_area, text = "Please input the correct size of the image (max 1100x1000)", font = size_font)
                label_info2.pack(pady = 1)
                
        else:
            
            try:
                hide(label_info2)   
            except NameError: 
                pass
            
            try:
                hide(label_info)
            except NameError: 
                pass
            
            label_info = customtkinter.CTkLabel(master = size_area, text = "Please enter a number", font = size_font)
            label_info.pack(pady = 1)
            
        
        
    def manual_edition(img_label):
        
        global enhance   
        global save_image
        
        if image.size != resized_image.size:
            
            global canvas
            canvas.get_tk_widget().forget()
            
            brightness_value=float(int(brightness.get()) / 150)
            contrast_value = contrast.get() / 150
            color_saturation_value = color_saturation.get() / 150
            hue_value = hue.get() / 100
            sharpness_value = sharpness.get() / 50
            warm_value = int(warm.get())
            
            x = [0, 64, 128, 255]
            y = [0,255]
            z = [0,255]
            for i in x:
                if i == 64:
                    y.insert(1, i + warm_value)
                    z.insert(1, i - warm_value)
                elif i == 128:
                    y.insert(2, i + warm_value)
                    z.insert(2, i - warm_value)
            red_color = UnivariateSpline(x, y)(range(256))
            blue_color = UnivariateSpline(x, z)(range(256))
            
            def apply_warm(enhance, display = True):
                enh_convert = enhance.convert('RGB')
                enh_array = np.array(enh_convert)
                r_channel, g_channel, b_channel = cv2.split(enh_array)
                
                r_channel = cv2.LUT(r_channel, red_color).astype(np.uint8)
                b_channel = cv2.LUT(b_channel, blue_color).astype(np.uint8)
                global result
                result = cv2.merge((r_channel, g_channel, b_channel))
                result = Image.fromarray(result)
            
                
            img_enhancer = ImageEnhance.Brightness(resized_image)
            enhance = img_enhancer.enhance(brightness_value)
            
            img_enhancer2 = ImageEnhance.Contrast(enhance)
            enhance = img_enhancer2.enhance(contrast_value)
            
            img_enhancer3 = ImageEnhance.Color(enhance)
            enhance = img_enhancer3.enhance(color_saturation_value)
            
            img_enhancer4 = ImageEnhance.Sharpness(enhance)
            enhance = img_enhancer4.enhance(sharpness_value)
            
            apply_warm(enhance)
            
            save_image = F.adjust_hue(result, hue_value)
            
            global photo2
            photo2 = ImageTk.PhotoImage(save_image)
            
            new_img_label.configure(image = photo2)
            new_img_label.image = photo2    
            new_img_label.place(rely = 0.5, relx = 0.5, anchor = "center")
            new_img_label.lower()
            
            histogram2 = save_image.histogram()
            hist_r, hist_g, hist_b = np.array_split(histogram2, 3)
            g, bx = plt.subplots()
            bx.set_facecolor("#909080")
            plt.grid()
            bx.plot(hist_r, color = "red")
            bx.plot(hist_g, color = "green")
            bx.plot(hist_b, color = "blue")
            plt.title("RGB Channels", **histogram_font)
            plt.xlabel("Pixel value", **histogram_font)
            plt.ylabel("Number of pixels", **histogram_font)
            plt.tick_params(axis='x', colors='grey')
            plt.tick_params(axis='y', colors='grey')
            plt.tight_layout()
            bx.set_xlim([-5, 260])
            bx.set_ylim([0, max(max(hist_r) + max(hist_r) / 10 , max(hist_g) + max(hist_g) / 10, max(hist_b) + max(hist_b) / 10)])
            
            for i in ['top', 'bottom', 'left', 'right']:
               ax.spines[i].set_visible(False)
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            
            canvas = FigureCanvasTkAgg(g, master = histogram_area)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
            
        else:
            
                canvas.get_tk_widget().forget()
                
                brightness_value=float(int(brightness.get()) / 150)
                contrast_value = contrast.get() / 150
                color_saturation_value = color_saturation.get() / 150
                hue_value = hue.get() / 100
                sharpness_value = sharpness.get() / 50
                warm_value = int(warm.get())
                
                x = [0, 64, 128, 255]
                y = [0,255]
                z = [0,255]
                for i in x:
                    if i == 64:
                        y.insert(1,i + warm_value)
                        z.insert(1,i - warm_value)
                    elif i == 128:
                        y.insert(2,i + warm_value)
                        z.insert(2,i - warm_value)
                red_color = UnivariateSpline(x, y)(range(256))
                blue_color = UnivariateSpline(x, z)(range(256))
                
                def apply_warm(enhance, display = True):
                    enh_convert = enhance.convert('RGB')
                    enh_array = np.array(enh_convert)
                    
                    r_channel, g_channel, b_channel = cv2.split(enh_array)
                    r_channel = cv2.LUT(r_channel, red_color).astype(np.uint8)
                    b_channel = cv2.LUT(b_channel, blue_color).astype(np.uint8)
                    global result
                    result = cv2.merge((r_channel, g_channel, b_channel))
                    result = Image.fromarray(result)
                    
                img_enhancer = ImageEnhance.Brightness(image)
                enhance = img_enhancer.enhance(brightness_value)
                
                img_enhancer2 = ImageEnhance.Contrast(enhance)
                enhance = img_enhancer2.enhance(contrast_value)
                
                img_enhancer3 = ImageEnhance.Color(enhance)
                enhance = img_enhancer3.enhance(color_saturation_value)
                
                img_enhancer4 = ImageEnhance.Sharpness(enhance)
                enhance = img_enhancer4.enhance(sharpness_value)
                
                apply_warm(enhance)
                
                save_image = F.adjust_hue(result, hue_value)
                
                global photo
                photo = ImageTk.PhotoImage(save_image)
                
                
                new_img_label.configure(image = photo)
                new_img_label.image = photo    
                new_img_label.place(rely = 0.5, relx = 0.5, anchor = "center")
                
                histogram2 = save_image.histogram()
                hist_r, hist_g, hist_b = np.array_split(histogram2, 3)
                g, bx = plt.subplots()
                bx.set_facecolor("#909080")
                plt.grid()
                bx.plot(hist_r, color = "red")
                bx.plot(hist_g, color = "green")
                bx.plot(hist_b, color = "blue")
                plt.title("RGB Channels", **histogram_font)
                plt.xlabel("Pixel value", **histogram_font)
                plt.ylabel("Number of pixels", **histogram_font)
                plt.tick_params(axis='x', colors='grey')
                plt.tick_params(axis='y', colors='grey')
                plt.tight_layout()
                bx.set_xlim([-5, 260])
                bx.set_ylim([0, max(max(hist_r) + max(hist_r) / 10 , max(hist_g) + max(hist_g) / 10, max(hist_b) + max(hist_b) / 10)])
                
                for i in ['top', 'bottom', 'left', 'right']:
                   ax.spines[i].set_visible(False)
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')
                
                canvas = FigureCanvasTkAgg(g, master = histogram_area)
                canvas.draw()
                canvas.get_tk_widget().pack()
        
    def delete_text_y(e):
        sizey.delete(0,"end")   
    
    def delete_text_x(e):
        sizex.delete(0,"end")
        
    def auto_edit_image():
        
        global canvas
        global auto_image
        
        canvas.get_tk_widget().forget()
        img_label.pack_forget()
        img_label.place_forget()
        
        histogram = image.histogram()
        hist_r, hist_g, hist_b = np.array_split(histogram, 3)
    
        is_note = is_note_histogram(hist_r, hist_g, hist_b)
    
        if is_note:
          
          auto_image = image.convert("RGB")
          d = auto_image.getdata()
          new_image = []
          for item in d:
              if item[0] in list(range(150,256)):
                  new_image.append((255, 255, 255))
              else:
                  new_image.append(item)

          auto_image.putdata(new_image)
          auto_image.thumbnail((640,480))
          
          global photo3
          photo3 = ImageTk.PhotoImage(auto_image)
          
          new_img_label.configure(image = photo3)
          new_img_label.image = photo3
          new_img_label.pack(expand = True, fill = tk.BOTH)
          new_img_label.place(anchor = "center", relx = 0.5, rely = 0.5)
          
          histogram2 = auto_image.histogram()
          hist_r, hist_g, hist_b = np.array_split(histogram2, 3)
          g, bx = plt.subplots()
          bx.set_facecolor("#909080")
          plt.grid()
          bx.plot(hist_r, color = "red")
          bx.plot(hist_g, color = "green")
          bx.plot(hist_b, color = "blue")
          plt.title("RGB Channels", **histogram_font)
          plt.xlabel("Pixel value", **histogram_font)
          plt.ylabel("Number of pixels", **histogram_font)
          plt.tick_params(axis='x', colors='grey')
          plt.tick_params(axis='y', colors='grey')
          plt.tight_layout()
          bx.set_xlim([-5, 260])
          bx.set_ylim([0, max(max(hist_r) + max(hist_r) / 10 , max(hist_g) + max(hist_g) / 10, max(hist_b) + max(hist_b) / 10)])
          
          for i in ['top', 'bottom', 'left', 'right']:
             ax.spines[i].set_visible(False)
          ax.xaxis.set_ticks_position('none')
          ax.yaxis.set_ticks_position('none')
          
          canvas = FigureCanvasTkAgg(g, master = histogram_area)
          canvas.draw()
          canvas.get_tk_widget().pack()
          
        else:
            brightness_factor = 0.9
            contrast_factor = 1.5
            saturation_factor = 1.3
            
            edited_image = image.point(lambda x: x * brightness_factor)
        
            contrast_enhancer = ImageEnhance.Contrast(edited_image)
            edited_image = contrast_enhancer.enhance(contrast_factor)
            
            saturation_enhancer = ImageEnhance.Color(edited_image)
            auto_image = saturation_enhancer.enhance(saturation_factor)
            
            global photo4
            photo4 = ImageTk.PhotoImage(auto_image)
            
            new_img_label.configure(image = photo4)
            new_img_label.image = photo4
            new_img_label.pack(expand = True, fill = tk.BOTH)
            new_img_label.place(anchor = "center", relx = 0.5, rely = 0.5)
            
            histogram2 = auto_image.histogram()
            hist_r, hist_g, hist_b = np.array_split(histogram2, 3)
            g, bx = plt.subplots()
            bx.set_facecolor("#706999")
            plt.grid()
            bx.plot(hist_r, color = "red")
            bx.plot(hist_g, color = "green")
            bx.plot(hist_b, color = "blue")
            plt.title("RGB Channels", **histogram_font)
            plt.xlabel("Pixel value", **histogram_font)
            plt.ylabel("Number of pixels", **histogram_font)
            plt.tick_params(axis='x', colors='grey')
            plt.tick_params(axis='y', colors='grey')
            plt.tight_layout()
            bx.set_xlim([-5, 260])
            bx.set_ylim([0, max(max(hist_r) + max(hist_r) / 10 , max(hist_g) + max(hist_g) / 10, max(hist_b) + max(hist_b) / 10)])
            
            for i in ['top', 'bottom', 'left', 'right']:
               ax.spines[i].set_visible(False)
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            
            canvas = FigureCanvasTkAgg(g, master = histogram_area)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def is_note_histogram(hist_r, hist_g, hist_b):
   
        avg_r = np.mean(hist_r)
        avg_g = np.mean(hist_g)
        avg_b = np.mean(hist_b)
    
        print("Average R: ", avg_r)
        print("Average G: ", avg_g)
        print("Average B: ", avg_b)
    
        note_intensity_range = (595, 670)
    
    
        if note_intensity_range[0] <= avg_r <= note_intensity_range[1] and \
            note_intensity_range[0] <= avg_g <= note_intensity_range[1] and \
            note_intensity_range[0] <= avg_b <= note_intensity_range[1]:
                print("This is a note.")
                return True
        else:
            print("This is a beautiful photo.")
            return False

    autoE_button = customtkinter.CTkButton(master = right_area, text = "Auto edit", command = auto_edit_image, fg_color = "#8B8B7D")
    autoE_button.configure(width = 150, height = 30)
    autoE_button.pack(pady = 10)
    
    brightness_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    brightness_area.configure(height = 100)
    brightness_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (10, 5), padx = (5, 5))
   
    label_br = customtkinter.CTkLabel(master = brightness_area, text = "Brightness", font = tool_font)
    label_br.pack(pady = 3, padx = 6 )
    
    brightness = ctk.CTkSlider(brightness_area, from_ = 0, to = 300, fg_color = "#8B8B7D")
    brightness.set(150)
    brightness.pack(pady = 3)    
    brightness.bind("<B1-Motion>", manual_edition)
    
    contrast_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    contrast_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (5, 5), padx = (5, 5))
    
    label_con = customtkinter.CTkLabel(master = contrast_area, text = "Contrast", font = tool_font)
    label_con.pack(pady = 3, padx = 6 )
    
    contrast = ctk.CTkSlider(master = contrast_area, from_ = 0, to = 300, fg_color = "#8B8B7D")
    contrast.set(150)
    contrast.pack(pady = 3)
    contrast.bind("<B1-Motion>", manual_edition)
    
    color_saturation_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    color_saturation_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (5, 5), padx = (5, 5))
    
    label_col = customtkinter.CTkLabel(master = color_saturation_area, text = "Color saturation", font = tool_font)
    label_col.pack(pady = 3, padx = 6 )
    
    color_saturation = ctk.CTkSlider(master = color_saturation_area, from_ = 0, to = 300, fg_color = "#8B8B7D")
    color_saturation.set(150)
    color_saturation.pack(pady = 3)
    color_saturation.bind("<B1-Motion>", manual_edition)
    
    sharpness_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    sharpness_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (5, 5), padx = (5, 5))
    
    label_sharp = customtkinter.CTkLabel(master = sharpness_area, text = "Sharpness", font = tool_font)
    label_sharp.pack(pady = 3, padx = 6 )
    
    sharpness = ctk.CTkSlider(master = sharpness_area, from_ = -150, to = 250, fg_color = "#8B8B7D")
    sharpness.set(50)
    sharpness.pack(pady = 3)
    sharpness.bind("<B1-Motion>", manual_edition)
    
    hue_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    hue_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (5,5), padx = (5,5))
    
    label_hue = customtkinter.CTkLabel(master = hue_area, text = "Hue", font = tool_font)
    label_hue.pack(pady = 3, padx = 6)
    
    hue = ctk.CTkSlider(master = hue_area, from_ = -50, to = 50, fg_color = "#8B8B7D")
    hue.set(0)
    hue.pack(pady = 3)
    hue.bind("<B1-Motion>", manual_edition)
    
    warm_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    warm_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (5, 5), padx = (5, 5))
    
    label_warm = customtkinter.CTkLabel(master = warm_area, text = "Temperature", font = tool_font)
    label_warm.pack(pady = 3, padx = 6)
    
    warm = ctk.CTkSlider(master = warm_area, from_ = -20, to = 20, fg_color = "#8B8B7D")
    warm.set(0)
    warm.pack(pady = 3)
    warm.bind("<B1-Motion>", manual_edition)
    
    size_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    size_area.configure(width = 100, height = 150)
    size_area.pack(side = tk.TOP, fill = tk.BOTH, pady = (5, 5), padx = (5, 5))
    size_area.pack_propagate(0)
    
    label_size = customtkinter.CTkLabel(master = size_area, text = "Size (max 1100x1000)", font = tool_font)
    label_size.pack(pady = 1)
    
    sizex = ctk.CTkEntry(master = size_area, width = 80, border_width = 2, border_color = "black", font = size_font, fg_color="#8B8B7D")
    sizex.insert(0, "Width")
    sizex.pack(pady = 2)
    sizex.bind("<FocusIn>", delete_text_x)
    
    sizey = ctk.CTkEntry(master = size_area, width = 80, border_width = 2, border_color = "black", font = size_font, fg_color="#8B8B7D")
    sizey.insert(0, "Height")
    sizey.pack(pady = (2,0))
    sizey.bind("<FocusIn>", delete_text_y)
    
    set_size = ctk.CTkButton(master = size_area, width = 10, text = "Set", border_width = 2, border_color = "black", fg_color="#8B8B7D", command = scale)
    set_size.pack(pady = 2)
    set_size.place(rely=0.4, relx = 0.65)  
    
    reset_area = tk.Frame(right_area, borderwidth = 1, relief = tk.SOLID, bg = "grey24")
    reset_area.pack(side = tk.TOP, fill = tk.BOTH, expand = False, pady = (5,5), padx = (5,5))
    
    reset_button = customtkinter.CTkButton(master = right_area, text = "Original image", command = reset, fg_color = "#8B8B7D")
    reset_button.configure(width = 150, height = 30)
    reset_button.pack(pady = 10, side = tk.TOP)
    
    img_label = tk.Label(middle_area)
    img_label.place(relx = 0.5, rely = 0.5, anchor = "center")
    img_label.lower()
    
    tk_image = ImageTk.PhotoImage(image)
    img_label.configure(image = tk_image)
    img_label.image = tk_image
    
    new_img_label = tk.Label(middle_area)  
    
root = customtkinter.CTk()
root.title("MyGraphics")
root.geometry("400x320")
root.resizable(False, False)

#Zbiór czcionek
histogram_font = {'fontname': "Bahnschrift", 'size': "15", "color": "grey"}
size_font = CTkFont(family = "Abadi_Extra_Light", size = 10, slant = "italic", underline = 0)
label_font = CTkFont(family = "Abadi", size = 30, weight = "bold", slant = "roman", underline = 0)
footer_font = CTkFont(family = "Bahnschrift", size = 12, weight = "normal", slant = "roman", underline = 0)
tool_font = CTkFont(family = "Bahnschrift", size = 12, weight = "normal", slant = "roman", underline = 0)

frame = customtkinter.CTkFrame(master = root)
frame.pack(pady = 10, padx = 10 , fill = "none", expand = True)

label = customtkinter.CTkLabel(master = frame, text = "MyGraphics", font = label_font)
label.pack(pady = 15, padx = 10 )

open_button = customtkinter.CTkButton(master = frame, text = "Open the file", command=open_file, fg_color="#8B8B7D")
open_button.configure(width = 150, height = 30)
open_button.pack(pady = 30, padx = 10, side = "bottom") 

quit_button = customtkinter.CTkButton(master = root, text = "Quit program", command = root.destroy, fg_color="#8B8B7D")
quit_button.configure(width = 20, height = 15)
quit_button.pack(pady = 5, side = "top")

footer_frame = customtkinter.CTkFrame(master = root)
footer_frame.pack(side = "bottom", fill = "x")

footer_label_1 = customtkinter.CTkLabel(master = footer_frame, text ="Projekt: Grafika / Technologie Informatyczne ", font = footer_font)
footer_label_1.pack(pady = 0)

footer_label_2 = customtkinter.CTkLabel(master = footer_frame, text ="Kamil Iwaniak, Szymon Olszak", font = footer_font)
footer_label_2.pack(pady = 0)

background_image = Image.open("tlo2.png")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()


root.mainloop()