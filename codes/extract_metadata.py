import arff

class Metadata(object):
	def __init__(self):
		self.nattrs = None
		self.attr_types = None
		self.ninstances = None
		self.nmissing_values = None
		self.nclasses = None

	def __str__(self):
		ret = 'nattrs %d\n' % self.nattrs
		ret +='attr_types %s\n' % self.attr_types
		ret +='ninstances %d\n' % self.ninstances
		ret +='nmissing_values %d\n' % self.nmissing_values
		ret +='nclasses %d\n' % self.nclasses
		return ret

_known_attr_types = set(['numeric'])

def extract_attr_types(attrs):
	attr_types = set()
	for attr in attrs:
		if str(attr[0]) != 'Class':

			attr_type = str(attr[1]).lower()
			if attr_type not in _known_attr_types:
				raise Exception('Unexpected attribute type:' + attr_type)

			attr_types.add(attr_type)

	result = list(attr_types)
	result.sort()
	return result

def count_attrs(attrs):
	count = 0
	for attr in attrs:
		if str(attr[0]) != 'Class':
			count += 1
	return count

def count_classes(attrs):
	p = len(attrs)-1
	if str(attrs[p][0]) != 'Class':
		return 0
	return len(attrs[p][1])

def count_missing_values(data):
	count = 0
	for i in xrange(len(data)):
		for j in xrange(len(data[i])):
			if str(data[i][j]) == '?':
				count += 1
	return count

def load(pathfilename):

	with open(pathfilename, 'r') as fp:
		md = Metadata()

		data = arff.load(fp)

		md.nattrs = count_attrs(data['attributes'])
		md.attr_types = extract_attr_types(data['attributes'])
		md.ninstances = len(data['data'])
		md.nmissing_values = count_missing_values(data['data'])
		md.nclasses = count_classes(data['attributes'])

		print md

if __name__=='__main__':
	import sys
	load(sys.argv[1])