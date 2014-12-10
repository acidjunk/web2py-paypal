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
import StringIO
import copy

import util


class RequestFields( object ):

	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def get_nvp_request( self ):	
		"""Creates and returns part of the NVP (name value pair) request containing request values."""


class Address( RequestFields ):

	def __init__( self, street, city, state, country='IT' ):
		self._nvp_request = dict()
		self._nvp_request['STREET'] = street
		self._nvp_request['CITY'] = city
		self._nvp_request['STATE'] = state
		self._nvp_request['COUNTRY'] = country

	def set_street_2( self, street):
		"""Second street address.
		Character length and limitations: 100 single-byte characters."""
		if len(street) > 100:
			raise ValueError( 'street can be maximum 100 characters.' )
		self._nvp_request['STREET2'] = street


	def set_zip( self, zip_code ):
		"""U.S. ZIP code or other country-specific postal code. 
		Required if using a U.S. shipping address; may be required for other countries.  
		Character length and limitations: 20 single-byte characters."""
		if len(street) > 20:
			raise ValueError( 'zip_code can be maximum 20 characters.' )
		self._nvp_request['ZIP'] = street


	def set_phone_number( self, phone_number ):
		"""Phone number. Character length and limit: 20 single-byte characters."""
		if len(phone_number) > 20:
			raise ValueError( 'phone_number can be maximum 20 characters.' )
		self._nvp_request['SHIPTOPHONENUM'] = phone_number

	def get_nvp_request( self ):
		return self._nvp_request
	



class ShipToAddress( RequestFields ):

	def __init__( self, name, street, city, state, country='NL' ):
		"""name is the Person's name associated with this shipping address (max 32 single-byte chars)
		street is the First street address (max 100 single-byte characters).
		city is the Name of city (max 40 single-byte characters).
		state is the State or province (max 40 single-byte character).
		country is the Country code."""
		if (len(name) > 32) or (len(street) > 100) or (len(city) > 40) or (len(state) > 40):
			raise ValueError( 'Characters limit exceeded.' )

		self._nvp_request = dict()
		self._nvp_request['SHIPTONAME'] = name
		self._nvp_request['SHIPTOSTREET'] = street
		self._nvp_request['SHIPTOCITY'] = city
		self._nvp_request['SHIPTOSTATE'] = state
		self._nvp_request['SHIPTOCOUNTRY'] = country

	def set_street_2( self, street):
		"""Second street address.
		Character length and limitations: 100 single-byte characters."""
		if len(street) > 100:
			raise ValueError( 'street can be maximum 100 characters.' )
		self._nvp_request['SHIPTOSTREET2'] = street


	def set_zip( self, zip_code ):
		"""U.S. ZIP code or other country-specific postal code. 
		Required if using a U.S. shipping address; may be required for other countries.  
		Character length and limitations: 20 single-byte characters."""
		if len(street) > 20:
			raise ValueError( 'zip_code can be maximum 20 characters.' )
		self._nvp_request['SHIPTOZIP'] = street


	def set_phone_number( self, phone_number ):
		"""Phone number. Character length and limit: 20 single-byte characters."""
		if len(phone_number) > 20:
			raise ValueError( 'phone_number can be maximum 20 characters.' )
		self._nvp_request['SHIPTOPHONENUM'] = phone_number

	def get_nvp_request( self ):
		return copy.deepcopy(self._nvp_request)
	




