from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label 
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.app import runTouchApp
from kivy.uix.widget import Widget
from kivy.lang import Builder
import os
import extract
import update

get_files = lambda: os.listdir("./pdfs")

class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))
            
            
class MainApp(App):
	def last_chapter_readed(self):
		update.change_value(self.file_name, self.page)
		return


	def change_page(self, x):
		self.page+=x
		self.back_next.clear_widgets()
		self.root.scroll_y=1
		self.get_content(self.page)
		return


	def third_screen(self):
		self.screen.cols = 1 #main layout will be 1 col
		#settung another grid
		self.back_next =  GridLayout(size_hint_y=None)
		self.back_next.cols=2
		self.back_next.bind(
			minimum_height= self.screen.setter('height')
		)
		#putting the back to the last screen button 
		self.button = Button(
			text="back",
			on_press=self.second_screen,
			size_hint=(.3,.3),
			size_hint_y=None,
			halign="left"
		)
		#putting text
		my_label = WrappedLabel(text=self.content,  
			bold=True, 
			font_size="20sp", 
			halign="center", 
			size_hint=(1,1),
			size_hint_y=None
		)
		#put back and next buttons (chapter)
		if self.page>0:
			self.back_next.add_widget(Button(
				text="previous",
				on_press=lambda x: self.change_page(-1),
				size_hint=(.3,.3),
				size_hint_y=None,
				halign="left"
			))
		#back next  button
		self.back_next.add_widget(Button(
			text="next",
			on_press=lambda x: self.change_page(1),
			size_hint=(.3,.3),
			size_hint_y=None,
			halign="left"
		))
		#fit it on the screen
		self.screen.add_widget(self.button)
		self.screen.add_widget(my_label)
		self.screen.add_widget(self.back_next)
		return 
		
		
	# get the text
	def get_content(self, page):
		self.page=page
		self.content = extract.create_text(self.page, self.arch)
		self.screen.clear_widgets()
		self.last_chapter_readed()
		self.third_screen()
		
		
	#create second screen
	def second_screen(self, x):
		self.screen.clear_widgets()
		self.screen.cols = 2
		#variables
		self.button=[]
		#put buttons 
		self.screen.add_widget(
			Button(
				text="back",
				on_press=lambda i: self.first_screen(),
				size_hint_y=None,
				height= 100
				)
			)
		last_chapter=update.get_values(self.file_name)
		self.screen.add_widget(
				Button(
					text=str(last_chapter+1),
					on_press=lambda x, v=last_chapter:  self.get_content(v),
					size_hint_y=None,
					height= 100
				)
			)
		for i in range(self.pages):
			self.button.append(
				Button(
					text=f"{i+1}",
					on_press= lambda x, v=i:  self.get_content(v),
					size_hint_y=None,
					height= 100
					)
			)
		#fit buttons
		for i in range(len(self.button)):
			self.screen.add_widget(self.button[i])
			
			
	#get pdf variable 
	def get_text(self, x):
		self.file_name = self.files[x]
		self.arch = extract.extract_text(self.files[x])
		self.pages = len(self.arch)
		#clean screen and call a function that create another one
		self.screen.clear_widgets()
		self.page=x
		self.second_screen(x) 
		
		
	def first_screen(self):
		self.screen.clear_widgets()
		#variables
		self.files = get_files()
		self.button=[]
		self.label=[]
		#make list of buttons
		for i in range(len(self.files)):
			self.button.append(
				Button(
					text=">",
					size_hint=(.3,.3),
					on_press= lambda x, v=i:  self.get_text(v),
					size_hint_y=None
					)
			)
			
			
			#make labels with pdf name
			self.label.append(
				Label(
					text=str(self.files[i].replace(".pdf", "")),
					font_size="8dp",
					size_hint=(1,1),
					size_hint_y=None
				)
			)
			
		#add it all on the screen 
		for i in range(len(self.button)):
			self.screen.add_widget(self.label[i])
			self.screen.add_widget(self.button[i])
			
		

	def build(self):
		self.root= ScrollView(
			do_scroll_y= True,
			size=(Window.width, Window.height)
			)
		self.screen =  GridLayout(size_hint_y=None)
		self.screen.cols=2
		self.screen.bind(
			minimum_height= self.screen.setter('height')
		)
		
		self.first_screen()
		
		#adding ScrollView
		self.root.add_widget(self.screen)
		return self.root


if __name__ == "__main__":
	MainApp().run()
