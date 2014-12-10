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



import datetime
import re



class FormatFields( object ):

	"""Converts fields to the paypal required format."""


	def get_datetime_field( self, dateTime ):
		"""This method is used inside main classes, if any classes needs date
		argument you can use Python datetime.datetime. 
		In short - you will not need to use this method.

		Paypal needs  Coordinated Universal Time (UTC/GMT), using ISO 8601
		format, and of type ns:dateTime for Date/Time formats.
 
		An example date/time stamp is 2006-08-24T05:38:48Z"""

		if type(dateTime) == datetime.datetime:
			return dateTime.isoformat()
		
		raise ValueError( 'dateTime value must be a datetime.datetime instance' )


	def get_carddate_field( self, date ):
		"""This method is used inside main classes, if any classes needs date
		argument you can use Python datetime.date. 
		In short - you will not need to use this method.

		Paypal cards needs date in MMYYYY format."""

		if type(date) == datetime.date:
			return date.strftime('%m%Y')

		raise ValueError( 'date value must be a datetime.date instance' )


	def get_amount_field( self, amount ):
		"""Returns formated amount. 
		For example 24.7 will become "24.70".

		Returned amount can be used for setting amounts in PayPal requests."""

		if (amount is None) or (amount < 0): 
			return '0.00'

		if type( amount ) == float:
			return '%.2f' % amount

		elif type( amount ) == int:
			return '%d.00' % amount
		
		else:
			try:
				val = float(amount)
				return '%.2f' % val
			except:
				return '0.00'




class Validator( object ):

	def __init__( self ):
		self._amount_pattern = re.compile( '^(\\d*\\.\\d{2}|0{1})$' )
		self._email_pattern = re.compile( 
			'^[_A-Za-z0-9-]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9-]+)*(\\.[_A-Za-z0-9-]+)$' )
		self._hexcolor_pattern = re.compile( '^[0-9,a-f,A-F]{6}$' )


	def is_valid_amount( self, amount ):
		"""Validates string if it is amount supported by paypal.
		Amount has to be exactly two decimal places, decimal point is ".", or 0.
		
		You can set 0 for for example Payment when you set up recurring payment."""

		if (amount is None) or (len(amount) == 0):
			return False;

		if not isinstance(amount, (str,unicode)):
			return False

		m = re.match( self._amount_pattern, amount )
		if not m: return False

		#print m.group(0)
		return ( (m.start() == 0) and (m.end() == len(amount)) )


	def is_valid_email( self, address ):
		"""Validates email address. Does not validate length of the email, 
		this is because it varies between paypal requests."""

		if (address is None) or (len(address) == 0):
			return False;

		m = re.match( self._email_pattern, address )
		if not m: return False

		return ( (m.start() == 0) and (m.end() == len(address)) )


	def is_valid_hexcolor( self, color ):

		if (color is None) or (len(color) == 0):
			return False;

		m = re.match( self._hexcolor_pattern, color )
		if not m: return False

		return ( (m.start() == 0) and (m.end() == len(color)) )

	
	def is_valid_luhn( self, number ):
		"""Uses Luhn algorithm to validate numbers. 
		Luhn algorithm is also known as modulus 10 or mod 10 algorithm.

		In this case, this is used to validate credit card numbers."""

		num = map(int, str(number))
		return sum(num[::-2] + [sum(divmod(d * 2, 10)) for d in num[-2::-2]]) % 10 == 0