class ShippingOptions( RequestFields ):

	def __init__( self ):
		self._nvp_request = dict()

	def set_default_shipping_option( self, is_default ):
		"""Required if specifying the Callback URL.
		When the value of this flat rate shipping option is true, PayPal 
		selects it by default for the buyer and reflects it in the "default" total.
		
		Note:
		There must be ONE and ONLY ONE default. It is not OK to have no default."""
		option = 'true' if is_default else 'false'
		self._nvp_request['L_SHIPPINGOPTIONISDEFAULT'] = option


	def set_shipping_name( self, name ):
		"""Required if specifying the Callback URL.
		The internal name of the shipping option such as Air, Ground, 
		Expedited, and so forth. 

		Character length and limitations: 50 character-string."""

		if len(name) > 50:
			raise ValueError( 'name can be maximum 50 characters.' )
		self._nvp_request['L_SHIPPINGOPTIONNAME'] = name


	def set_shipping_label( self, label ):
		"""Required if specifying the Callback URL. 
		The label for the shipping option as displayed to the user. 
		Examples include: Air: Next Day, Expedited: 3-5 days, Ground: 5-7 days, 
		and so forth. Shipping option labels can be localized based on the 
		buyer's locale, which PayPal sends to your website as a parameter value 
		in the callback request. 

		Character length and limitations: 50 character-string."""
		if len(label) > 50:
			raise ValueError( 'label can be maximum 50 characters.' )
		self._nvp_request['L_SHIPPINGOPTIONLABEL'] = label
	

	def set_shipping_amount( self, amount ):
		"""Required if specifying the Callback URL. 
		The amount of the flat rate shipping option. 

		Limitations: 

			- Must not exceed $10,000 USD in any currency.
			- No currency symbol.
			- Must have two decimal places, decimal separator must be a period (.)."""
		
		v = util.Validator()
		if not v.is_valid_amount( amount ):
			sb = StringIO.StringIO()
			sb.write( 'Amount {0} is not valid. '.format(amount) )
			sb.write( 'Amount has to have exactly two decimal ' )
			sb.write( 'places seaprated by \".\" ' )
			sb.write( '- example: \"50.00\"' )
			raise ValueError( sb.getvalue() )
		
		self._nvp_request['L_SHIPPINGOPTIONAMOUNT'] = amount


	def get_nvp_request( self ):
		return copy.deepcopy(self._nvp_request)



class BillingAgreement( RequestFields ):

	def __init__( self ):
		self._nvp_request = dict()


	def set_billing_type( self, billing_type ):
		"""Type of billing agreement.
		For recurring payments, this field must be set to 'RecurringPayments'
		and description (set_description) MUST be set as well.
		In this case, you can specify up to ten billing agreements. 
		
		Note: Other defined values are not valid."""
		self._nvp_request['L_BILLINGTYPE'] = billing_type

	def set_description( self, description ):
		"""Description of goods or services associated with the billing agreement, 
		which is required for each recurring payment billing agreement.
		PayPal recommends that the description contain a brief summary of the 
		billing agreement terms and conditions.
		For example, customer will be billed at "9.99 per month for 2 years".

		Character length and limitations: 127 single-byte alphanumeric bytes."""
		if len(description) > 127:
			raise ValueError( 'description can be maximum 127 characters.' )
		self._nvp_request['L_BILLINGAGREEMENTDESCRIPTION'] = description 

	def set_payment_type( self, payment_type ):
		"""Type of PayPal payment you require for the 
		billing agreement ('Any' or 'InstantOnly').

		Note: For recurring payments, this field is ignored."""
		if payment_type not in ['Any', 'InstantOnly']:
			raise ValueError( 'payment_type must be Any or InstantOnly' )
		self._nvp_request['L_PAYMENTTYPE'] = payment_type 

	def set_custom_field( self, field ):
		"""Custom annotation field for your own use.

		Note: For recurring payments, this field is ignored.

		Character length and limitations: 256 single-byte alphanumeric bytes."""
		if len(field) > 256:
			raise ValueError( 'description can be maximum 256 characters.' )
		self._nvp_request['L_BILLINGAGREEMENTCUSTOM'] = field 

	def get_nvp_request( self ):
		return copy.deepcopy(self._nvp_request)



