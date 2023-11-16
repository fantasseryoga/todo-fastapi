from motor.motor_asyncio import AsyncIOMotorClient
import configparser

config = configparser.ConfigParser()
config.read("settings/settings.ini")

connection_str = "mongodb+srv://" + config["DB"]["DB_USER"] + ":" + config["DB"]["DB_PASS"] + "@cluster0.vnrgwih.mongodb.net/"

client = AsyncIOMotorClient(connection_str)
db = client["library"] 

try:
    client.admin.command('ping')
    print("Pinged your deployment. You have successfully connected to MongoDB!")
except Exception as e:
    print(e)