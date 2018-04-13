from xml.dom import minidom

class XmlDataExtractor(object):

	def __init__(self,path_to_file):
		self.meanJtime = 0
		self.file = path_to_file
		
	def get_data(self):
		try:
			xmldoc = minidom.parse(self.file)
			tripinfo_list = xmldoc.getElementsByTagName("tripinfo")
			accumlated_JTime =0
			for i,tripinfo in enumerate(tripinfo_list):
				accumlated_JTime += (float(tripinfo.getAttribute("duration")))

			meanJtime = accumlated_JTime/i
			return meanJtime
		except:
			print("error while parsing the file , make sure the path is valid and the attributes are ok! ")