def index():
    # #Create Payment Using PayPal Sample
    # This sample code demonstrates how you can process a
    # PayPal Account based Payment.
    # API used: /v1/payments/payment
   
    from paypalrestsdk import Payment
    from paypalrestsdk import set_config
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    set_config(mode=settings.paypal_mode, # sandbox or live
               client_id=settings.paypal_client_id,
               client_secret=settings.paypal_client_secret)
    
    # ###Payment
    # A Payment Resource; create one using
    # the above types and intent as 'sale'
    payment = Payment({
      "intent":  "sale",
    
      # ###Payer
      # A resource representing a Payer that funds a payment
      # Payment Method as 'paypal'
      "payer":  {
        "payment_method":  "paypal" },
    
      # ###Redirect URLs
      "redirect_urls": {
        "return_url": "http://localhost:3000/payment/execute",
        "cancel_url": "http://localhost:3000/" },
    
      # ###Transaction
      # A transaction defines the contract of a
      # payment - what is the payment for and who
      # is fulfilling it.
      "transactions":  [ {
    
        # ### ItemList
        "item_list": {
          "items": [{
            "name": "Test item",
            "sku": "001",
            "price": "5.00",
            "currency": "USD",
            "quantity": 2 },
            {
            "name": "Test item 2",
            "sku": "002",
            "price": "125.70",
            "currency": "USD",
            "quantity": 3}]},
    
        # ###Amount
        # Let's you specify a payment amount.
        "amount":  {
          "total":  "387.10",
          "currency":  "USD" },
        "description":  "This is the payment transaction description." } ] } )
    
    # Create Payment and return status
    if payment.create():
      print("Payment[%s] created successfully"%(payment.id))
      # Redirect the user to given approval url
      for link in payment.links:
        if link.method == "REDIRECT":
          redirect_url = link.href
          print("Redirect for approval: %s"%(redirect_url))
    else:
      print("Error while creating payment:")
      print(payment.error)