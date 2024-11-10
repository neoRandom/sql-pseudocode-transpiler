from sys import argv

class ArgumentParser:
    def __init__(self):
        self.args: list[str] = argv
        self.options: dict[str, str] = dict()

        # Getting the options
        for i, arg in enumerate(argv):
            if arg.startswith("-") and len(argv) > i + 1:
                value = argv[i + 1]
                if not value.startswith("-"):
                    self.options[arg.replace("-", "")] = value
                    self.args.remove(arg)
                    self.args.remove(value)


    def get_argument(
            self, 
            index: int, 
            *, 
            option_key: str | None = None,
            error_message: str = "Missing required argument") -> str:
        try:
            if option_key and option_key in self.options.keys():
                return_value = self.options[option_key].strip()
                if return_value:
                    return return_value
            
            return self.args[index]
        
        except IndexError:
            raise ValueError(error_message)
        
    def get_option(
            self, 
            option_key: str, 
            *, 
            panic: bool = True, 
            panic_message: str = "Missing required option"):
        if option_key in self.options.keys():
            return self.options[option_key].strip()
        if panic is True:
            raise ValueError(panic_message)