class PaymentItem( RequestFields ):

	"""Payment Details Item Type Fields. 
	You have to set amount for at leas one item.
	Otherwise the payment will be rejected by paypal, because order will be 0.00"""

	def __init__( self ):
		self._nvp_request = dict()


	def set_name( self, name ):
		"""Item name. Character length and limitations: 127 single-byte characters."""
		if len( name ) > 127:
			raise ValueError( 'Name cannot exceed 127 characters' )
	
		self._nvp_request['L_NAME'] = name


	def set_description( self, description ):
		"""Item description. Character length and limitations: 127 single-byte characters."""
		if len( description ) > 127:
			raise ValueError( 'Name cannot exceed 127 characters' )
		self._nvp_request['L_DESC'] = description


	def set_amount( self, amount ):
		"""Cost of item.

		Set amount to 0 if the transaction does not include a one-time
		purchase; for example, when you set up a billing agreement for a
		recurring payment that is not immediately charged.
		
		Character length and limitations: Must not exceed
		$10,000 USD in any currency. No currency symbol.
		Regardless of currency, decimal separator must be a
		period (.). Equivalent to nine characters maximum for USD."""

		v = util.Validator()
		if not v.is_valid_amount( amount ):
			sb = StringIO.StringIO()
			sb.write( 'Amount {0} is not valid. '.format(amount) )
			sb.write( 'Amount has to have exactly two decimal ' )
			sb.write( 'places seaprated by \".\" ' )
			sb.write( '- example: \"50.00\"' )
			raise ValueError( sb.getvalue() )
		
		self._nvp_request['L_AMT'] = amount


	def set_item_number( self, item_number ):
		"""Item number. Character length and limitations: 127 single-byte characters."""

		if len( item_number ) > 127:
			raise ValueError( 'Item number cannot exceed 127 characters' )

		self._nvp_request['L_NUMBER'] = item_number


	def set_quantity( self, quantity ):
		"""Item quantity. Character length and limitations: Any positive integer."""
		quantity = int( quantity )
		if quantity < 0:
			raise ValueError( 'Quantity has to be positive integer' )

		self._nvp_request['L_QTY'] = '{0}'.format(quantity)

				
	def set_tax_amount( self, amount ):
		"""Item sales tax.

		Character length and limitations: Must not exceed
		$10,000 USD in any currency. No currency symbol.
		Regardless of currency, decimal separator must be a
		period (.). Equivalent to nine characters maximum for USD."""
		v = util.Validator()
		if not v.is_valid_amount( amount ):
			sb = StringIO.StringIO()
			sb.write( 'Amount {0} is not valid. '.format(amount) )
			sb.write( 'Amount has to have exactly two decimal ' )
			sb.write( 'places seaprated by \".\" ' )
			sb.write( '- example: \"50.00\"' )
			raise ValueError( sb.getvalue() )
		
		self._nvp_request['L_TAXAMT'] = amount


	def set_weight( self, value, unit ):
		"""Item weight corresponds to the weight of the item. 
		You can pass this data to the shipping carrier as is without 
		having to make an additional database query."""
		val = int(value)
		if val < 0:
			raise ValueError( 'Value has to be positive integer' )

		self._nvp_request['L_ITEMWEIGHTVALUE'] = '{0}'.format( val )
		self._nvp_request['L_ITEMWEGHTUNIT'] = unit

	
	def set_length( self, value, unit ):
		"""Item length corresponds to the length of the item. 
		You can pass this data to the shipping carrier as is without 
		having to make an additional database query."""

		val = int(value)
		if val < 0:
			raise ValueError( 'Value has to be positive integer' )

		self._nvp_request['L_ITEMLENGTHVALUE'] = '{0}'.format( val )
		self._nvp_request['L_ITEMLENGTHUNIT'] = unit


	def set_width( self, value, unit ):
		"""Item width corresponds to the width of the item. 
		You can pass this data to the shipping carrier as is without 
		having to make an additional database query."""

		val = int(value)
		if val < 0:
			raise ValueError( 'Value has to be positive integer' )

		self._nvp_request['L_ITEMWIDTHVALUE'] = '{0}'.format( val )
		self._nvp_request['L_ITEMWIDTHUNIT'] = unit


	def set_height( self, value, unit ):
		"""Item height corresponds to the height of the item. 
		You can pass this data to the shipping carrier as is without 
		having to make an additional database query."""

		val = int(value)
		if val < 0:
			raise ValueError( 'Value has to be positive integer' )

		self._nvp_request['L_ITEMHEIGHTVALUE'] = '{0}'.format( val )
		self._nvp_request['L_ITEMHEIGHTUNIT'] = unit


	def get_nvp_request( self ):
		return copy.deepcopy(self._nvp_request)


	def __str__( self ):
		sb = StringIO.StringIO()
		sb.write( 'instance of PaymentDetailsItem class with ' )
		sb.write( 'the nvpRequest values: ' )
		sb.write( str(self._nvp_request) )
		return sb.getvalue()


	def __del__( self ):
		del (self._nvp_request)




