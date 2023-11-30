from nmigate.lib import log, postProcessingOutput
import requests

@log
@postProcessingOutput   
def validate_billing_id(self, customer_vault_id, billing_id):
    data = {
        "type": "validate",
        "security_key": self.security_token,
        "customer_vault_id": customer_vault_id,
        "billing_id": billing_id,
    }

    response = requests.post(url="https://secure.networkmerchants.com/api/transact.php", data=data)
    return {"response": response, "type": 'validate_billing_id', "org": self.org}
    
@log
@postProcessingOutput   
def add_billing_info(self, customer_id, token, billing_info, billing_id):
    data = {
        "customer_vault": "add_billing",
        "payment": "creditcard",
        "security_key": self.security_token,
        "payment_token": token,
        "customer_vault_id": customer_id,   
        "billing_id": billing_id 
    }
    data.update(billing_info) 
    res = requests.post(url="https://secure.nmi.com/api/transact.php", data=data)
    return {"response": res, "type": 'add_billing_info', "org": self.org}


@log
@postProcessingOutput   
def update_billing_info(self, id, token, billing_id, billing_info):
    data = {
        "customer_vault": "update_billing",
        "payment": "creditcard",
        "security_key": self.security_token,
        "payment_token": token,
        "customer_vault_id": id,
        "billing_id": billing_id
    }
    data.update(billing_info) 
    response = requests.post(url="https://secure.nmi.com/api/transact.php", data=data)
    return {"response": response, "type": 'update_billing_info', "org": self.org}

@log      
@postProcessingOutput     
def delete_billing_info(self, id, billing_id):
    data = {
        "customer_vault": "delete_billing",
        "security_key": self.security_token,
        "customer_vault_id": id,
        "billing_id": billing_id
    }
    response = requests.post(url="https://secure.nmi.com/api/transact.php", data=data)
    return {"response": response, "type": 'delete_billing_info', "org": self.org}


@log  
@postProcessingOutput     
def change_subscription_billing(self, request):
    data = {
        "recurring": "update_subscription",
        "security_key": self.security_token,
        "customer_vault_id": request.get('user_id'),
        "subscription_id": request.get('subscription_id'),
        "billing_id": request.get('billing_id')
    }
    
    response = requests.post(url="https://secure.nmi.com/api/transact.php", data=data)
    return {"response": response, "req": request,  "type": 'update_subscription_billing', "org": self.org}


