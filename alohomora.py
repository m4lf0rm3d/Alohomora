import sys, os
sys.path.append("RSA/")
from rsa_cryptography import *
from banner import *
from time import sleep, time
from math import ceil, floor

class Alohomora:
    def __init__(self):
        self.RSA = RSA()
        
    def run(self):
        self._clear_terminal()
        print(ITALIC + "👉 Select an option\n" + END)
        print(BOLD + "   1)  Generate new key pairs")
        print(BOLD + "   2)  Load key pairs from files")
        print(BOLD + "   3)  Encrypt file or directory")
        print(BOLD + "   4)  Decrypt file or directory")
        print(BOLD + "   5)  Exit")

        CHOSEN_OPTION = input("\nChoose option from (1-5):\n>>> ")
        if CHOSEN_OPTION not in ("1", "2", "3", "4", "5"): 
            self._print_invalid_option()
            self.run()

        else:
            if CHOSEN_OPTION == "5":
                self._clear_terminal()
                print(GRAY + "💀 Don't forget to DELETE private key! 💀\n" + END)
                sleep(1)
                print(BOLD + ITALIC + GREEN + "💖 THANKS FOR USING ALOHOMORA 💖")
            
            if CHOSEN_OPTION == "1": self.generate_new_key_pairs()

            if CHOSEN_OPTION == "2": self.load_keys_from_file()

            if CHOSEN_OPTION == "3": self.lock()

            if CHOSEN_OPTION == "4": self.lock(True)

    def generate_new_key_pairs(self):
        self._clear_terminal()
        print(ITALIC+ "👉 Generate new key pairs" +END+ BOLD)
        try:
            BITS_INPUT = int(input("\nEnter bits from range [530,4096]:\n>>> "))
            if BITS_INPUT < 530 or BITS_INPUT > 4096: raise ValueError()
            
            self._clear_terminal()
            print(ITALIC+ "👉 Generate new key pairs\n" +END)

            print(GRAY + BOLD + "  ⏳ Generating keys ...\n"+END)
            self.RSA.generate_keys(BITS_INPUT)

            print(GREEN +BOLD+ "  ✅ Keys generated successfully\n")
            sleep(2)

            self.run()

        except:
            self._print_invalid_option()
            self.generate_new_key_pairs()
        
    def load_keys_from_file(self):

        self._clear_terminal()
        print(ITALIC+ "👉 Load keys from file\n" +END)

        print(GRAY + BOLD + "  ⏳ Loading keys ...\n"+END)
        self.RSA.load_keys_from_file()

        print(GREEN +BOLD+ "  ✅ Keys loaded successfully\n")
        sleep(2)

        self.run()

    def lock(self, UNLOCK = False):
        
        self._clear_terminal()

        print(ITALIC+ "👉 Encrypt file or directory\n" +END) if not UNLOCK else print(ITALIC+ "👉 Decrypt file or directory\n" +END)

        if(not self.RSA.PRIVATE_KEY or not self.RSA.PUBLIC_KEY):
            print(RED + BOLD + "  ❌ Keys have not been loaded or generated yet!\n" + END)
            print(GRAY+ITALIC+ "  👋 Note: You can load or generate keys from main menu."+END)
            sleep(4)
            return self.run()
        
        ABSOLUTE_PATH = input(BOLD + "\nEnter absolute path to the file or directory\n>>> ")

        if not os.path.exists(ABSOLUTE_PATH):
            print(RED + "\n   Path not exists! ❌\n")
            sleep(1)
            self.lock(UNLOCK)
            return

        if UNLOCK:
            self.encrypt_decrypt_dashboard(ABSOLUTE_PATH, True, True) if(os.path.isdir(ABSOLUTE_PATH)) else self.encrypt_decrypt_dashboard(ABSOLUTE_PATH, True, False)
        else:
            self.encrypt_decrypt_dashboard(ABSOLUTE_PATH, False, True) if(os.path.isdir(ABSOLUTE_PATH)) else self.encrypt_decrypt_dashboard(ABSOLUTE_PATH, False, False)

    def encrypt_decrypt_dashboard(self, DIRECTORY_PATH, DECRYPT = False, DIRECTORY = False):
        
        self._clear_terminal()
        if DIRECTORY:
            print(ITALIC+ "👉 Decrypt directory\n" +END) if DECRYPT else print(ITALIC+ "👉 Encrypt directory\n" +END)
        else:
            print(ITALIC+ "👉 Decrypt file\n" +END) if DECRYPT else print(ITALIC+ "👉 Encrypt file\n" +END)

        print(GRAY + BOLD + "  ⏳ Reading files ...\n"+END) if DIRECTORY else print(GRAY + BOLD + "  ⏳ Reading file ...\n"+END)

        FILE_PATHS_LIST = [] if DIRECTORY else [DIRECTORY_PATH]
        TOTAL_SIZE = 0 if DIRECTORY else os.path.getsize(DIRECTORY_PATH)

        if DIRECTORY:
            for FILE_PATH in self._get_all_files(DIRECTORY_PATH):
                FILE_PATHS_LIST.append(FILE_PATH)
                TOTAL_SIZE += os.path.getsize(FILE_PATH)
        

        print(GRAY + BOLD + "  ⏳ Computing total time ...\n"+END)
        sleep(1)
        EXPECTED_TIME = (TOTAL_SIZE * 0.00001)/60 if DECRYPT else (TOTAL_SIZE * 0.000001)/60
        EXPECTED_TIME_HMS = self._convert_minutes_to_hms(EXPECTED_TIME)
        print(GREEN + BOLD + "  ✅ Expected time: " + str(EXPECTED_TIME_HMS)) 
        sleep(1) 

        print(GRAY + BOLD + "\n  🔑 Starting decryption ...\n"+END) if DECRYPT else print(GRAY + BOLD + "\n  🔒 Starting encryption ...\n"+END)
        sleep(2)

        START_TIME = time()
        COUNT = 0

        for FILE_PATH in FILE_PATHS_LIST:

            COUNT+=1
            self._clear_terminal()
            print(ITALIC+BOLD+ "🛡  Decryptor Dashboard 🛡\n" +END) if DECRYPT else print(ITALIC+BOLD+ "🛡  Encryptor Dashboard 🛡\n" +END) 

            FILE_NAME = FILE_PATH.split("/")[-1]

            print(30 * "=" + "\n")

            print("FILENAME: "+ BOLD+ FILE_NAME +END)
            print( "FILEPATH: "+ FILE_PATH )
            print( "SIZE:     "+ str(ceil(os.path.getsize(FILE_PATH)/1000)) +"KB"+END)

            print()
            print(30 * "=")

            print(GREEN  + f"\n  ⏳ Expected time {BOLD}{EXPECTED_TIME_HMS}\n"+END)
            
            ELAPSED_TIME = int(time() - START_TIME)
            HOURS = ELAPSED_TIME // 3600
            MINUTES = (ELAPSED_TIME % 3600) // 60
            SECONDS = ELAPSED_TIME % 60
            
            TIME_STR = f"{GREEN}  ⏳ Elpased Time: {BOLD}{HOURS:02d}:{MINUTES:02d}:{SECONDS:02d}"

            print(TIME_STR, end="\r", flush=True) if COUNT != len(FILE_PATHS_LIST) else print(TIME_STR)

            PROGRESS_HASH_COUNT = ((floor((COUNT/len(FILE_PATHS_LIST))*100)//10))

            print("\n\n  🏆 Progress: [" + PROGRESS_HASH_COUNT * "##" + "__" * (10 - PROGRESS_HASH_COUNT) + "]\n" ) if COUNT != len else print("\n  🏆 Progress: COMPLETED! ")


            with open(FILE_PATH, 'rb') as FILE:
                BYTES = FILE.read()

            LENGTH = self.RSA.MAX_CIPHER_LENGTH if DECRYPT else 446


            ENCRYPT_FUNCTION = self._encrypt_function(DECRYPT)
            DECRYPT_FUNCTION = self._decrypt_function(DECRYPT)

            OUTPUT_FILE_BYTES = bytes()

            INPUT_FILE_SIZE = len(BYTES)

            if not DECRYPT: os.remove(FILE_PATH)

            with open(FILE_PATH, 'wb') as FILE:

                for i in range(0,INPUT_FILE_SIZE, LENGTH):
                    BYTE = ENCRYPT_FUNCTION(BYTES[i:i+LENGTH])
                    FILE.write(DECRYPT_FUNCTION(BYTE))
            
                REMAINING_BYTES = INPUT_FILE_SIZE % LENGTH
                
                if REMAINING_BYTES != 0:
                    BYTE = ENCRYPT_FUNCTION(BYTES[INPUT_FILE_SIZE-REMAINING_BYTES-1:])
                    FILE.write(DECRYPT_FUNCTION(BYTE))

            sleep(1)

        self.run()

    def _print_invalid_option(self):
        print(RED + "\n   Invalid option ❌\n")
        sleep(1)
        self._clear_terminal()

    def _clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(BANNER_TEXT)

    def _get_all_files(self, DIRECTORY):
        for ROOT, DIRS, FILES in os.walk(DIRECTORY):
            for FILE in FILES:
                FILE_PATH = os.path.join(ROOT, FILE)
                yield FILE_PATH

    def _encrypt_function(self, DECRYPT):
        def void(BYTE): return BYTE
        return void if DECRYPT else self.RSA.encrypt
        self.RSA.decrypt(BYTE) if DECRYPT else BYTE

    def _decrypt_function(self, DECRYPT):
        def void(BYTE): return BYTE
        return self.RSA.decrypt if DECRYPT else void
    


    def _convert_minutes_to_hms(self, MINUTES):

        SECONDS_PART = ceil((MINUTES - floor(MINUTES))*60)

        MINUTES = ceil(MINUTES) if MINUTES > 1 else 0

        HOURS = str(MINUTES // 60) if (MINUTES // 60) >=10 else '0'+str(MINUTES // 60)

        MINUTES = str(MINUTES % 60) if (MINUTES % 60) >=10 else '0'+str(MINUTES % 60)

        SECONDS = str(SECONDS_PART) if SECONDS_PART >= 10 else "0" + str(SECONDS_PART)
        
        return HOURS+"h:"+MINUTES+"m:"+SECONDS+"s"
        


if __name__ == "__main__":

    SPELL = Alohomora()
    SPELL.run()