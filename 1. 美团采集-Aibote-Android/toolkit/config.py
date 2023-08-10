import configparser

config = configparser.ConfigParser()
configPath = r"./data/config.ini"
config.read(configPath)

if __name__ == "__main__":
    print("a")
