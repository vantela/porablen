from numpy import *
import pyqtgraph as pg
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import (Parameter, ParameterTree)

app = pg.mkQApp("Porablen in Python")


class ScalableGroup(pTypes.GroupParameter):
	
	def __init__(self, **opts):
		opts['type'] = 'group'
		opts['addText'] = "Add new function"
		opts['addList'] = ['function']
		pTypes.GroupParameter.__init__(self, **opts)
	
	def addNew(self, typ):
		self.addChild(dict(name="f%d(x)" % (len(self.childs) / 2), type='str', value='%d*x + 10*sin(x)' % (len(self.childs) / 2)))
		self.addChild(dict(name="Color for f%d(x)" % (len(self.childs) / 2), type='color', value=random.randint(0, 256, size=3)))


params = [
	{'name': 'main', 'type': 'group', 'children': [
		{'name': 'Left limit', 'type': 'float', 'value': -100, 'step': 0.1},
		{'name': 'Right limit', 'type': 'float', 'value': 100, 'step': 0.1},
		{'name': 'Dots number', 'type': 'int', 'value': 1000, 'step': 10},
		{'name': 'Show grid', 'type': 'bool', 'value': True, 'tip': "Do you want to show grid?"},
	]},
	ScalableGroup(name="functions", children=[
		{'name': 'f0(x)', 'type': 'str', 'value': "x*sin(x)+x*cos(x)+0.4"},
		{'name': 'Color for f0(x)', 'type': 'color', 'value': "F0F"},
	]),
	{'name': 'Plot', 'type': 'action'},
	# {'name': 'Check', 'type': 'action'}
]

# Create tree of Parameter objects
p = Parameter.create(name='params', type='group', children=params)
t = ParameterTree()
t.setParameters(p, showTop=False)
t.show()
t.setWindowTitle('Make your choose')
t.resize(400, 800)

win = pg.GraphicsLayoutWidget(show=False, title="Посвящается... porablen!")
win.resize(1000, 600)
win.setWindowTitle('pyqtgraph example: porablen')
# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)


def plotting():
	left_limit = p.getValues()['main'][1:][0]['Left limit'][0]
	right_limit = p.getValues()['main'][1:][0]['Right limit'][0]
	dots_number = p.getValues()['main'][1:][0]['Dots number'][0]
	p1 = win.addPlot()
	i = 0
	while True:
		if 'f%d(x)' % i in p.getValues()['functions'][1:][0]:
			func = p.getValues()['functions'][1:][0]['f%d(x)' % i][0]
			color = p.getValues()['functions'][1:][0]['Color for f%d(x)' % i][0]
			x = linspace(left_limit, right_limit, dots_number)
			y = eval(func)
			p1.plot(x, y, pen=color)
#   		, symbolBrush=(255, 255, 0), symbolPen='g'
			i = i+1
		else:
			break

	if p.getValues()['main'][1:][0]['Show grid'][0]:
		p1.showGrid(x=True, y=True)
	win.show()
	t.hide()


# def checking():
# 	# print(p.getValues()['functions'][1:][0])
# 	# for key, value in p.getValues()['functions'][1:][0].items():
# 	# 	print("key=", key, 'value[0]=', value[0])
# 	# if 'f5(x)' in p.getValues()['functions'][1:][0]:
# 	# 	print('by key=', p.getValues()['functions'][1:][0]['f5(x)'][0])
# 	i = 0
# 	while True:
# 		if 'f%d(x)' % i in p.getValues()['functions'][1:][0]:
# 			print('f%d(x) = ' % i, p.getValues()['functions'][1:][0]['f%d(x)' % i][0])
# 			print('Color for f%d(x) = ' % i, p.getValues()['functions'][1:][0]['Color for f%d(x)' % i][0])
# 			i = i+1
# 		else:
# 			break

p.param('Plot').sigActivated.connect(plotting)
# p.param('Check').sigActivated.connect(checking)

if __name__ == '__main__':
	pg.exec()
