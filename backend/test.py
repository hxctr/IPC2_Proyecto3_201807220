import re
import random
# text = "Number is  23.1234"

# def nume(text):
#     result = re.search(r"\b\d{1,3}\.\d{4}\b", text)
#     if result:
#         return result.group()
#     else:
#         return None

# print(nume(text))

#-----------------------------------------------------------------------------------------------
number_random = random.randint(450000, 1000000)
text = str(number_random)
v_digit = int(text[-1])
number = str(text[:-1])

suma = 0
length = len(number) +1
for i in number:
    
    suma += int(i) * length
    length -= 1

mod_operation = suma % 11

minus_operation = 11 - mod_operation

k = minus_operation % 11

if (k < 10) and (k == v_digit):
    
    print("yes, nit is valide", number_random)
else:
    print("no, nit is valide", number_random)
#------------------------------------------------------------------------------------
# text = "Number is  23.12345"
# result = re.search(r"\b\d{1,3}\.\d{4}\b", text)
# print(result.group())