import os, discord, datetime, threading
import time as t
dir_path = os.path.dirname(os.path.realpath(__file__))

token = open(dir_path + "/token.code", "r").readlines()[0].strip()
print(token)