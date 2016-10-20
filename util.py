import math

class packet(object):
	"""docstring for packet"""
	def __init__(self, ts=0, sip=0, sport=0, dip=0, dport=0, protocol=0, size=0):
		super(packet, self).__init__()
		self.ts = ts
		self.sip = sip
		self.sport = sport
		self.dip = dip
		self.dport = dport
		self.protocol = protocol
		self.size = size
		self.count = 1

	def get_size(self):
		return size

	def print_all(self):
		print self.ts, self.sip, self.sport, self.dip, self.dport, self.protocol, self.size

	def equal(self, other):
		# just judge if belong to the same flow
		if self.sip == other.sip  and\
			self.sport == other.sport and\
			self.dip == other.dip and\
			self.dport == other.dport:
			return True
		return False

	def equal_sip(self, other):
		if self.sip == other.sip:
			return True
		return False

	def equal_sport(self, other):
		if self.sport == other.sport:
			return True
		return False

	def equal_dip(self, other):
		if self.dip == other.dip:
			return True
		return False

	def equal_dport(self, other):
		if self.dport == other.dport:
			return True
		return False
		
	def ins(self):
		self.count += 1
		return self.count

	def to_string(self):
		return '|'.join(str(x) for x in [self.ts, self.sip, self.sport, self.dip, self.dport, self.protocol, self.size, self.count])


def entropy(flow_list):
	slist = [pkt.count for pkt in flow_list]
	S = sum(slist)
	result = 0

	for x in slist:
		x = (x +0.0)/S
		result += - (x)*math.log(x,2)

	return result

if __name__ == '__main__':
	# unit test 
	a = packet(1,1,1,1,1,2,1)
	a.count = 1111
	b = packet(1,1,1,1,2,2,1)
	c = packet(1,1,1,1,1,2,1)
	z = [a,b,c]
	print entropy(z)