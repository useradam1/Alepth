import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkcalendar import DateEntry
from tkinter import messagebox
from pathlib import Path
from engene.MathF import *
import re

class Color(vec3f):
	def __init__(self, x: float | int | vec2i | vec2i | vec3f | vec3i | vec4f | vec4i = 0, y: float | int | vec2i | vec2i = 0, z: float = 0) -> None:
		super().__init__(x, y, z)
	@property
	def hex(self):
		r = int(self.x * 255)
		g = int(self.y * 255)
		b = int(self.z * 255)
		return f"#{r:02x}{g:02x}{b:02x}"


def show_error_NOT_NUMBER(value : str):
    messagebox.showerror("ERROR", f"{value}")

def choose_file() -> str:
    file_path = fd.askopenfilename()
    return file_path

class FormTk:
	def __init__(self,
			title: str = "0",
			size: vec2i = vec2i(500, 500),
			color: Color = Color(0.95,0.95,0.95),
            modal: bool = False) -> None:

		self.root = tk.Tk()
		self.root.title(title)


		self.root.geometry(f"{int(size.x)}x{int(size.y)}")
		self.Color = color
		self.canvas = tk.Canvas(self.root, bg=(self.Color.hex), width=size.x, height=size.y)
		self.canvas.pack()
		self.SizeScreen = size
		self.H_SizeScreen: vec2i = size * 0.5
		self.clock = tk.Label(self.root)
		self.clock.pack()
		self.root.resizable(False,False)
		self.modal = modal

		if self.modal:
			self.root.attributes("-topmost", True)

	def set_pixel(self, pos: vec2i, color: Color) -> None:
		x, y = int(pos.x), int(pos.y)
		self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=color.arr, outline='')
	
	@property
	def clear(self) -> None:
		self.canvas.delete(tk.ALL)
	
	@property
	def close(self) -> None:
		self.root.destroy()

	@property
	def show(self) -> None:
		self.root.mainloop()

	@property
	def is_window_active(self) -> bool:
		return self.root.winfo_exists()
		


class Label:
	def __init__(self, 
			form : FormTk, text:str='', 
			pos:vec2i=vec2i(), 
			font:Tuple[str,int]=('Arial',10))->None:
		
		self.form=form
		self.text = text
		self.pos=pos
		self.font=font
		self.label = tk.Label(self.form.canvas)
		self.label.configure(font=self.font)
		self.label.place(anchor='center')
		self.set_text(self.text)

	def set_text(self, text:str)->None:
		self.text = text
		self.label.configure(text=self.text)
		self.set_position(self.pos)

	def set_position(self, pos:vec2i=vec2i())->None:
		self.pos=pos
		x=self.form.H_SizeScreen.x+self.pos.x
		y=self.form.H_SizeScreen.y-self.pos.y
		self.label.place(x=x, y=y)
	
	def set_font(self,font:Tuple[str,int]=('Arial',10))->None:
		self.font=font        
		self.label.configure(font=self.font)

	def set_image(self, img)->None:
		self.label.configure(image=img)

	'''def show_tooltip(self, text, event)->None:
		x, y, _, h = self.label.bbox('all')
		x += event.x_root
		y +=  event.y_root + h
		self.tooltip = tk.Toplevel(self.label)
		self.tooltip.geometry("+%d+%d" % (x, y))
		self.tooltip.overrideredirect(True)
		self.tooltip_label = tk.Label(self.tooltip, text=text, bg='lightyellow', 
									borderwidth=1, relief='solid', 
									font=self.font)
		self.tooltip_label.pack(ipadx=1)'''

	def hide_tooltip(self)->None:
		if hasattr(self, 'tooltip'):
			self.tooltip.destroy()

	def bind_tooltip(self, text)->None:
		self.label.bind('<Enter>', lambda event: self.show_tooltip(text, event))
		self.label.bind('<Leave>', lambda event: self.hide_tooltip())
	
	@property
	def delete(self) -> None:
		self.label.destroy()




