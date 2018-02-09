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
        self.__write_message("%s[INFO]%s %s" % (colorama.Fore.BLUE, colorama.Style.RESET_ALL, str(message)))

    def success(self, message):
        if(self.quiet): return
        self.__write_message("%s[SUCCESS]%s %s" % (colorama.Fore.GREEN, colorama.Style.RESET_ALL, str(message)))

    def warning(self, message):
        self.__write_message("%s[WARNING]%s %s" % (colorama.Fore.YELLOW, colorama.Style.RESET_ALL, str(message)))     

    def error(self, message):
        self.__write_message("%s[ERROR]%s %s" % (colorama.Fore.RED, colorama.Style.RESET_ALL, str(message)))
        

            
