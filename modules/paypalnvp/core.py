# Copyright (C) 2011 Luca Sepe <luca.sepe@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import abc
import httplib
import urllib
import urllib2
import urlparse
import logging
import StringIO
import copy



class Profile:
	"""Represents paypal user - his/her password, user name etc."""

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def get_nvp_map( self ):	
		"""Creates and returns part of the NVP (name value pair) 
		containing user name, password, signature etc. (obtained from paypal)."""



class BaseProfile( Profile ):
	"""Represents paypal user - his/her password, user name etc."""

	def __init__( self, username, password ):
		self._nvpMap = dict()
		# user name obtained from paypal
		self._nvpMap['USER'] = username
		# password obtained from paypal
		self._nvpMap['PWD'] = password


	def set_subject( self, value ):
		"""Email address of a PayPal account that has granted 
		you permission to make this call.
		
		Set this parameter only if you are calling an API on a different user's behalf"""

		if value is None: return
		self._nvpMap['SUBJECT'] = value


	def set_signature( self, value ):
		"""If you use an API certificate, do not include this parameter."""

		if value is None: return
		self._nvpMap['SIGNATURE'] = value


	def get_nvp_map( self ):
		return copy.deepcopy(self._nvpMap)


	def __str__( self ):
		return str(self._nvpMap)


class Request( object ):
	
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def get_nvp_request( self ):
		"""Creates and returns part of the nvp (name value pair) 
		request containing request values."""

	@abc.abstractmethod
	def set_nvp_response( self, nvpResponse ):
		"""Setter for nvp (name value pair) response."""

	@abc.abstractmethod
	def get_nvp_response( self ):
		"""Return response from paypal. 
		If response is not set/received returns empty Map."""




class Transport( object ):
	"""Used for sending request and returning response."""

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def get_response( self, urlString, msg ):
		"""Sends request (msg attribute) to the specified url and returns response as a string."""


class HttpPost( Transport ):

	def get_response( self, urlString, msg, debug=False ):

		if debug:
			httplib.HTTPConnection.debuglevel = 1
		
		headers = {
			'Content-type': 'application/x-www-form-urlencoded',
			'Accept': 'text/plain'
		}

		url = urlparse.urlparse( urlString )
		conn = None		
		if url.scheme == 'https':
			conn = httplib.HTTPSConnection( url.netloc, timeout=10 )
		else:
			conn = httplib.HTTPConnection( url.netloc, 80, timeout=10 )
		try:
			conn.request('POST', url.path, msg, headers)
			response = conn.getresponse()
			logging.getLogger().debug( '%s: %s', response.status, response.reason )

			return response.read()
			
		except httplib.HTTPException as e:
			logging.getLogger().error( e )
		finally:
			if conn: conn.close()



class PayPal( object ):


	def __init__( self, profile, sandbox=False, apiSignature=True ):
		if not isinstance(profile, Profile): 
			raise ValueError( 'profile must be an instance of <Profile> class' )

		self._profile = profile
		self._sandbox = sandbox
		self._version = '61.0'
		self._apiSignature = apiSignature;


	def set_response( self, request ):
		"""Sets response from PayPal. 
		Calls set_nvp_response on supplied request argument 
		and sets response Map from PayPal."""

		if not isinstance(request, Request): 
			raise ValueError( 'request must be an instance of <Request> class' )

		sb = StringIO.StringIO()

		# profile part
		params = self._profile.get_nvp_map()
		for k,v in params.items():
			params[k] = self._encode_if_necessary( v )
		sb.write( urllib.urlencode(params) )
		del ( params )
		
		# request part
		params = request.get_nvp_request()
		if len(params) > 0: sb.write( '&' )
		for k,v in params.items():
			params[k] = self._encode_if_necessary( v )
		sb.write( urllib.urlencode(params) )
		del ( params )

		params = { 'VERSION': '61.0' }
		sb.write( '&' )
		sb.write( urllib.urlencode(params) )
		del ( params )

		endpointUrl = StringIO.StringIO()
		if self._apiSignature:
			endpointUrl.write( 'https://api-3t.' )
		else:
			endpointUrl.write( 'https://api.' )
		if self._sandbox:
			endpointUrl.write( 'sandbox.' )
		endpointUrl.write( 'paypal.com/nvp' )

		transport = HttpPost()
		response = transport.get_response( endpointUrl.getvalue(), sb.getvalue() )
		
		if response:
			responseMap = dict()
			response = urllib2.unquote( response )
			for data in response.split('&'):
				keyval = data.split( '=' )
				responseMap[keyval[0]] = keyval[1]
			
			request.set_nvp_response( responseMap )


	def get_redirect_url( self, request ):
		"""Returns paypal url, where profile should be redirected. 
		If Request has not been sent, or response has not been successfull, None is returned."""

		if not isinstance(request, Request): 
			raise ValueError( 'request must be an instance of <Request> class' )

		response = request.get_nvp_response();
		if response is None: return None

		ack      = response['ACK']
		token    = response['TOKEN']

		# ack is not successfull or token is not set 
		if ( (ack is None) or (ack not in ['Success',]) ): return None
		if ( (token is None) or (len(token) == 0) ): return None

		# return redirect url
		url = StringIO.StringIO()
		url.write( 'https://www.' )
		if self._sandbox:
			url.write( 'sandbox.' )
		url.write( 'paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=' )
		url.write( token )
		
		return url.getvalue()


	def _encode_if_necessary(self, s):
		if isinstance(s, unicode):
			return s.encode('utf-8')
		return s