class Slider:
	def __init__(self, 
			form:FormTk, 
			min_value:int=0, 
			max_value:int=100, 
			default_value:int=50, 
			pos:vec2i=vec2i(), 
			length:int=100,
			orient:Literal['horizontal','vertical']='horizontal',
			command=None)->None:
		self.form = form
		self.min_value = min_value
		self.max_value = max_value
		self.value = default_value
		self.pos = pos
		self.length = length
		self.orient = orient
		self.command = command

		# Create a Scale widget for the slider
		self.slider = tk.Scale(self.form.canvas, from_=min_value, to=max_value, orient=self.orient, length=length, command=self._on_slider_change)
		self.slider.set(default_value)
		self.set_position(self.pos)

		# Set the command to be called when the slider value changes
		self.set_command(command)

	def set_position(self, pos:vec2i=vec2i())->None:
		self.pos = pos
		x=self.form.H_SizeScreen.x+self.pos.x-(self.length*0.5)
		y=self.form.H_SizeScreen.y-self.pos.y
		self.slider.place(x=x, y=y)

	def set_command(self, command=None):
		self.command = command

	def set_value(self, value=0):
		self.slider.set(value)

	def set_min_value(self, min_value):
		self.min_value = min_value
		self.slider.config(from_=min_value)

	def set_max_value(self, max_value):
		self.max_value = max_value
		self.slider.config(to=max_value)

	@property
	def get_value(self):
		return self.value

	def _on_slider_change(self, event):
		self.value = int(self.slider.get())
		if self.command:self.command(self.value)
	
	@property
	def delete(self) -> None:
		self.slider.destroy()




class DropdownList:
	def __init__(self, 
			form:FormTk, 
			options:List[str], 
			selected_option:str,
			pos:vec2i=vec2i(),
			sca:vec2i=vec2i(1,1),
			command = None
		)->None:
		self.form = form
		self.options = options
		self.selected_option = selected_option
		self.pos = pos
		self.sca = sca
		self.command = command

		# Create the dropdown button widget
		self.button = tk.Button(master=self.form.canvas, text=self.selected_option, command=self.show_menu)
		self.button.place(anchor='center')
		self.set_position(self.pos)
		self.set_scale(self.sca)

		# Create the menu
		self.menu = tk.Menu(self.form.canvas, tearoff=0)

		# Populate the menu with options
		self.set_options(self.options)

	def show_menu(self):
		self.menu.post(self.button.winfo_rootx(), self.button.winfo_rooty() + self.button.winfo_height())

	def set_options(self, options : List[str])->None:
		self.menu.delete(0, tk.END)
		self.options = options[:]
		for option in self.options:
			self.menu.add_command(label=option, command=lambda opt=option: self.select_option(opt))

	def set_position(self, pos:vec2i=vec2i())->None:
		self.pos = pos
		x=self.form.H_SizeScreen.x+self.pos.x
		y=self.form.H_SizeScreen.y-self.pos.y
		self.button.place(x=x, y=y)

	def set_scale(self, scale:vec2i=vec2i(1,1))->None:
		self.sca=scale
		self.button.configure(width=self.sca.x, height=self.sca.y)
		
	def set_command(self, command=None)->None:
		self.command = command
		self.button.configure(command=command)

	def select_option(self, option):
		self.selected_option = option
		if(self.command):self.command(option)
		self.button.configure(text=option)
	
	@property
	def get_option(self) -> str:
		return self.button["text"]
	
	@property
	def delete(self) -> None:
		self.button.destroy()
		self.menu.destroy()




class Calendar:
	def __init__(self, 
		form:FormTk,
		pos:vec2i=vec2i()
	)->None:
		self.form = form
		self.pos = pos
	
		self.cal = DateEntry(self.form.canvas, width=12, background="darkblue", foreground="white", borderwidth=2)
		self.set_position(self.pos)
	
	@property
	def get_date(self):
		return self.cal.get_date()

	def set_position(self, pos:vec2i=vec2i())->None:
		self.pos = pos
		x=self.form.H_SizeScreen.x+self.pos.x
		y=self.form.H_SizeScreen.y-self.pos.y
		self.cal.place(x=x, y=y)
	
	@property
	def delete(self) -> None:
		self.cal.destroy()



