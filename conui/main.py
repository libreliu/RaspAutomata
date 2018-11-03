import curses, time
import config
import os

global screen
global uifetch
global nextpage

def init(scr, uif, npage):
	uifetch = uif
	screen = scr
	nextpage = npage

def redraw():

def on_key():