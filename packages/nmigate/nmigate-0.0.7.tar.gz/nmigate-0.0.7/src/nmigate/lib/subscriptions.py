from nmigate.util.wrappers import postProcessXml
import requests 
import xmltodict
from nmigate.lib.nmi import Nmi
from nmigate.lib.plans import Plans
import functools
from urllib.parse import parse_qs, urlparse
from datetime import datetime, date, timedelta

class Subscriptions(Nmi):
    def __init__(self, token, org):
        super().__init__(token, org)
        self.plans = Plans(token, org)

    def postProcessingOutput(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Before
            nmi_operation = func(*args, **kwargs)

            # clean unwished loggin data
            if 'req' in nmi_operation and 'security_key' in nmi_operation['req']:
                nmi_operation['req'].pop('security_key')

            # pre process nmi_detail 
            nmi_response = nmi_operation.pop("response")
            nmi_response_parsed_url = urlparse(nmi_response.text)
            nmi_response_cleared = parse_qs(nmi_response_parsed_url.path)
            

            # create new dictionary with all the data
            nmi_operation['nm_response'] = nmi_response_cleared
            nmi_operation["date"] = datetime.now()
            
            # Validate if nmi response is successfull
            if nmi_response_cleared['response_code'][0] == '100':
                nmi_operation['successfull'] = True
            else:
                nmi_operation['successfull'] = False
            
            new_res={}
            try:
                for key in nmi_operation['nmi_response']:
                    new_res[key] = nmi_operation['nmi_response'][key][0]
            except:
                pass
            nmi_operation['nmi_response'] = new_res 
            return nmi_operation
        
        return wrapper

    
    @postProcessingOutput   
    def custom_sale_using_vault(self, plan_id, customer_vault_id, create_customer_vault=False):

        plan = self.plans.get_plan(plan_id)
        plan_amout = plan['plan_amount']

        data = {
            "type": "sale",
            "recurring": "add_subscription",
            "initiated_by": "merchant",
            "security_key": self.security_token,
            "amount": str(plan_amout),
            "customer_vault_id": customer_vault_id,
            "plan_id": plan_id,
        }
        data["customer_vault"] = "add_customer" if create_customer_vault else None
        
        response = requests.post(url="https://secure.networkmerchants.com/api/transact.php", data=data)
        return {"response": response, "req":{"customer_vault_id": customer_vault_id, "plan_id": plan_id, "total": plan_amout},  "type": 'set_subscription_with_sale_and_vault', "org": self.org}



    """  if amount = 0 then its a simple subscription, if amount = 1 then its a subscription with sale """
    
    @postProcessingOutput   
    def custom_sale_using_vault_month_frequency(self, request_sub):
        
        data = {
            "type": "sale",
            "recurring": "add_subscription",
            "initiated_by": "merchant",
            "security_key": self.security_token,
            "customer_vault_id": request_sub['user_id'],
            "amount": request_sub['total_amount'],
            "plan_payments": request_sub['custom_subscription_info']['plan_payments'],
            "plan_amount": request_sub['custom_subscription_info']['plan_amount'],
            "month_frequency": request_sub['custom_subscription_info']['month_frequency'],   
            "day_of_month": request_sub['custom_subscription_info']['day_of_month'],   
        }

        if float(request_sub['total_amount']) == 0:
            del data['type']
            del data['amount']

        response = requests.post(url="https://secure.networkmerchants.com/api/transact.php", data=data)
        return {"response": response, "req": request_sub,  "type": 'set_custom_subscription_with_sale_and_vault_month_config', "org": self.org}


    
    @postProcessingOutput   
    def custom_with_sale_and_vault_day_frequency(self, request_sub):
            
        data = {
            "type": "sale",
            "recurring": "add_subscription",
            "initiated_by": "merchant",
            "security_key": self.security_token,
            "amount": request_sub['total_amount'],
            "customer_vault_id": request_sub['user_id'],
            "plan_payments": request_sub['custom_subscription_info']['plan_payments'],
            "plan_amount": request_sub['custom_subscription_info']['plan_amount'],
            "day_frequency": request_sub['custom_subscription_info']['day_frequency'],   
        }
        
        if float(request_sub['total_amount']) == 0:
            del data['type']
            del data['amount']
            
        response = requests.post(url="https://secure.networkmerchants.com/api/transact.php", data=data)
        return {"response": response, "req": request_sub,  "type": 'set_custom_subscription_with_sale_and_vault_day_frequency', "org": self.org}


    @postProcessXml
    def get_info(self, id):
        url = "https://secure.nmi.com/api/query.php"
        query = {
            "report_type": "recurring",
            "security_key": self.security_token,
            "subscription_id": id
        }
        response = requests.post(url=url, data=query)        
        return response


    
    @postProcessingOutput   
    def delete(self, subscription_id):
        data = {
            "recurring": "delete_subscription",
            "security_key": self.security_token,
            "subscription_id": subscription_id,
        }
        response = requests.post(url="https://secure.networkmerchants.com/api/transact.php", data=data)
        return {"response": response, "req": subscription_id,  "type": 'delete_subscription', "org": self.org}


    
    @postProcessingOutput
    def pause_subscription(self, subscription_id, pause):
        data = {
            "recurring": "update_subscription",
            "security_key": self.security_token,
            "subscription_id": subscription_id,
            "paused_subscription": str(pause).lower(),
        }
        response = requests.post(url="https://secure.networkmerchants.com/api/transact.php", data=data)
        return {"response": response, "req": subscription_id,  "type": 'pause_subscription', "org": self.org}