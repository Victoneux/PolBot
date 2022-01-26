import os, discord, datetime, threading
import time as t
import provinces

dir_path = os.path.dirname(os.path.realpath(__file__))

token = open(dir_path + "/token.code", "r").readlines()[0].strip() ## Make a file called token.code, put bot token inside.

print(provinces.readProvince(1))