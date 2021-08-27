import csv
from tkinter import Frame, Label, Text, Button, Grid, END, Tk, messagebox
from tkinter.filedialog import askopenfile, asksaveasfile, askopenfilename
import requests
import re
from bs4 import BeautifulSoup


class YoutubeViews:
    def __init__(self, master):
        self.master = master
        master.title(" Youtube Views ")
        master.geometry("1200x600")

        # Frame 1
        self.boxes_frame = Frame(master)
        self.input_label = Label(self.boxes_frame, text = "URLs") 
        self.title_label = Label(self.boxes_frame, text = "Título") 
        self.views_label = Label(self.boxes_frame, text = "Visualizações") 
        self.input_box = Text(self.boxes_frame, bg = "light gray") 
        self.title_box = Text(self.boxes_frame, bg = "light gray")
        # Frame 1.1
        self.views_sum_frame = Frame(self.boxes_frame)
        self.sum_label = Label(self.views_sum_frame, text = "Soma total") 
        self.views_box = Text(self.views_sum_frame, bg = "light gray") 
        self.sum_box = Text(self.views_sum_frame, bg = "light gray") 
        # Frame 2
        self.buttons_frame = Frame(master)
        self.show_button = Button(self.buttons_frame, height = 2, 
                        width = 20,  
                        text ="Show", 
                        command = lambda:self.process_input()) 
        self.open_button = Button(self.buttons_frame, height = 2, 
                        width = 20,  
                        text ="Abrir", 
                        command = lambda:self.open_file()) 
        self.save_button = Button(self.buttons_frame, height = 2, 
                        width = 20,  
                        text ="Salvar", 
                        command = lambda:self.save_file())
        self.reset_button = Button(self.buttons_frame, height = 2, 
                        width = 20,  
                        text ="Reset", 
                        command = lambda:self.reset())
        # Master frame grid config
        Grid.rowconfigure(master, 0, weight=1)
        Grid.columnconfigure(master, 0, weight=1)
        # Boxes frame grid config
        Grid.rowconfigure(self.boxes_frame, 1, weight=1)
        Grid.columnconfigure(self.boxes_frame, 0, weight=1)
        Grid.columnconfigure(self.boxes_frame, 1, weight=1)
        Grid.columnconfigure(self.boxes_frame, 2, weight=5)
        # Master frame grid
        self.boxes_frame.grid(row=0, sticky="nsew")
        self.buttons_frame.grid(row=1, sticky="nsew")
        # Frame 1 grid
        self.input_label.grid(row=0, column=0) 
        self.title_label.grid(row=0, column=1) 
        self.views_label.grid(row=0, column=2) 
        self.input_box.grid(row=1, column=0, sticky="nsew") 
        self.title_box.grid(row=1, column=1, sticky="nsew") 
        self.views_sum_frame.grid(row=1, column=2, sticky="nsew")
        # Frame 1.1 packing
        self.views_box.pack(side="top") 
        self.sum_label.pack(side="top") 
        self.sum_box.pack(side="top") 
        # Frame 2 packing
        self.show_button.pack(side="left", fill=None, expand="yes")
        self.open_button.pack(side="left", fill=None, expand="yes")
        self.save_button.pack(side="left", fill=None, expand="Yes")
        self.reset_button.pack(side="left", fill=None, expand="Yes")

        self.viewData = {}
        self.viewsSum = 0

    def reset(self):
        self.title_box.delete('1.0', END)
        self.views_box.delete('1.0', END)
        self.sum_box.delete('1.0', END)
        self.input_box.delete('1.0', END)
        self.viewsSum = 0
        self.viewData = {}

    def get_views(self, urlList):
        for url in urlList:
            if url not in self.viewData and url != '':
                print(url)
                try:
                    soup = BeautifulSoup(requests.get(url).text, 'lxml')
                    self.viewData[url] = {}
                    self.viewData[url]['name'] = soup.select_one('[itemprop="name"]')['content']
                    self.viewData[url]['interactionCount'] = soup.select_one('[itemprop="interactionCount"]')['content']
                    self.viewData[url]['author'] = soup.select_one('[itemprop="author"]').find(itemprop='name')['content']
                    self.viewsSum += int(self.viewData[url]['interactionCount'])
                except:
                    messagebox.showerror("Erro", f"URL \"{url}\" inválida")
                    del self.viewData[url]

    def process_input(self):
        # Clear boxes
        self.sum_box.delete('1.0', END)
        self.title_box.delete('1.0', END)
        self.views_box.delete('1.0', END)
        self.sum_box.delete('1.0', END)
        # Get input and process it
        inputData = self.input_box.get("1.0", "end-1c")
        urlList = re.split(' |\n', inputData)
        self.get_views(urlList)
        # Insert new data into boxes
        for url in list(self.viewData):
            if url not in urlList and url != '':
                self.viewsSum -= int(self.viewData[url]['interactionCount'])
                del self.viewData[url]
                print(f"deleted {url}")
            else:
                self.title_box.insert(END, f"{self.viewData[url]['name']}\n")
                self.views_box.insert(END, f"{self.viewData[url]['interactionCount']}\n")
        self.sum_box.insert(END, f"{self.viewsSum}")

    def open_file(self):
        file = askopenfile(mode ='r', filetypes = [('Arquivos csv', '*.csv'), ('Arquivo txt', '*.txt')]) 
        print(file)
        if file is not None:
            # Clear boxes
            self.reset()
            # Identify file extension and open it
            ext = file.name.split('.')[-1]
            if(ext == 'csv'):
                self.viewData = self.open_csv(file)
                if isinstance(self.viewData, dict) is False:
                    messagebox.showerror("Erro", self.viewData)
                    print(self.viewData)
                    return
                print(f"CSV file opened: {self.viewData}")
            if(ext == 'txt'):
                urlList = self.open_txt(file)
                if isinstance(urlList, list) is False:
                    messagebox.showerror("Erro", f"URL \"{urlList}\" inválida")
                    print(f"Url {urlList} inválida")
                    return
                print(f"URL file list opened: {urlList}")
                self.viewData = {}
                self.get_views(urlList)
            # Insert new data into boxes
            for video in self.viewData:
                self.input_box.insert(END, f"{video}\n")
                self.title_box.insert(END, f"{self.viewData[video]['name']}\n")
                self.views_box.insert(END, f"{self.viewData[video]['interactionCount']}\n")
            self.sum_box.insert(END, f"{self.viewsSum}")

    def open_csv(self, file):
        viewData = {}
        reader = csv.reader(file)
        try:
            for row in reader:
                viewData[row[3]] = {}
                viewData[row[3]]['interactionCount'] = row[1]
                viewData[row[3]]['author'] = row[2]
                viewData[row[3]]['name'] = row[0]
                self.viewsSum += int(row[1])
        except:
            return "Dados incompletos!"
        return viewData 

    def open_txt(self, file):
        urlList = []
        for line in file:
            urlList.append(line.strip())
            if(len(line.split(' ')) > 1):
                return line
        return urlList

    def save_file(self):
        files = [('Arquivo csv', '*.csv'), 
                ('Arquivo texto', '*.txt'),
                ('All Files', '*.*')] 
        f = asksaveasfile(mode='w', filetypes = files, defaultextension = files) 
        if f is None:
            return

        output = csv.writer(f, lineterminator='\n')
        for row in self.viewData:
            output.writerow([self.viewData[row]['name'], self.viewData[row]['interactionCount'], self.viewData[row]['author'], row])
        f.close()
        print(f"Data saved: {self.viewData}")
 

master = Tk() 

my_gui = YoutubeViews(master)
  
master.mainloop()