class Button:
	def __init__(self, 
			form:FormTk, 
			text:str="", 
			pos:vec2i=vec2i(), 
			sca:vec2i=vec2i(1,1), 
			command=None,
			color:Color = Color(0.9,0.9,0.9))->None:
		
		self.form = form
		self.text = text
		self.pos = pos
		self.sca=sca
		self.command = command
		self.color=color

		# Create the button widget
		self.button = tk.Button(master=self.form.canvas)
		self.button.place(anchor='center')

		# Set the button param
		self.set_text(self.text)
		self.set_position(self.pos)
		self.set_scale(self.sca)
		self.set_command(self.command)
		self.set_color(self.color)

	def set_text(self, text:str="")->None:
		self.text = text
		self.button.configure(text=text)

	def set_position(self, pos:vec2i=vec2i())->None:
		self.pos = pos
		x=self.form.H_SizeScreen.x+self.pos.x
		y=self.form.H_SizeScreen.y-self.pos.y
		self.button.place(x=x, y=y)

	def set_scale(self, scale:vec2i=vec2i(1,1))->None:
		self.sca=scale
		self.button.configure(width=self.sca.x, height=self.sca.y)

	def set_command(self, command=None)->None:
		self.command = command
		self.button.configure(command=command)

	def set_color(self, color=Color(0.9,0.9,0.9))->None:
		self.color = color
		self.button.configure(bg=self.color.hex)

	@property
	def get_text(self) -> str:
		return self.button["text"]
	
	@property
	def delete(self) -> None:
		self.button.destroy()



class TextEdit:
	def __init__(self,
				form: FormTk,
				pos: vec2i = vec2i(),
				sca: vec2i = vec2i(10,10),
				scrollBar:bool = False,
				digital:Literal['str','float','int'] = 'str',
				command=None,
				tooltipText:str="") -> None:

		self.form = form
		self.pos = pos
		self.sca = sca
		self.scrollBarVar = scrollBar
		self.frame = tk.Frame(self.form.canvas)
		self.text = tk.Text(self.frame, wrap="none")
		self.digital = digital
		self.command = command
		self.tooltipText = tooltipText
		if(self.scrollBarVar):
			self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.text.yview)
			self.text.configure(yscrollcommand=self.scrollbar.set)
			self.scrollbar.pack(side='right', fill='y')
		self.text.pack(side='left', fill='both', expand=True)
		self.frame.place(anchor='center')
		self.set_position(self.pos)
		self.set_scale(self.sca)


		# create context menu
		self.context_menu = tk.Menu(self.text, tearoff=0)
		self.context_menu.add_command(label="Clear", command=self.clear)
		self.context_menu.add_separator()
		self.context_menu.add_command(label="Cut", command=self.cut)
		self.context_menu.add_command(label="Copy", command=self.copy)
		self.context_menu.add_command(label="Paste", command=self.paste)
		self.context_menu.add_separator()
		self.context_menu.add_command(label="Select All", command=self.select_all)

		# bind context menu to right-click event
		self.text.bind("<Button-3>", self.show_context_menu)

		self.text.bind("<Key>", self.handle_key_press)

		# create tooltip
		self.tooltip = None

		# bind tooltip events
		self.text.bind('<Enter>', self.show_tooltip)
		self.text.bind('<Leave>', self.hide_tooltip)

	def show_tooltip(self, event)->None:
		if(self.tooltipText!=""):
			x, y, _, h = self.text.bbox('insert')
			x += event.x_root
			y +=  event.y_root + h
			self.tooltip = tk.Toplevel(self.text)
			self.tooltip.geometry("+%d+%d" % (x, y))
			self.tooltip.overrideredirect(True)
			self.tooltip_label = tk.Label(self.tooltip, text=self.tooltipText, bg='lightyellow', 
										borderwidth=1, relief='solid', 
										font=self.text['font'])
			self.tooltip_label.pack(ipadx=1)

	def hide_tooltip(self, event)->None:
		if(self.tooltipText!=""):
			if self.tooltip is not None:
				self.tooltip.destroy()
				self.tooltip = None


	def handle_key_press(self, event)->None:
		if event.keysym == "Return" or event.keysym == "KP_Enter":
			# Execute your custom event here
			if(self.digital != 'str' and (self.get_last_char=='' or not self.get_text.lstrip('-').isdigit())):
				self.set_text(0)
				show_error_NOT_NUMBER("You entered a non-number")
			if(self.command):self.command(int(self.get_text) if(self.digital=='int') else float(self.get_text) if(self.digital=='float') else self.get_text)
			if(self.sca.y==1):return "break"
		elif(event.state==12):
			if (event.keycode == 86):self.paste()
			elif (event.keycode == 65):self.select_all()
			elif (event.keycode == 67):self.copy()
			elif (event.keycode == 88):self.cut()
			return "break"
		elif(self.digital!='str'):
			if(
				not event.char.isdigit() and 
				event.keycode!=8 and 
				event.state!=262153 and 
				event.keycode!=37 and 
				event.keycode!=38 and 
				event.keycode!=39 and 
				event.keycode!=40 and 
				(event.keysym != "Return" or event.keysym != "KP_Enter") and
				(event.keycode!=109 if(self.get_last_char == '') else True) and
				((event.keycode!=110 if( self.get_text.lstrip('-').isdigit() ) else True) if(self.digital=='float') else True)
			):
				return "break"

	def show_context_menu(self, event)->None:
		self.context_menu.tk_popup(event.x_root, event.y_root)

	def clear(self) -> None:
		self.text.delete("1.0", tk.END)

	def cut(self)->None:
		self.text.event_generate("<<Cut>>")

	def copy(self)->None:
		self.text.event_generate("<<Copy>>")

	def paste(self)->None:
		if(self.digital):
			if(self.text.clipboard_get().isdigit()):
				self.text.event_generate("<<Paste>>")
		else:self.text.event_generate("<<Paste>>")

	def select_all(self)->None:
		self.text.tag_add("sel", "1.0", "end-1c")

	def set_command(self, command=None)->None:
		self.command = command

	def set_position(self, pos: vec2i = vec2i(1,1)) -> None:
		self.pos = pos
		x = self.form.H_SizeScreen.x + self.pos.x
		y = self.form.H_SizeScreen.y - self.pos.y
		self.frame.place(x=x, y=y)

	def set_scale(self, scale: vec2i = vec2i(1,1)) -> None:
		self.sca = scale
		self.text.configure(width=self.sca.x, height=self.sca.y)

	@property
	def get_text(self)->str:
		return self.text.get("1.0", tk.END).strip()

	@property
	def get_last_char(self)->str:
		char = self.text.get("1.0", tk.END).strip()
		if(len(char)>0):char = char[-1]
		return char

	@property
	def get_firstText(self)->str:
		text = list(filter(bool, self.get_text.split('\n')))
		if len(text) > 0:
			text = text[0]
		else:
			text = ""
		return text

	def set_text(self, text) -> None:
		self.clear()
		self.text.insert(tk.END, text)
	
	@property
	def delete(self) -> None:
		self.frame.destroy()
		self.text.destroy()
		if(self.scrollBarVar):self.scrollbar.destroy()




