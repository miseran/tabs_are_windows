c.tabs.show = 'never'
c.tabs.tabs_are_windows = True
c.window.title_format = '{private}{perc}{current_title}'

config.load_autoconfig()
config.bind('q', 'spawn --userscript tab-close')
config.bind('u', 'undo --window')
config.bind(']', 'spawn ~/.local/share/i3/window-tool tab-focus next')
config.bind('[', 'spawn ~/.local/share/i3/window-tool tab-focus prev')
config.bind('}', 'spawn ~/.local/share/i3/window-tool tab-move next')
config.bind('{', 'spawn ~/.local/share/i3/window-tool tab-move prev')
config.bind('z', 'spawn i3-msg move container to workspace 2, workspace 2')

# Monkey patching to allow tabs to open in the background.
# Very hacky.
import qutebrowser.mainwindow.mainwindow as mw
import inspect

# Set role on background tabs_are_windows
mw_old_init = mw.MainWindow.__init__
def __init__(self, *, private, geometry=None, parent=None):
	mw_old_init(self, private=private, geometry=geometry, parent=parent)
	f = inspect.stack()[1]
	if f.function == 'tabopen':
		bg = f.frame.f_locals["background"]
		if bg or (bg is None and c.tabs.background):
			self.setWindowRole("qutebrowser_background")
mw.MainWindow.__init__ = __init__
