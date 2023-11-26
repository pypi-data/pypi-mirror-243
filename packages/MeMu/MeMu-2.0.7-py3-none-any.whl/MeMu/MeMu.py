from . import emulator as emu
import customtkinter as ctk
from tkinter import filedialog 
from tkinter import font
import threading
from PIL import Image
import pkg_resources




class Memu:
    def __init__(self):
        self.app = ctk.CTk()
        self.size_x = round(694/1.5)
        self.size_y = round(1115/1.5)
        self.app.geometry(f'{self.size_x}x{self.size_y}')
        self.app.title('MeMu')
        self.emu_running = False
        self.app.resizable(False, False)
        self.screen_color = '#95b128'
        self.secondary_color = '#3d5b28'
        self.text_color = '#688852'
        self.selected_color = '#8af977'
        self.hovered_color = '#0b2f05'
        self.font_path = pkg_resources.resource_filename(__name__, 'Gbboot-ALpM.ttf')
        # self.custom_font = font.Font(family="G.B.BOOT", name="G.B.BOOT")
        self.image_path = pkg_resources.resource_filename(__name__, 'bg.png')
        self.icon_path = pkg_resources.resource_filename(__name__, 'icon.ico')
        self.app.iconbitmap(self.icon_path)

        try:
            self.custom_font = font.Font(family="G.B.BOOT", name="G.B.BOOT")
            self.custom_font_path = font_path  # Save for later use
        except Exception as e:
            print(f"Failed to load custom font: {e}")
            self.custom_font = None
            self.custom_font_path = None


        # TODO add fonts
        # Configure the fonts
        try:
            self.main_font_norm = ctk.CTkFont(family="G.B.BOOT", size=32)
            self.main_font_norm.configure(file=self.custom_font_path)

            self.main_font_bold_large = ctk.CTkFont(family="G.B.BOOT", size=64, weight='bold')
            self.main_font_bold_large.configure(file=self.custom_font_path)

            self.main_font_small = ctk.CTkFont(family="G.B.BOOT", size=16)
            self.main_font_small.configure(file=self.custom_font_path)

        except Exception as e:
            print(f"Failed to configure custom fonts: {e}")
            
            if self.custom_font_path is None:
                # Use default fonts here
                self.main_font_norm = ctk.CTkFont(family="Arial", size=32)
                self.main_font_bold_large = ctk.CTkFont(family="Arial", size=64, weight='bold')
                self.main_font_small = ctk.CTkFont(family="Arial", size=16)





        # TODO add background images
        self.bg_image = ctk.CTkImage(light_image=Image.open(self.image_path),
                                  dark_image=Image.open(self.image_path),
                                  size=(self.size_x, self.size_y))

        self.bg_object = ctk.CTkLabel(self.app, image=self.bg_image, text='MeMu', text_color="#0F197B", font=self.main_font_bold_large)
        self.bg_object.place(x=0, y=0, relwidth=1, relheight=1)



        # Widget variables
        self.rom_path = ctk.StringVar(self.app)


        # Tabs View
        self.tabs = ctk.CTkTabview(master=self.app, width=50, height=10, segmented_button_unselected_color=self.secondary_color, text_color=self.text_color, segmented_button_selected_color=self.selected_color, segmented_button_selected_hover_color=self.hovered_color, segmented_button_unselected_hover_color=self.hovered_color, bg_color=self.screen_color, border_color=self.screen_color, fg_color=self.screen_color)
        self.tabs.pack(padx=10, pady=105)
        self.tabs.add("Main Menu")
        self.tabs.add("In-Game")
        self.tabs.add("Cheats")



        # Main Menu
        self.menu_frame = ctk.CTkFrame(self.tabs.tab("Main Menu"), bg_color=self.screen_color, border_color=self.screen_color, fg_color=self.screen_color)
        self.menu_frame.pack(padx=10)

        self.main_btn_frame = ctk.CTkFrame(self.menu_frame, bg_color=self.screen_color, border_color=self.screen_color, fg_color=self.screen_color)  #self.menu_frame
        self.main_btn_frame.pack()

        self.btn_load_rom = ctk.CTkButton(self.main_btn_frame, font=self.main_font_small, text='Select ROM', fg_color=self.secondary_color, bg_color=self.screen_color, text_color=self.text_color, command=self.load_rom)
        self.btn_load_rom.pack(padx=10)

        self.btn_start = ctk.CTkButton(self.main_btn_frame, font=self.main_font_small, text='Start Emulator', fg_color=self.secondary_color, bg_color=self.screen_color, text_color=self.text_color, command=self.start)
        self.btn_start.pack(padx=10)

        self.btn_close = ctk.CTkButton(self.main_btn_frame, font=self.main_font_small, text='Quit', fg_color=self.secondary_color, bg_color=self.screen_color, text_color=self.text_color, command=self.close_app)
        self.btn_close.pack(padx=10)



        # Running Menu
        self.auto_save = ctk.CTkCheckBox(self.tabs.tab("In-Game"), font=self.main_font_small, text_color=self.text_color, text='Auto Save On Close', bg_color=self.screen_color, fg_color=self.screen_color)
        self.auto_save.pack(padx=10)

        self.entry_label = ctk.CTkLabel(self.tabs.tab("In-Game"), font=self.main_font_small, text_color=self.text_color, text='Save Slot Name:', bg_color=self.screen_color, fg_color=self.screen_color)
        self.entry_label.pack(padx=10)

        self.slot_name = ctk.CTkEntry(self.tabs.tab("In-Game"), bg_color=self.secondary_color, fg_color=self.screen_color)
        self.slot_name.pack(padx=10)

        self.save_btn = ctk.CTkButton(self.tabs.tab("In-Game"), font=self.main_font_small, text='Save Game', fg_color=self.secondary_color, bg_color=self.screen_color, text_color=self.text_color, command=self.save_game)
        self.save_btn.pack(padx=10)

        self.load_btn = ctk.CTkButton(self.tabs.tab("In-Game"), font=self.main_font_small, text='Load Game', fg_color=self.secondary_color, bg_color=self.screen_color, text_color=self.text_color, command=self.load_game)
        self.load_btn.pack(padx=10)

        self.btn_close = ctk.CTkButton(self.tabs.tab("In-Game"), font=self.main_font_small, text='Quit', fg_color=self.secondary_color, bg_color=self.screen_color, text_color=self.text_color, command=self.close_app)
        self.btn_close.pack(padx=10)




        # Cheat Menu
        self.cheat_entry_label = ctk.CTkLabel(self.tabs.tab("Cheats"), font=self.main_font_small, text_color=self.text_color, text='Enter Gameshark Code:', bg_color=self.screen_color, fg_color=self.screen_color)
        self.cheat_entry_label.pack(padx=10)

        self.cheat_entry = ctk.CTkEntry(self.tabs.tab("Cheats"), bg_color=self.secondary_color, fg_color=self.screen_color)
        self.cheat_entry.pack(padx=10)

        self.cheat_list_frame = ctk.CTkFrame(self.tabs.tab("Cheats"), width=200 , height=50, bg_color='transparent', fg_color='transparent')
        self.cheat_list_frame.pack(padx=10)



 
    # TODO add functions

    def turn_on(self):
        self.app.mainloop()


    # Open a file dialog to choose a .gb file
    def load_rom(self):
        '''
        Allows user to select the rom from a file manager window.
        '''
        # self.app.withdraw()        # Uncomment line to hide the main app while selecting .gb file
        file_path = filedialog.askopenfilename(
            title="Select a .gb or .gbc file",
            filetypes=[("Game Boy ROM Files", "*.gb;*.gbc")])
        if file_path:
            self.rom_path.set(file_path)
        # self.app.deiconify()       # Uncomment line to unhide the main app after selecting .gb file


    def save_game(self):
        '''
        Saves Game to {slot_name}.state
        '''
        if self.emulator.is_running == True:
            self.emulator.save()


    def load_game(self):
        '''
        Loads Game from {slot_name}.state
        '''
        if self.emulator.is_running == True:
            self.emulator.load()



    def start(self):
        '''
        Initializes PyBoy emulator and runs selected rom file.
        '''
        if not self.emu_running:
            self.tabs.set("In-Game")
            self.emulator = emu.MeMu(self.rom_path.get())
            self.emulator.start()
            self.emu_running = True



    def stop(self):
        '''
        Stops the emulator if running.
        '''

        if self.emu_running:
            self.tabs.set("Main Menu")
            self.emulator.stop()
            self.emu_thread.join()  # Wait for the thread to finish
            self.emu_running = False


    def close_app(self):
        '''
        Closes the MeMu App
        '''
        self.app.destroy()


    def checkbox_event(self):
        '''
        TODO Allow for enabling and disabling cheats
        '''
        print("checkbox toggled, current value:", self.check_var.get())

 

    # TODO finish cheat menu

    # TODO add settings menu

    # TODO add possibly showing the emulator in ctk




if __name__ == '__main__':
    emu = Memu()
    emu.turn_on()