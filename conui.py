import curses, time
import config
import os

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
	
def draw_main_panel(main_h, main_w):
	main.addstr(0,min(int(main_w / 2) - int(len(config.conui.main_title)/2) , main_w - len(config.conui.main_title)), config.conui.main_title)
	
	dparam = {"evnt_rpt" : "nope"}
	li = do_template_conv(main_h - 2, main_w - 2, 0, acquire_template("main"), dparam)
	fill_panel_blank(li, main)

def draw_stat_panel(stat_h, stat_w):
	stat.addstr(0,min(int(stat_w / 2) - int(len(config.conui.stat_title)/2) , stat_w - len(config.conui.stat_title)), config.conui.stat_title)

		
	dparam = {"evnt_rpt" : "nope"}
	li = do_template_conv(stat_h - 2, stat_w - 2, 0, acquire_template("stat"), dparam)
	fill_panel_blank(li, stat)


def draw_info_panel(info_h, info_w):
	info.addstr(0,min(int(info_w / 2) - int(len(config.conui.info_title)/2) , info_w - len(config.conui.info_title)), config.conui.info_title)
	
	dparam = {"uptime" : "10h", "ip" : "192.168.1.1", "daemon_status" : "stopped"}
	li = do_template_conv(info_h - 2, info_w - 2, 0, acquire_template("info"), dparam)
	fill_panel_blank(li, info)

	
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
	print(height, width)
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

		draw_main_panel(main_h,main_w)
		draw_stat_panel(stat_h,stat_w)
		draw_info_panel(info_h,info_w)
		
		refresh()
		main.getch()
		
	finally:
		screen.keypad(False)
		curses.endwin()


main_scr()
