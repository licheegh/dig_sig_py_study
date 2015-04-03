
def	complex_w(fobj, data, name):
	fobj.write(('{0}:\n').format(name))
	for number in data:
		fobj.write(('\t{0.real:+.8e} {0.imag:+.8e}i\n').format(number))

def	real_w(fobj, data, name):
	fobj.write(('{0}:\n').format(name))
	for number in data:
		fobj.write(('\t{0:+.8e}\n').format(number))
