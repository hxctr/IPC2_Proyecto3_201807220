from django.shortcuts import render
from .forms import FileForm
import requests
from xml.etree import ElementTree as ET
# Create your views here.

endpoint = 'http://127.0.0.1:5000/'
def home(request):
    response = requests.get(endpoint + 'showall')
    bills = response.json()
    context = {
        'bills': bills
    }
    return render(request, 'index.html', context)

def add(request):
    pass

def massive_load(request):
    ctx = {
        'content': None,
        'response': None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            # print(request.FILES )
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + 'add', data=xml_binary)
            second_response = requests.get(endpoint + 'send')
            if response.ok:
                tree = ET.parse('C:/Users/hctr/Documents/IPC2_Proyecto3_201807220/frontend/web/autorizaciones.xml')
                tree = tree.getroot()
                xml_response = ET.tostring(tree, encoding='unicode', method='xml')
                
                # print(xml_response)
                ctx['response'] = xml_response
    else:
        return render(request, 'massive.html')
    return render(request, 'massive.html', ctx)

def reset_load(request):
    ctx = {
        'content': None,
        'response': None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            # print(request.FILES )
            ctx['content'] = ''
            second_response = requests.get(endpoint + 'reset')
            if second_response.ok:
                # print(xml_response)
                second_response = requests.get(endpoint + 'reset')
                ctx['response'] = ''
    else:
        return render(request, 'massive.html')
    return render(request, 'massive.html', ctx)