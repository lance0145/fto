# -*- coding: utf-8 -*-

import flectra
from flectra import api, models, fields

class FTO_Custom_Logic():
	
	"""
	In the following method we define FTO Custom Logic that will potentially be leveraged in more than one place.
	This method allows for FTO to be able to take a split employee name (First, Middle and Last) and then 
	update the "Full Name" field. There is a trigger in fto_applicant/models/models.py that will call this
	function whenever one of the name fields is updated, and then will update the "Full Name".
	"""

	@api.model
	def update_name_fields(self,first,middle,last):
		fullname_concat = str(first) +' '+ str(middle) +' '+ str(last)
		return fullname_concat.strip()     ##Using strip.() will remove leading and trailing whitespaces