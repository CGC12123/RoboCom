from pymycobot.mycobot import MyCobot

mc = MyCobot('/dev/arm',115200)
mc.power_on()
print(mc.get_coords())