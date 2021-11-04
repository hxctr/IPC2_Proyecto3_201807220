from dte import DTE
import sys
import re
from xml.dom import minidom
import datetime

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
        
        if (date_response is not None) and (reference_response is not None) and (sender_nit_response is not None) and (receiver_nit_response is not None) and (value_response is not None) and (iva_response is not None) and (total_response is not None):
            new = DTE(date_response, reference_response, sender_nit_response, receiver_nit_response, value_response,    iva_response, total_response)
            self.bills.append(new)
        else:
            print('Error in a bill')
        return True
    
    def check_date(self, date):
        result = re.search(r"\b\d{2}/\d{2}/\d{4}\b", date)
        if result:
            date_result = result.group()
            day, month, year = date_result.split("/")
            
            try:
                date_test = datetime.datetime(int(year), int(month), int(day))
                return date_result
            except Exception as e:
                return None#Date is not valid
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
        result = re.search(r"\b\d{1,8}\.\d{2,}", value)
        if result:
            digits, decimals = result.group().split(".")
            truncate_number = digits +'.'+decimals[0]+decimals[1]
            return truncate_number
            # return result.group()
        else:
            return None#Value from XML file does not match
    
    def check_iva(self, iva, value):
        
        value_response = self.check_value(value)
        
        if value_response is not None:
            
            value_response = float(self.check_value(value))
            
            result = re.search(r"\b\d{1,7}\.\d{2,}", iva)
            if result:
                
                digits, decimals = result.group().split(".")
                truncate_iva = digits +'.'+decimals[0]+decimals[1]
            
                # valid_iva = float(result.group())
                valid_iva = float(truncate_iva)
                
                iva_operation = round(value_response * 0.12, 2)
                
                if valid_iva == iva_operation:
                    return valid_iva
                else:
                    return None#"IVA's are different" 
            else:
                return None#IVA from xml file does not match
        else:
            print('La cadena no contiene ninguna IVA valido')
            return None#'Value is None'
    
    def check_total(self,value, iva, total):
        value_response = self.check_value(value)
        iva_response = self.check_iva(iva, value)
        
        if (value_response is not None) and (iva_response is not None):
            result = re.search(r"\b\d{1,7}\.\d{2,}", total)
            
            value_response = float(self.check_value(value))
            iva_response = float(self.check_iva(iva, value))
            if result:
                
                digits, decimals = result.group().split(".")
                truncate_total = digits +'.'+decimals[0]+decimals[1]

                
                # valid_total = float(result.group())
                valid_total = float(truncate_total)
                total_operation = float(value_response + iva_response)
                
                if valid_total == total_operation:
                    return valid_total
                else:
                    return None#Totals are different" 
            else:
                return None#Total from XML file does not match
        else:
            return None#value_response and iva_response are None
        
    def get_authorization(self):
        sort_by_date = set(k.date for k in self.bills)
        document = minidom.Document()
        root = document.createElement("LISTAAUTORIZACIONES")
        
        for i in sort_by_date:
            references =  []
            autorizacion = document.createElement("AUTORIZACION")
            root.appendChild(autorizacion)
            # print('---------------',i,'---------------')
            fecha = document.createElement("FECHA")
            fecha.appendChild(document.createTextNode(str(i)))
            autorizacion.appendChild(fecha)
            
            errores = document.createElement("ERRORES") 
            autorizacion.appendChild(errores)
                    
            listado_autorizaciones = document.createElement("LISTADO_AUTORIZACIONES")
            autorizacion.appendChild(listado_autorizaciones)
            
            counter = 0
            duplicate_reference = ''
            for k in self.bills:
                if k.reference in references:
                    duplicate_reference = k.reference
                counter += 1
                
                if k.date == i:
                    
                    aprobacion = document.createElement("APROBACION")
                    listado_autorizaciones.appendChild(aprobacion)
                    
                    nit_emisor = document.createElement("NIT_EMISOR")
                    nit_emisor.setAttribute("ref", k.reference)
                    nit_emisor.appendChild(document.createTextNode(k.sender_nit))
                    aprobacion.appendChild(nit_emisor)
                    
                    split_date = k.date.split("/")
                    
                    codigo_aprobacion = document.createElement("CODIGO_APROBACION")
                    codigo_aprobacion.appendChild(document.createTextNode(split_date[2]+split_date[1]+split_date[0]))
                    aprobacion.appendChild(codigo_aprobacion)
                    
                    
                    nit_receptor = document.createElement("NIT_RECEPTOR")
                    nit_receptor.appendChild(document.createTextNode(k.receiver_nit))
                    aprobacion.appendChild(nit_receptor)
                    
                    valor = document.createElement("VALOR")
                    valor.appendChild(document.createTextNode(k.value))
                    aprobacion.appendChild(valor)
                    references.append(k.reference)
                    
                if counter == len(self.bills):
                        referencia_duplicada = document.createElement("REFERENCIA_DUPLICADA")
                        referencia_duplicada.appendChild(document.createTextNode(str(references.count(duplicate_reference))))
                        errores.appendChild(referencia_duplicada)
                    
                    # print(k.reference)
                    # print(k.sender_nit)
                    # print(k.receiver_nit)
                    # print(k.value)
                    # print(k.iva)
                    # print(k.total)
            references =  []
        xml_str = root.toprettyxml(indent="\t")
        save_path_file= "../frontend/web/autorizaciones.xml"
        
        with open(save_path_file, "w") as f:
            f.write(xml_str)
    
    def reset_authorization(self):
        self.bills.clear()
        xml_str = "<LISTAAUTORIZACIONES> </LISTAAUTORIZACIONES>"
                
        save_path_file= "../frontend/web/autorizaciones.xml"
        with open(save_path_file, "w") as f:
            f.write(xml_str)
        
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