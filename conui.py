import curses, time
import config
import os
import uifetch

screen = curses.initscr()
main = curses.newwin(3,3,0,0)
info = curses.newwin(3,3,0,0)
stat = curses.newwin(3,3,0,0)

acq_template = {}

def acquire_template(name):
	global acq_template
	try:
		t = acq_template[name]
		return t
	except KeyError:
		# Fetch in template path
		try:
			f = open(os.getcwd() + "/" + config.conui.template_path + name, "r")
			acq_template[name] = f.read()
			f.close()
			return acq_template[name]
		except FileNotFoundError:
			raise

def do_template_conv(h, w, pos, template, dparam):
	''' template(str) -> formated str -> line wrap and packed in list -> slice according to pos -> done '''
	fmt_li = template.format(**dparam).split("\n")
	# Do line wrap
	i = 0
	while i < len(fmt_li):
		elem = fmt_li[i]
		if len(elem) > w:
			if len(fmt_li) > i + 1:
				fmt_li[i + 1] = fmt_li[i + 1] + elem[w:]
			else:   # No next line available
				fmt_li.append(elem[w:])
			# Remember to erase the old!
			fmt_li[i] = elem[:w]
		i = i + 1
	return fmt_li[pos:pos+h]
	
def fill_panel_blank(li, handle):
	i = 1
	for elem in li:
		handle.addstr(i, 1, elem)
		i = i + 1
	
def draw_panel(h, w, win, title, dparam, pos, tempname):
	win.addstr(0, min(int(w / 2) - int(len(title)/2), w - len(title)), title)

	li = do_template_conv(h - 2, w - 2, pos, acquire_template(tempname), dparam)
	fill_panel_blank(li, win)
	
def resize_win():
	''' Window layout:
	+=======================+=======+
	|	main		|info	|
	|			|	|
	+			+=======+	
	|			|stat	|
	|			|	|
	+===============================+
	'''
	height, width = screen.getmaxyx()
	main_x = 0
	main_y = 0
	main_h = height
	main_w = int(width * 3 / 4) - 1

	info_x = int(width * 3 / 4)
	info_y = 0
	info_h = int(height / 2)
	info_w = int(width / 4)

	stat_x = info_x
	stat_y = height - info_h
	stat_h = info_h
	stat_w = info_w
	print("main y x:" , main_y, main_x)
	main.mvwin(main_y, main_x)
	print("info y x:" , info_y, info_x)
	info.mvwin(info_y, info_x)
	print("stat y x:" , stat_y, stat_x)
	stat.mvwin(stat_y, stat_x)

	main.resize(main_h, main_w)
	info.resize(info_h, info_w)
	stat.resize(stat_h, stat_w)	
	
	erase()
	main.box()
	info.box()
	stat.box()

	refresh()
	return (stat_h,stat_w,info_h,info_w,main_h,main_w)

def erase():
	screen.erase()
	main.erase()
	info.erase()
	stat.erase()

def refresh():
	''' explicitly fresh '''
	# Must refresh in the following order
	# Or the latter will overlap the former
	screen.refresh()
	main.refresh()
	info.refresh()
	stat.refresh()

def main_scr():
	global screen, main, info, stat
	try:
		curses.cbreak()
		screen.keypad(True)
		stat_h,stat_w,info_h,info_w,main_h,main_w = resize_win()

		# draw_panel(h, w, win, title, dparam, pos, tempname)
		draw_panel(main_h, main_w, main, config.conui.main_title 
			,{"evnt_rpt" : "nope"}, 0, "main")
		draw_panel(stat_h, stat_w, stat, config.conui.stat_title 
			,{"evnt_rpt" : "nope"}, 0, "stat")
		draw_panel(info_h, info_w, info, config.conui.info_title 
			,{"uptime" : "10h",
			  "ip" : uifetch.f.query("get_net_info",{})['ip'], "daemon_status" : "stopped"}, 0, "info")
	
		refresh()
		main.getch()
		
	finally:
		screen.keypad(False)
		curses.endwin()

def choose_shell():
	pass


main_scr()
