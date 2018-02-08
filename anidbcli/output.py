import colorama

class CliOutput:
    def __init__(self, quiet):
        self.quiet = quiet
        self.initialized = False

    def __write_message(self, message):
        if self.initialized:
            colorama.reinit()
        else:
            colorama.init()
            self.initialized = True
        print(message)
        colorama.deinit()

    def info(self, message):
        if(self.quiet): return
        self.__write_message(f"{colorama.Fore.BLUE}[INFO]{colorama.Style.RESET_ALL} {message}")

    def success(self, message):
        if(self.quiet): return
        self.__write_message(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Style.RESET_ALL} {message}")

    def warning(self, message):
        self.__write_message(f"{colorama.Fore.YELLOW}[WARNING]{colorama.Style.RESET_ALL} {message}")        

    def error(self, message):
        self.__write_message(f"{colorama.Fore.RED}[ERROR]{colorama.Style.RESET_ALL} {message}")
        

            
