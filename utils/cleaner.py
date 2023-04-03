import os
class Cleaner:
    """
    This class deletes the log and other cache files from the working directory. please reconfigure this according to your system/
    """
    def clean_logs(self):
        logs = os.listdir("D:/erocabulary") # put your directory here
        for item in logs:
            if item.endswith(".log"):
                os.remove(item)
    def clear_cache(self):
        os.remove("__pycache__") 
    def main(self):
        self.clean_logs()
        self.clear_cache()
if __name__ == "__main__":
    Cleaner().main()

                