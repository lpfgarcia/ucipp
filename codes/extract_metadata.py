import arff
import json
import os

class Database(object):
	def __init__(self, path):
		self._data = dict()

		files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
		files = [f for f in files if f.endswith('.arff')]
		for f in files:
			md = Metadata(os.path.join(path, f))
			self._data[f] = md.dict_repr()

	def save(self, pathfilename):
		print 'Saving database to %s...' % pathfilename
		with open(pathfilename, 'w') as fp:
			fp.write(json.dumps(self._data))


class Metadata(object):
    def __init__(self, pathfilename):
    	print 'Reading %s.' % pathfilename
        self.nattrs = None
        self.attr_types = None
        self.ninstances = None
        self.nmissing_values = None
        self.nclasses = None

        self._load(pathfilename)

    def __str__(self):
        ret = 'nattrs %d\n' % self.nattrs
        ret +='attr_types %s\n' % self.attr_types
        ret +='ninstances %d\n' % self.ninstances
        ret +='nmissing_values %d\n' % self.nmissing_values
        ret +='nclasses %d' % self.nclasses
        return ret

    def dict_repr(self):
        d = dict()
        d['nattrs'] = self.nattrs
        d['attr_types'] = self.attr_types
        d['ninstances'] = self.ninstances
        d['nmissing_values'] = self.nmissing_values
        d['nclasses'] = self.nclasses
        return d

    def _extract_attr_types(self, attrs):
        attr_types = set()
        for attr in attrs:
            if str(attr[0]) != 'Class':

                if type(attr[1]) is list:
                    attr_types.add('categorical')
                elif str(attr[1]).lower() == 'numeric':
                    attr_types.add('numeric')
                else:
                    raise Exception('Unexpected attribute type:' + attr[1])

        result = list(attr_types)
        result.sort()
        return result

    def _count_attrs(self, attrs):
        count = 0
        for attr in attrs:
            if str(attr[0]) != 'Class':
                count += 1
        return count

    def _count_classes(self, attrs):
        p = len(attrs)-1
        if str(attrs[p][0]) != 'Class':
            return 0
        return len(attrs[p][1])

    def _count_missing_values(self, data):
        count = 0
        for i in xrange(len(data)):
            for j in xrange(len(data[i])):
                if str(data[i][j]) == '?':
                    count += 1
        return count

    def _load(self, pathfilename):
        with open(pathfilename, 'r') as fp:
            data = arff.load(fp)

            self.nattrs = self._count_attrs(data['attributes'])
            self.attr_types = self._extract_attr_types(data['attributes'])
            self.ninstances = len(data['data'])
            self.nmissing_values = self._count_missing_values(data['data'])
            self.nclasses = self._count_classes(data['attributes'])

if __name__=='__main__':
    import sys
    db = Database(sys.argv[1])
    db.save(sys.argv[2])