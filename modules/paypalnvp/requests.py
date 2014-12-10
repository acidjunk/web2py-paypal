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
import copy


import core
import util
import fields


class SetExpressCheckout( core.Request ):
	"""Instance is used for SetExpressCheckout request.
	This request initiates an Express Checkout transaction."""

	def __init__( self, payment, return_url, cancel_url ):
		"""PayPal recommends that the return_url be the final review page 
		on which the customer confirms the order and payment or billing agreement.

		PayPal recommends that the cancel_url be the original page on which the
		customer chose to pay with PayPal or establish a billing agreement."""
	
		if payment is None or return_url is None or cancel_url is None:
			raise ValueError( 'Arguments cannot be null' )

		if not isinstance(payment, fields.Payment):
			raise ValueError( 'payment must be an instance of class <Payment>.' )

		if len(return_url) > 2048:
			raise ValueError( 'return_url cannot be longer than 2048 characters.' )

		if len(cancel_url) > 2048:
			raise ValueError( 'cancel_url cannot be longer than 2048 characters.' )
 
		self._nvp_response = dict()
		self._nvp_request = dict()
		self._nvp_request['METHOD'] = 'SetExpressCheckout'

		self._shipping_options = list()
		self._billing_agreement = list()

		nvp = copy.deepcopy( payment.get_nvp_request() )
		self._nvp_request.update( nvp )

		self._nvp_request['RETURNURL'] = return_url
		self._nvp_request['CANCELURL'] = cancel_url


	def set_token(self, token ):
		if token is None or len(token) != 20:
			raise ValueError( 'Invalid token argument' )

		self._nvp_request['TOKEN'] = token


	def set_max_amount( self, max_amount ):
		"""The expected maximum total amount of the complete 
		order, including shipping cost and tax charges.

		If the transaction does not include a one-time purchase, this field is ignored.

		Limitations: 
	
			- Must not exceed $10,000 USD in any currency.
			- No currency symbol. 
			- Must have two decimal places, decimal separator must be a period (.), 
			  and no thousands separator."""
		v = util.Validator()
		if not v.is_valid_amount( max_amount ):
			sb = StringIO.StringIO()
			sb.write( 'Amount {0} is not valid. '.format(max_amount) )
			sb.write( 'Amount has to have exactly two decimal ' )
			sb.write( 'places seaprated by \".\" ' )
			sb.write( '- example: \"50.00\"' )
			raise ValueError( sb.getvalue() )
		del ( v )

		ff = util.FormatFields()
		amount = ff.get_amount_field( max_amount )
		self._nvp_request['MAXAMT'] = max_amount


	def set_callback( self, callback ):
		"""URL to which the callback request from PayPal is sent.
		It must start with HTTPS for production integration. 
		It can start with HTTPS or HTTP for sandbox testing."""

		if len(callback) > 1024:
			raise ValueError( 'Callback can be maximum 1024 in length' )

		self._nvp_request['CALLBACK'] = callback


	def set_callback_timeout( self, timeout ):
		"""An override for you to request more or less time to 
		be able to process the callback request and respond.
		The acceptable range for the override is 1 to 6 seconds."""
		try:
			timeout = int(timeout)
		except:
			raise ValueError( 'timeout must be an integer' )

		if timeout < 1 or timeout > 6:
			raise ValueError( 'Timeout has to be between 1 - 6' )

		self._nvp_request['CALLBACKTIMEOUT'] = '%d' % timeout


	def set_require_confirmed_shipping( self, required ):
		"""Indicates that you require that the customer's shipping 
		address on file with PayPal be a confirmed address.
		
		Setting this field overrides the setting you have specified 
		in your Merchant Account Profile."""

		req = '1' if required else '0'
		self._nvp_request['REQCONFIRMSHIPPING'] = req


	def set_no_shipping( self, no_shipping ):
		"""Indicates that on the PayPal pages, no shipping address 
		fields should be displayed whatsoever."""

		shipping = '1' if no_shipping else '0'
		self._nvp_request['NOSHIPPING'] = shipping


	def set_allow_note( self, allow_note ):
		"""Indicates that the customer may enter a note to the 
		merchant on the PayPal page during checkout. 

		The note is returned in the GetExpressCheckoutDetails response 
		and the DoExpressCheckoutPayment response."""

		note = '1' if allow_note else '0'
		self._nvp_request['ALLOWNOTE'] = note


	def set_address_override( self, address_override ):
		"""Indicates that the PayPal pages should display the 
		shipping address set by you in this SetExpressCheckout 
		request, not the shipping address on file with PayPal for this customer.

		Displaying the PayPal street address on file does not allow 
		the customer to edit that address.

		Set address using set_address(ShipToAddress address) method."""

		override = '1' if address_override else '0'
		self._nvp_request['ADDROVERRIDE'] = override	


	def set_local_code( self, local_code ):
		"""Locale of pages displayed by PayPal during Express Checkout."""
		self._nvp_request['LOCALECODE'] = local_code

	def set_page_style( self, page_style ):
		"""Sets the Custom Payment Page Style for payment pages 
		associated with this button/link. 
		This value corresponds to the HTML variable page_style 
		for customizing payment pages. 

		The value is the same as the Page Style Name you chose when adding 
		or editing the page style from the Profile subtab of the 
		My Account tab of your PayPal account.
 
		Character length and limitations: 30 single-byte alphabetic characters."""
		if len(page_style) > 30:
			raise ValueError( 'Character length exceeded 30 characters.' )

		self._nvp_request['PAGESTYLE'] = page_style

	def set_image( self, img_url ):
		"""URL for the image you want to appear at the top left of the payment page. 
		The image has a maximum size of 750 pixels wide by 90 pixels high. 

		PayPal recommends that you provide an image that is stored on a secure (https) server.
		If you do not specify an image, the business name is displayed.

		Character length and limit: 127 single-byte alphanumeric characters."""
		
		if len(img_url) > 127:
			raise ValueError( 'Character length exceeded 127 characters.' )

		self._nvp_request['HDRIMG'] = img_url


	def set_border_color( self, hex_color ):
		"""Sets the border color around the header of the payment page.
		The border is a 2-pixel perimeter around the header space, which is 
		750 pixels wide by 90 pixels high. By default, the color is black.

		Character length and limitation: Six character HTML hexadecimal 
		color code in ASCII."""

		v = util.Validator()
		if not v.is_valid_hexcolor( hex_color ):
			raise ValueError( 'Hex color {0} is not valid.'.format(hex_color) )

		self._nvp_request['HDRBORDERCOLOR'] = hex_color

	def setBackgroundColor( self, hex_color ):
		"""Sets the background color for the header of the payment page. 
		By default, the color is white.

		Character length and limitation: 

			Six character HTML hexadecimal color code in ASCII."""
		v = util.Validator()
		if not v.is_valid_hexcolor( hex_color ):
			raise ValueError( 'Hex color {0} is not valid.'.format(hex_color) )

		self._nvp_request['HDRBACKCOLOR'] = hex_color


	def set_payflow_color( self, hex_color ):
		"""Sets the background color for the payment page.
		By default, the color is white.

		Character length and limitation: 

			Six character HTML hexadecimal color code in ASCII."""
		v = util.Validator()
		if not v.is_valid_hexcolor( hex_color ):
			raise ValueError( 'Hex color {0} is not valid.'.format(hex_color) )

		self._nvp_request['PAYFLOWCOLOR'] = hex_color


	def set_payment_action( self, payment_action ):
		"""How you want to obtain payment:
			
			- 'Sale' indicates that this is a final sale for which you are 
			requesting payment. (Default)

			- 'Authorization' indicates that this payment is a basic authorization 
			subject to settlement with PayPal Authorization & Capture.

			- 'Order' indicates that this payment is an order authorization subject 
			to settlement with PayPal Authorization & Capture.

		If the transaction does not include a one-time purchase, this field is ignored.

		Note:
		You cannot set this value to 'Sale' in SetExpressCheckout request and then 
		change this value to 'Authorization' or 'Order' on the final API 
		DoExpressCheckoutPayment request.
		If the value is set to 'Authorization' or 'Order' in SetExpressCheckout, the 
		value may be set to 'Sale' or the same value (either 'Authorization' or 'Order') 
		in DoExpressCheckoutPayment."""

		if payment_action not in ['Sale','Authorization','Order']:
			raise ValueError( 'payment_action must be Sale, Authorization or Order.' )

		self._nvp_request['PAYMENTACTION'] = payment_action


	def set_email( self, email ):
		"""Email address of the buyer as entered during checkout.
		PayPal uses this value to pre-fill the PayPal membership sign-up 
		portion of the PayPal login page.

		Character length and limit: 127 single-byte alphanumeric characters."""

		if len(email) > 127:
			raise ValueError( 'Character length exceeded 127 characters.' )

		self._nvp_request['EMAIL'] = email


	def set_solution_type( self, solution_type ):
		"""Type of checkout flow:

			- 'Sole' Express Checkout for auctions;

			- 'Mark' Normal Express Checkout."""

		if solution_type not in ['Sole','Mark']:
			raise ValueError( 'solution_type must be Sole or Mark.' )

		self._nvp_request['SOLUTIONTYPE'] = solution_type
		
	
	def set_landing_page( self, landing_page ):
		"""Type of PayPal page to display:

			- 'Billing' non-PayPal account;

			- 'Login' PayPal account login."""

		if landing_page not in ['Billing','Login']:
			raise ValueError( 'landing_page must be Billing or Login.' )

		self._nvp_request['LANDINGPAGE'] = landing_page


	def set_channel_type( self, channel_type ):
		"""Type of channel::

			- 'Merchant' non-auction seller;

			- 'eBayItem' eBay auction."""

		if channel_type not in ['Merchant','eBayItem']:
			raise ValueError( 'channel_type must be Merchant or eBayItem.' )

		self._nvp_request['CHANNELTYPE'] = channel_type


	def set_giropay_success_url( self, url ):
		"""The URL on the merchant site to redirect to after a successful 
		giropay payment.
		Use this field only if you are using giropay or bank transfer 
		payment methods in Germany."""
		self._nvp_request['GIROPAYSUCCESSURL'] = url

	def set_giropay_cancel_url( self, url ):
		"""The URL on the merchant site to redirect to after a unsuccessful 
		giropay payment.
		Use this field only if you are using giropay or bank transfer 
		payment methods in Germany."""
		self._nvp_request['GIROPAYCANCELURL'] = url

	def set_banktx_pending_url( self, url ):
		"""The URL on the merchant site to transfer to after a 
		bank transfer payment.
		Use this field only if you are using giropay or bank transfer 
		payment methods in Germany."""
		self._nvp_request['BANKTXNPENDINGURL'] = url

	def set_address( self, address ):
		if not isinstance(address, fields.Address):
			raise ValueError( 'address must be an instance of <Address> class.' )

		self._nvp_request.update( address.get_nvp_request() )
 

	def set_shipping_options( self, options ):
		if not isinstance( options, list ):
			raise ValueError( 'options must be a list of ShippingOptions instances.' )
		
		if len(options) == 0:
			raise ValueError( 'You did not supply options.' )

		for option in options:
			self._shipping_options.append( option.get_nvp_request() )

	def set_billing_agreement( self, agreements ):
		if not isinstance( agreements, list ):
			raise ValueError( 'agreements must be a list of BillingAgreement instances.' )
		
		if len(agreements) == 0:
			raise ValueError( 'You did not supply options.' )

		for agreement in agreements:
			self._billing_agreement.append( agreement.get_nvp_request() )

	def set_buyer_details( self, buyer ):
		"""The unique identifier provided by eBay for this buyer.
		The value may or may not be the same as the username. 
		In the case of eBay, it is different. 

		Character length and limitations: 255 single-byte characters."""
		self._nvp_request['BUYERUSERNAME'] = buyer

	def set_shipping_address( self, address ):
		if not isinstance(address, fields.ShipToAddress):
			raise ValueError( 'address must be an instance of <ShipToAddress> class.' )

		self._nvp_request.update( address.get_nvp_request() )


	def set_nvp_response( self, nvp_response ):
		if not isinstance( nvp_response, dict ):
			raise ValueError( 'nvp_response must be a <dict>.' )
		self._nvp_response = copy.deepcopy( nvp_response )


	def get_nvp_response( self ):
		return copy.deepcopy( self._nvp_response )


	def get_nvp_request( self ):
		
		nvp = copy.deepcopy( self._nvp_request )
		
		# shipping options
		i = 0
		for option in self._shipping_options:
			for k, v in option:
				# KEYn VALUE
				nvp['{0}{1}'.format(k,i)] = v	

		# billing agreement 
		i = 0
		for agreement in self._billing_agreement:
			for k, v in agreement:
				# KEYn VALUE
				nvp['{0}{1}'.format(k,i)] = v

		return nvp


