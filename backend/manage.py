from dte import DTE
import sys
import re

class Manager(object):
    def __init__(self):
        self.bills = []
    
    def add_bill(self, date, reference, sender_nit, receiver_nit, value, iva, total):#I have to add "reference"
        
        date_response = self.check_date(date)
        reference_response = self.check_reference(reference)
        sender_nit_response = self.check_sender_nit(sender_nit)
        receiver_nit_response = self.check_receiver_nit(receiver_nit)
        value_response = self.check_value(value)
        iva_response = self.check_iva(iva, value)
        total_response = self.check_total(value, iva, total)
        
        new = DTE(date_response, reference_response, sender_nit_response, receiver_nit_response, value_response, iva_response, total_response)
        self.bills.append(new)
        return True
    
    def check_date(self, date):
        result = re.search(r"([0-2][0-9]|3[0-1])(\/|-)(0[1-9]|1[0-2])\2(\d{4})", date)
        if result:
            return result.group()
        else:
            return None#Date from XML file does not match
    
    def check_reference(self, reference):
        if len(reference) < 41:
            return reference
        else:
            return None
    
    def check_sender_nit(self, sender_nit):
        result = re.search(r"(\b\d{1,21}\b)", sender_nit)
        if result:
            v_digit = int(result.group()[-1])
            number = str(result.group()[:-1])

            plus = 0
            length = len(number) + 1
            for i in number:
                plus += int(i) * length
                length -= 1

            mod_operation = plus % 11
            minus_operation = 11 - mod_operation
            k = minus_operation % 11
            validate_nit = ''
            if (k < 10) and (k == v_digit):
                validate_nit = str(number)+str(v_digit)
                return validate_nit
            else:
                return None#k and v_digit are not the same
        else:
            return None#IVA from XML file does not match
    
    def check_receiver_nit(self, receiver_nit):
        result = re.search(r"(\b\d{1,21}\b)", receiver_nit)
        if result:
            v_digit = int(result.group()[-1])
            number = str(result.group()[:-1])

            plus = 0
            length = len(number) + 1
            for i in number:
                plus += int(i) * length
                length -= 1

            mod_operation = plus % 11
            minus_operation = 11 - mod_operation
            k = minus_operation % 11
            validate_nit = ''
            if (k < 10) and (k == v_digit):
                validate_nit = str(number)+str(v_digit)
                return validate_nit
            else:
                return None#k and v_digit are not the same
        else:
            return None#IVA from XML file does not match
    
    def check_value(self, value):
        result = re.search(r"\b\d{1,8}\.\d{2}\b", value)
        if result:
            return result.group()
        else:
            return None#Value from XML file does not match
    
    def check_iva(self, iva, value):
        
        value_response = self.check_value(value)
        
        if value_response is not None:
            
            value_response = float(self.check_value(value))
            
            result = re.search(r"\b\d{1,7}\.\d{2}\b", iva)
            if result:
                valid_iva = float(result.group())
                iva_operation = round(value_response * 0.12, 2)
                
                if valid_iva == iva_operation:
                    return valid_iva
                else:
                    return None#"IVA's are different" 
            else:
                return None#IVA from xml file does not match
        else:
            return None#'Value is None'
    
    def check_total(self,value, iva, total):
        value_response = self.check_value(value)
        iva_response = self.check_iva(iva, value)
        
        if (value_response is not None) and (iva_response is not None):
            result = re.search(r"\b\d{1,7}\.\d{2}\b", total)
            
            value_response = float(self.check_value(value))
            iva_response = float(self.check_iva(iva, value))
            if result:
                valid_total = float(result.group())
                total_operation = float(value_response + iva_response)
                
                if valid_total == total_operation:
                    return valid_total
                else:
                    return None#Totals are different" 
            else:
                return None#Total from XML file does not match
        else:
            return None#value_response and iva_response are None
    
    def get_bills(self):
        json_bill = []
        for i in self.bills:
            bill = {
                'fecha':i.date,
                'reference':i.reference,
                'nit emisor':i.sender_nit,
                'nit receptor':i.receiver_nit,
                'valor':i.value,
                'IVA':i.iva,
                'total':i.total
            }
            json_bill.append(bill)
        return json_bill