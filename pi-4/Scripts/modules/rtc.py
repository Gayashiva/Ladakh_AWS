import time
from modules.SDL_DS3231 import SDL_DS3231

ds3231 = SDL_DS3231(1, 0x68)
# ds3231.write_now()
ds3231.write_all(29,30,4,1,3,12,92,True)
while True:
    print time.strftime("%Y-%m-%d %H:%M:%S")
    print ds3231.read_datetime()
    time.sleep(10)
