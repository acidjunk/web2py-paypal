def index():
    # import the required modules
    import paypalnvp.core
    import paypalnvp.requests
    import paypalnvp.fields
    
    # set user - these are your credentials from paypal
    user = paypalnvp.core.BaseProfile(
       username=settings.paypal_username, 
       password=settings.paypal_password )
    user.set_signature( settings.paypal_signature )
    
    # create items (items from a shopping basket)
    item1 = paypalnvp.fields.PaymentItem()
    item1.set_name( 'Tazza da caffe' )
    item1.set_description('Splendida tazza da caffe bianca')
    item1.set_amount( '8.00' );
    
    item2 = paypalnvp.fields.PaymentItem()
    item2.set_name( 'Biscottiera' )
    item2.set_description('Pregiata biscottiera in porcellana Ming')
    item2.set_amount( '24.00' );
    
    # create payment payment from the items
    payment = paypalnvp.fields.Payment( items=[item1, item2] )
    payment.set_currency( 'EUR' )
    
    # create set express checkout - the first paypal request
    set_ec = paypalnvp.requests.SetExpressCheckout( 
        payment, URL('paypalnvp', 'success', scheme=True), 
        URL('paypalnvp', 'cancel', scheme=True) )
    
    # create new instance of paypal nvp, send request e set response
    paypal = paypalnvp.core.PayPal( user )
    paypal.set_response( set_ec )   
    
    api_response = set_ec.get_nvp_response()
    redirect_url = paypal.get_redirect_url( set_ec )
    redirect(redirect_url)
    
def succes():
    return dict()

def cancel():
    return dict()