class CheckBox:
	def __init__(self,
			form:FormTk, 
			pos:vec2i=vec2i(),
			var:bool=False) -> None:
		self.form:FormTk=form
		self.pos:vec2i=pos
		self.var=tk.BooleanVar(value=var)

		self.checkbox = tk.Checkbutton(self.form.canvas,variable=self.var)
		self.checkbox.place(anchor='center')
		self.set_position(self.pos)

	def set_position(self, pos:vec2i=vec2i())->None:
		self.pos = pos
		x=self.form.H_SizeScreen.x+self.pos.x+5
		y=self.form.H_SizeScreen.y-self.pos.y+5
		self.checkbox.place(x=x, y=y)
	
	@property
	def get_value(self)->bool:
		return self.var.get()
	
	def set_value(self,value:bool)->None:
		self.var.set(value)
	
	@property
	def delete(self) -> None:
		self.checkbox.destroy()




class ImageOBJ(Label):
	def __init__(self, form:FormTk, data=None, path:str="", pos:vec2i=vec2i()) -> None:
		super().__init__(form, "", pos, ('Arial',10))
		self.path=path
		self.data=data
		self.image : tk.PhotoImage = 0
		if(self.data==None):
			self.image = tk.PhotoImage(file=self.path)
		else:
			self.image = tk.PhotoImage(data=self.data)
		super().set_image(self.image)
	
	def set_image(self, data=None, path:str="") -> None:
		self.path=path
		self.data=data
		if(self.data==None):
			self.image.configure(file=self.path)
		else:
			self.image.configure(data=self.data)
		super().set_image(self.image)
