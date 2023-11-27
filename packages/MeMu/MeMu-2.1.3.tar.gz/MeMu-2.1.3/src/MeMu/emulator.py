from pyboy import PyBoy
import threading
import os

class Backend:
    def __init__(self, rom_path, save_slot='test', cheats_path='cheats.txt', config_path='settings.config'):
        self.pyboy = PyBoy(rom_path, cheats_path=cheats_path, cheats_enabled=True, sound=True)
        self.config_path = 'settings.config'
        self.cheats_path = 'Cheats/cheats.txt'
        self.slot = 'Save'
        self.auto_save = False
        self.is_running = False
        if os.path.exists(self.cheats_path):
            self.cheats_enabled = True
        else:
            self.cheats_enabled = False


        # Flag to control the emulator loop
        self.is_running = False

        # Event to signal when the emulator is ready to process cheats
        self.cheats_ready = threading.Event()

        # Lock for synchronization
        self.lock = threading.Lock()

        # Start the input processing thread
        self.input_thread = threading.Thread(target=self.input_thread_func)
        self.input_thread.start()

        # Start the cheats processing thread
        self.cheats_thread = threading.Thread(target=self.cheats_thread_func)
        self.cheats_thread.start()

    def input_thread_func(self):
        while True:
            # TODO Handle UI input processing here
            # TODO Update self.auto_save or any other UI-related flags
            # TODO use a queue to communicate with the UI thread
            pass

    def cheats_thread_func(self):
        while True:
            # Wait for the cheats_ready event to be set
            self.cheats_ready.wait()

            with self.lock:
                # Process cheats here
                if self.cheats_enabled:
                    self._update_codes()

            # Reset the event for the next iteration
            self.cheats_ready.clear()


    def start(self):
        if self.cheats_enabled:
            self._update_codes()
        self.load()
        self.is_running = True
        while not self.pyboy.tick():
            if self.cheats_enabled:
                self._run_cheats()
        if self.auto_save:
            self.save()
        print("State Saved as 'test.state'")


    def stop(self):
        try:
            self.is_running = False
            self.input_thread.join()  # Wait for the input thread to finish
            self.cheats_ready.set()  # Set the cheats_ready event to signal the cheats thread to exit
            self.cheats_thread.join()  # Wait for the cheats thread to finish
            self.pyboy.stop()
        except Exception as e:
            print(e)



    def save(self):
        try:
            with open(f'Saves/{self.slot}.state', "wb") as file_like_object:
                self.pyboy.save_state(file_like_object)
        except Exception as e:
            print(e)




    def load(self):
        try:
            with open(f'Saves/{self.slot}.state', "rb") as file_like_object:
                self.pyboy.load_state(file_like_object)
        except Exception as e:
            print(e)




    def get_screen(self):
        # TODO:
        # # Access PyBoy screen pixel data
        # pixels = pyboy.screen.pixel_array

        # # Convert PyBoy pixel data to an Image
        # img = Image.fromarray(np.uint8(pixels), "RGB")

        # # Update customtkinter image with the new frame
        # custom_image.update(img)

        # # Update the Tkinter canvas with the customtkinter image
        # canvas.create_image(0, 0, anchor="nw", image=custom_image)

        # # Update the Tkinter main loop
        # root.update()
        pass


    def emulate_input(self, input, release):
        '''
        Process one frame to let the game register the input.

        Example input: WindowEvent.PRESS_ARROW_DOWN
        Example release: WindowEvent.RELEASE_ARROW_DOWN
        '''
        self.pyboy.send_input(input)
        self.pyboy.tick()
        self.pyboy.send_input(release)



    def _update_codes(self):
        self.cheats = {}
        self._get_cheats()

    def _get_cheats(self):
        with open(self.cheats_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2:
                    cheat_name, gameshark_code = parts[0], parts[1]
                    self._convert_cheat(cheat_name, gameshark_code)
                else:
                    print(f"Invalid line in cheats file: {line}")

    def _convert_cheat(self, cheat_name: str, gameshark_code: str):
        '''
        A GameShark code for these consoles is written in the format ttvvaaaa. tt specifies the code type and VRAM bank, which is usually 01. vv specifies the hexadecimal value the code will write into the game's memory. aaaa specifies the memory address that will be modified, with the low byte first (e.g. address C056 is written as 56C0).
        Example 011556C0 would output:
        location = 01
        value = 0x15
        address = 0x56C0
        '''
        # Check if the input cheat code has the correct length (8 characters)
        if len(gameshark_code) != 8:
            raise ValueError("Invalid cheat code length. Cheat code must be 8 characters long.")

        # Extract components from the cheat code
        code_type = gameshark_code[:2]
        value = int((f'0x{gameshark_code[2:4]}'), 16)  # Convert hexadecimal value to an integer
        print(f'converted value = 0x{gameshark_code[2:4]}')
        unconverted_address = gameshark_code[4:]  # Ex:   1ED1
        lower = unconverted_address[:2]  # Ex:  1E
        upper = unconverted_address[2:]  # Ex:  D1
        address_converted = '0x' + upper + lower   # Ex: 0xD11E   # Converting to Ram Readable address 
        print(f'converted address = {address_converted}')
        address = int(address_converted, 16)

        # Format the output
        formatted_output = {
            'location': code_type,
            'value': value,
            'address': address
        }
        self.cheats[cheat_name] = formatted_output


    def _run_cheats(self):
        
        # Using keys() method
        for key in self.cheats.keys():
            if key in self.cheats:
                cheat = self.cheats[key]
                address = cheat['address']
                value = cheat['value']
                # print(f'cheat_address= {address}, cheat_value= {value}')
                self.pyboy.set_memory_value(address, value)
            else:
                print(f"Cheat '{key}' not found in the cheats database.")








if __name__ == '__main__':
    emulator = Backend('PokemonRed.gb')
    emulator.start()