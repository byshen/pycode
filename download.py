import os


def download():
	for i in range(1,32):
		if i < 13:
			continue

		text = "http://mawi.nezu.wide.ad.jp/mawi/samplepoint-B/2001/200101%02d1400.dump.gz" %i
		cmd = "wget " + text

		print cmd
		os.system(cmd)
	return

def unzip():
	for i in range(1,32):
	
		text = "200101%02d1400.dump.gz" %i
		cmd = "gzip -d " + text

		print cmd
		os.system(cmd)

	return

unzip()