class Payment( RequestFields ):

	"""Payment Details Type Fields. 
	For simple paymets use constructor with amount field. 
	If you want to set tax, or more options, use Constructor that takes PaymentItem list."""

	def __init__( self, amount=None, items=None ):
		self._nvp_request = dict()
		self._nvp_request['CURRENCYCODE'] = 'EUR'
		self._items = list()

		if (items is None) or (len(items) == 0):
			if amount:
				self._set_fieldamount( 'AMT', amount )
			else:
				return

		for item in items:
			self._items.append( item.get_nvp_request() )			

 
	def set_currency( self, currency ):
		"""A three-character currency code. Default: EUR.""" 
		self._nvp_request['CURRENCYCODE'] = currency

	
	def set_shipping_amount( self, amount ):
		"""Total shipping costs for this order. 
		Note: Character length and limitations: 
			Must not exceed $10,000 USD in any currency.
			No currency symbol. 
			Regardless of currency, decimal separator must be a period (.) 
			Equivalent to nine characters maximum for USD."""
		self._set_fieldamount( 'SHIPPINGAMT', amount )


	def set_insurance_amount( self, amount, insurance_option=False ):
		""" Total shipping insurance costs for this order."""
		self._set_fieldamount( 'INSURANCEAMT', amount )
		if insurance_option:
			self._nvp_request['INSURANCEOPTIONOFFERED'] = 'true'

	def set_shipping_discount( self, discount ):
		"""Shipping discount for this order, specified as a negative number."""
		self._set_fieldamount( 'SHIPPINGDISCOUNT', discount )

	def set_handling_amount( self, amount ):
		"""Total handling costs for this order."""
		self._set_fieldamount( 'HANDLINGAMT', amount )

	def set_description( self, description ):
		"""Description of items the customer is purchasing. 
		Character length and limitations: 127 single-byte alphanumeric characters."""
		if (description is None) or (len(description) == 0): return
		if len(description) > 127:
			raise ValueError( 'Description cannot exceed 127 characters' )

		self._nvp_request['DESC'] = description

	def set_custom_field( self, field ):
		"""A free-form field for your own use.
		Character length and limitations: 256 single-byte alphanumeric characters."""
		if (field is None) or (len(field) == 0): return
		if len(field) > 256:
			raise ValueError( 'CustomField cannot exceed 256 characters' )

		self._nvp_request['CUSTOM'] = field


	def set_invoice_number( self, invoice_number ):
		"""Your own invoice or tracking number. 
		Character length and limitations: 127 single-byte alphanumeric characters."""
		if (invoice_number is None) or (len(invoice_number) == 0): return
		if len(invoice_number) > 127:
			raise ValueError( 'invoice_number cannot exceed 127 characters' )

		self._nvp_request['INVNUM'] = invoice_number


	def set_button_source( self, source ):
		"""An identification code for use by third-party applications to identify transactions. 
		Character length and limitations: 32 single-byte alphanumeric characters."""
		if (source is None) or (len(source) == 0): return
		if len(source) > 127:
			raise ValueError( 'source cannot exceed 127 characters' )

		self._nvp_request['BUTTONSOURCE'] = source


	def set_notify_url( self, notify_url ):
		"""Your URL for receiving Instant Payment Notification (IPN) about this transaction. 
		If you do not specify this value in the request, the notification URL 
		from your Merchant Profile is used, if one exists.
		
			Important: The notify URL only applies to DoExpressCheckoutPayment. 

		This value is ignored when set in SetExpressCheckout or GetExpressCheckoutDetails.

		Character length and limitations: 2,048 single-byte alphanumeric characters."""
		if (notify_url is None) or (len(notify_url) == 0): return
		if len(notify_url) > 2048:
			raise ValueError( 'notify_url cannot exceed 2048 characters' )

		self._nvp_request['NOTIFYURL'] = notify_url
	

	def set_note( self, note ):
		"""Note to the seller.
		Character length and limitations: 255 single-byte characters."""
		if (note is None) or (len(note) == 0): return
		if len(note) > 255:
			raise ValueError( 'notify_url cannot exceed 2048 characters' )

		self._nvp_request['NOTETEXT'] = note


	def set_transaction_id( self, transaction_id ):
		"""Transaction identification number of the transaction that was created."""
		self._nvp_request['TRANSACTIONID'] = transaction_id


	def set_allowed_payment_method( self, method ):
		"""The payment method type. 
		Specify the value: InstantPaymentOnly."""
		self._nvp_request['ALLOWEDPAYMENTMETHOD'] = method

	
	def get_nvp_request( self ):

		ff = util.FormatFields()
		
		nvp = copy.deepcopy( self._nvp_request )

		item_amt = 0;
		item_tax = 0;
		
		i = 0
		for item in self._items:
			for k, v in item.items():
				# KEYn VALUE 
				nvp['{0}{1}'.format(k,i)] = v
				
				# item amount
				if k == 'L_AMT': item_amt += int( v.replace('.','') )

				# tax amount
				if k == 'L_TAXAMT': item_tax += int( v.replace('.','') )
			
			i = i + 1

		if item_amt > 0:
			nvp['ITEMAMT'] = ff.get_amount_field( (item_amt/float(100)) )

		if item_tax > 0:
			nvp['TAXAMT'] = ff.get_amount_field( (item_tax/float(100)) )
		
		# set AMT if not set
		if 'AMT' not in nvp:
			# calculate total - tax, shipping etc.
			total = item_amt + item_tax

			if 'HANDLINGAMT' in nvp:
				total += int( nvp['HANDLINGAMT'].replace('.', '') )

			if 'SHIPPINGAMT' in nvp:
				total += int( nvp['SHIPPINGAMT'].replace('.', '') )

			# convert back to two decimals
			total = total / float(100)
			nvp['AMT'] = ff.get_amount_field( total )

		# handling or shipping amount is set but item amount is not set
		if (('HANDLINGAMT' in nvp) or ('SHIPPINGAMT' in nvp)) and ('ITEMAMT' not in nvp):
			# set the amount for itemamt - because itemamt is required when handling amount is set
			nvp['ITEMAMT'] = nvp['AMT']

		return nvp


	def _set_fieldamount( self, field, amount ):
		v = util.Validator()
		if not v.is_valid_amount( amount ):
			sb = StringIO.StringIO()
			sb.write( 'Amount {0} is not valid. '.format(amount) )
			sb.write( 'Amount has to have exactly two decimal ' )
			sb.write( 'places seaprated by \".\" ' )
			sb.write( '- example: \"50.00\"' )
			raise ValueError( sb.getvalue() )
		del ( v )

		ff = util.FormatFields()
		amount = ff.get_amount_field( amount )
		self._nvp_request[field] = amount


