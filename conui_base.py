import config
import os
import uifetch

acq_template = {}

def acquire_config():
	return config

def acquire_uifetch():
	return uifetch

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