class GetExpressCheckoutDetails( core.Request ):
	"""Obtain the available balance for a PayPal account."""

	def __init__( self, token ):
		"""payment	Should be the same as for GetExpressCheckoutDetails
		token	PayPal token"""

		if (token is None) or (len(token) != 20):
			raise ValueError( 'Invalid token argument' )

		self._nvp_response = dict()
		self._nvp_request = dict()
		self._nvp_request['METHOD'] = 'GetExpressCheckoutDetails'
		
		nvp = copy.deepcopy( payment.get_nvp_request() )
		self._nvp_request.update( nvp )
		self._nvp_request['TOKEN'] = token

	
	def get_nvp_request( self ):
		return copy.deepcopy(self._nvp_request)


	def set_nvp_response( self, nvp_response ):
		if not isinstance( nvp_response, dict ):
			raise ValueError( 'nvp_response must be a <dict>.' )
		self._nvp_response = copy.deepcopy( nvp_response )


	def get_nvp_response( self ):
		return copy.deepcopy( self._nvp_response )


class DoExpressCheckoutPayment( core.Request ):
	"""Obtain the available balance for a PayPal account."""

	def __init__( self, payment, token, payment_action, payer_id ):
		"""payment	Should be the same as for SetExpressCheckout
		token	PayPal token
		payment_action How you want to obtain payment
		payerId	Unique PayPal customer account identification 
				number as returned by GetExpressCheckoutDetails response."""

		if not isinstance(payment, fields.Payment ):
			raise ValueError( 'payment must be an instance of class <Payment>.' )

		if (token is None) or (len(token) != 20):
			raise ValueError( 'Invalid token argument' )

		if payment_action not in ['Sale','Authorization','Order']:
			raise ValueError( 'payment_action must be Sale, Authorization or Order.' )

		if (payer_id is None) or (len(payer_id) != 13):
			raise ValueError( 'Invalid payer id' )

		self._nvp_response = dict()
		self._nvp_request = dict()
		self._nvp_request['METHOD'] = 'DoExpressCheckoutPayment'
		
		nvp = copy.deepcopy( payment.get_nvp_request() )
		self._nvp_request.update( nvp )
		self._nvp_request['TOKEN'] = token
		self._nvp_request['PAYMENTACTION'] = payment_action
		self._nvp_request['PAYERID'] = payer_id


	def set_return_fmf( self, fmf ):
		"""Flag to indicate whether you want the results returned 
		by Fraud Management Filters. By default this is false."""
		self._nvp_request['RETURNFMFDETAILS'] = '1' if fmf else '0'


	def set_user_selected_options( self, user_options ):
		"""Sets user selected options."""
		if not isinstance(user_options, fields.UserOptions):
			raise ValueError( 'user_options must be an instance of class <UserOptions>.' )

		nvp = copy.deepcopy( user_options.get_nvp_request() )
		self._nvp_request.update( nvp )

		
	def set_address( self, address ):
		"""Sets address fields."""
		if not isinstance(address, fields.Address):
			raise ValueError( 'address must be an instance of class <Address>.' )

		nvp = copy.deepcopy( address.get_nvp_request() )
		self._nvp_request.update( nvp )

	
	def get_nvp_request( self ):
		return copy.deepcopy(self._nvp_request)


	def set_nvp_response( self, nvp_response ):
		if not isinstance( nvp_response, dict ):
			raise ValueError( 'nvp_response must be a <dict>.' )
		self._nvp_response = copy.deepcopy( nvp_response )


	def get_nvp_response( self ):
		return copy.deepcopy( self._nvp_response )
	


class GetBalance( core.Request ):
	"""Obtain the available balance for a PayPal account."""

	def __init__( self ):
		self._nvp_response = None
		self._nvp_request = dict()
		self._nvp_request['METHOD'] = 'GetBalance'


	def set_all_currencies( self, all_currencies=False):
		self._nvp_request['RETURNALLCURRENCIES'] = '1' if all_currencies else '0'


	def get_nvp_request( self ):
		return copy.deepcopy(self._nvp_request)


	def set_nvp_response( self, nvp_response ):
		if not isinstance( nvp_response, dict ):
			raise ValueError( 'nvp_response must be a <dict>.' )
		self._nvp_response = copy.deepcopy( nvp_response )


	def get_nvp_response( self ):
		return copy.deepcopy( self._nvp_response )


	def __del__( self ):
		if self._nvp_response:
			del (self._nvp_response)

		if self._nvp_request:
			del ( self._nvp_request )
			