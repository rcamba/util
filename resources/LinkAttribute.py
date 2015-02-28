class LinkAttribute:
	def __init__(self,link):
		
		self.expire=""
		self.id=""
		self.sparams=""
		self.fexp=""
		self.ip=""
		self.upn=""
		self.cp=""
		self.ipbits=""
		self.newshard=""
		self.itag=""
		self.key=""
		self.ms=""
		self.ratebypass=""
		self.source=""
		self.sver=""
		self.mv=""
		self.mt=""
		self.itag=""
		self.signature=""
		self.fallback=""
		self.type=""
		self.gcr=""
		self.burst=""
		self.algorithm=""
		
		
		attribList=link.split('&')
		self.videoplayback=attribList[0]
		attribList=attribList[1:]
		
		for attrib in attribList:

			if attrib!=None:
			
				attrib="".join(['&',attrib])
							
				if "sparams" in attrib:
					self.sparams=attrib
				elif "algorithm" in attrib:
					self.algorithm=attrib
				elif "burst" in attrib:
					self.burst=attrib
				elif "expire" in attrib:
					self.expire=attrib
				elif "sig" in attrib:
					self.signature=attrib.replace("sig","signature")
				elif "fallback" in attrib:
					self.fallback=attrib
				elif "type" in attrib:
					self.type=attrib
				elif "fexp" in attrib:
					self.fexp=attrib
				elif "upn" in attrib:
					self.upn=attrib
				elif "ipbits" in attrib:
					self.ipbits=attrib
				elif "newshard" in attrib:
					self.newshard=attrib
				elif "key" in attrib:
					self.key=attrib
				elif "ms" in attrib:
					self.ms=attrib
				elif "ratebypass" in attrib:
					self.ratebypass=attrib
				elif "source" in attrib:
					self.source=attrib
				elif "sver" in attrib:
					self.sver=attrib
				elif "mv" in attrib:
					self.mv=attrib
				elif "mt" in attrib:
					self.mt=attrib
				elif "itag" in attrib:#get only first itag
					self.itag=attrib
				elif "gcr" in attrib:
					self.gcr=attrib
				elif "cp" in attrib:
					self.cp=attrib
				elif "id" in attrib:
					self.id=attrib
				elif "ip" in attrib:
					self.ip=attrib
				
				
	
	def __str__(self):
		return "\n".join([self.expire,self.id,self.sparams,self.fexp,self.ip, self.upn, self.cp, self.ipbits, self.newshard, self.itag, self.key, self.ms, self.ratebypass, self.source, self.sver, self.mv, self.mt, self.itag, self.signature, self.fallback, self.type, self.videoplayback])
		
		