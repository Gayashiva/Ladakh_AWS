import time
import SDL_DS3231

ds3231 = SDL_DS3231.SDL_DS3231(1, 0x48)
ds3231.write_now()
while True:
    print time.strftime(%Y-%m-%d)
    ds3231.read_datetime()
    time.sleep(10.0)