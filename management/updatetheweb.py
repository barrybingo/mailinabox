#!/usr/bin/python3
from web_update import do_web_update
import utils
env = utils.load_environment()
do_web_update(env)