class UserSelectedOptions( RequestFields ):

	def __init__( self ):
		self._nvp_request = dict()


	def set_shipping_calculation( self, calculation ):
		"""Describes how the options that were presented to 
		the user were determined."""
		if calculation not in ['CALLBACK', 'FLATRATE']:
			raise ValueError( 'calculation must be CALLBACK or FLATRATE' )

		self._nvp_request['SHIPPINGCALCULATIONMODE'] = calculation


	def set_insurance( self, insurance ):
		"""The Yes/No option that you chose for insurance."""
		flag = 'Yes' if insurance else 'No'
		self._nvp_request['INSURANCEOPTIONSELECTED'] = flag


	def set_default_shipping_option( self, option ):
		"""Is true if the buyer chose the default shipping option."""
		flag = 'true' if option else 'false'
		self._nvp_request['SHIPPINGOPTIONISDEFAULT'] = flag
		if option:
			self._nvp_request['SHIPPINGOPTIONNAME'] = flag


	def set_shipping_amount( self, amount ):
		"""The shipping amount that was chosen by the buyer 
		Limitations:

			- Must not exceed $10,000 USD in any currency.
			- No currency symbol. 
			- Must have two decimal places, decimal separator must be a period (.)."""
		v = util.Validator()
		if not v.is_valid_amount( amount ):
			sb = StringIO.StringIO()
			sb.write( 'Amount {0} is not valid. '.format(amount) )
			sb.write( 'Amount has to have exactly two decimal ' )
			sb.write( 'places seaprated by \".\" ' )
			sb.write( '- example: \"50.00\"' )
			raise ValueError( sb.getvalue() )
		del ( v )

		ff = util.FormatFields()
		amount = ff.get_amount_field( amount )
		self._nvp_request['SHIPPINGOPTIONAMOUNT'] = amount


	def get_nvp_request( self ):
		return self._nvp_request