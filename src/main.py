from Hodor import Hodor
from settings.HodorSettings import HodorSettings

print("##############################################")
print("####           HODOR ft. VI23            #####")
print("##############################################")

settings = HodorSettings.read_from_file("settings.json")
hodor = Hodor(settings)

try:
    hodor.stop()
    hodor.setup()
    hodor.loop()
finally:
    hodor.stop()
    hodor.cleanup()
