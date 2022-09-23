
import pyqrcode
from pyqrcode import QRCode
import png
import tabula
import datetime
import csv
from re import I
from django.http import HttpResponse
from django.db import connection
from django.utils import timezone


from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import os
from django.conf import settings

from .models import Donor

import random
import string
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


import pyqrcode
import png
from pyqrcode import QRCode

from num2words import num2words
# Create your views here.

if User.objects.filter(username='user_1').exists():
    pass
else:
    user = User.objects.create_user(
        username='user_1', password='abc', email='123@mail.com', first_name='user', last_name='1')
    user.save()


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                print('super')
            else:
                print('normal')
            return redirect("/")
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'Login.html')


def index(request):
    if request.method == 'POST':
        print('posted')
        name = request.POST['Name']
        amount = request.POST['Amount']
        phone = request.POST['Phone']
        cheque = request.POST['Cheque']
        fyear = request.POST['financial_year']
        onaccof = request.POST['on_acc_of']
        email = request.POST['email']
        remarks = request.POST['Remarks']
        country = request.POST['Country']
        type = request.POST['Type']
        typeMap = {'Credit': 'CR', 'Debit': 'DB'}
        token = ''.join(random.choices(
            string.ascii_letters+string.digits, k=7))

        Donor.objects.create(Date='2024-01-01', Financial_Year=fyear, Type=typeMap[type], Amount=amount,
                             Cheque_Number=cheque, From_To=name, Name='Mr. '+name, On_Account_Of=onaccof, Country=country, Remarks=remarks, Email=email, Phone_Number=phone, Status='RU', Action=True, Token=token)
        return redirect("/")
    donor_list = Donor.objects.order_by('id')
    return render(request, 'Index.html', {'donors': donor_list})


def logout(request):
    auth.logout(request)
    return redirect('login')


def delete_instance(request, id_=None):
    # if request.method == 'POST':
    print(id_)
    Donor.objects.get(id=id_).delete()
    return redirect("/")


def duplicate(request, date=None, fyear=None, type=None, amount=None, cheque=None, namenew=None, name=None, onaccof=None, country=None, remarks=None, email=None, phone=None):
    print(date)
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
              "Jul": '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    if len(date) == 13:
        year = date[9:]
        day = date[5:7]
    elif len(date) == 12:
        year = date[8:]
        day = '0'+date[5]
    month = months[date[:3]]
    amount = float(amount)
    formatted_date = year+'-'+month+'-'+day
    token = ''.join(random.choices(string.ascii_letters+string.digits, k=7))
    Donor.objects.create(Date=formatted_date, Financial_Year=fyear, Type=type, Amount=amount, Cheque_Number=cheque, name=namenew, From_To=name,
                         On_Account_Of=onaccof, Country=country, Remarks=remarks, Email=email, Phone_Number=phone, Status='RU', Action=True, Token=token)
    return redirect("/")

# def csv_generate(qs):
#     filename='new.csv'
#     # open(filename, 'w')

#     sql, params = qs.query.sql_with_params()
#     sql = f"COPY ({sql}) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER E'\t')"
#     filename = f'{filename}-{timezone.now():%Y-%m-%d_%H-%M-%S}.csv'
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = f'attachment; filename={filename}'
#     with connection.cursor() as cur:
#         sql = cur.mogrify(sql, params)
#         cur.copy_expert(sql, response)
#     return response

# from django.db.models import F

# from django.db.models import Case, When, Value, CharField
# def map_choices(field_name, choices):
#     return Case(
#         *[When(**{field_name: value, 'then': Value(str(representation))})
#           for value, representation in choices],
#         output_field=CharField()
#     )

# Place.objects.values(
#   'id',
#   'name',
#   verbose_type=map_choices('place_type', Place.PLACE_TYPE_CHOICES),
#   city_name=F('city__name')
# )


# def export_csv(self):
#     id = '1'
#     filename = f'{settings.BASE_DIR}-{timezone.now():%Y-%m-%d_%H-%M-%S}.csv'
#     with connection.cursor() as cursor:
#         cursor.execute(
#             "copy (SELECT * FROM main_donor WHERE id=%s)  TO %s DELIMITER ',' CSV HEADER;", [id, filename])

#     return redirect('/')


def export_csv(request):
    filenaam = f'Donors-{timezone.now():%Y-%m-%d_%H-%M-%S}.csv'
    # .get() for only one value
    # .filter
    donors = Donor.objects.filter(Date__gte=datetime.date.today())
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = f'attachment; filename={filenaam}'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Date', 'Financial Year', 'Type', 'Amount', 'Cheque Number', 'From/To',
                    'On Account Of', 'Country', 'Reamrks', 'Email', 'Phone Number', 'Status', 'Action'])
    writer.writerows(donors.values_list())
    return response


def is_date(date):
    if len(date) >= 10:
        date = date[:10]
        day = date[:2]
        slash1 = date[2]
        month = date[3:5]
        slash2 = date[5]
        year = date[6:]

        isdate = False
        if day.isdigit() and len(day) == 2 and slash1 == '/' and month.isdigit() and len(month) == 2 and slash2 == '/' and len(year) == 4 and year.isdigit():
            isdate = True
        return isdate
    return False


def date_format(date):
    day = date[:2]
    month = date[3:5]
    year = date[6:]
    datee = year+'-' + month + '-' + day
    return datee


def amount_extract(amount):
    new_amt = ''
    for i in amount:
        if i == ',':
            pass
        else:
            new_amt += i
    # print(new_amt)
    return float(new_amt)


def pdf_extractor(request):
    if request.method == 'POST':
        filename = request.FILES['myfile']

    test_area = [180.0, 10.0, 900.0, 800.0]
    csv_file = f"db_{timezone.now():%Y-%m-%d_%H-%M-%S}.csv"
    tabula.convert_into(filename, csv_file,
                        output_format="csv", pages='all', area=test_area)

    file = open(csv_file, 'r+')
    rows = file.readlines()
    to_del = []
    last = None
    for k in range(len(rows)):
        if 'DATE,VALUE,INSTRUMENT/,DETAILS,DEBIT,CREDIT,BALANCE' in rows[k] or 'DATE,DOC NO.' in rows[k] or 'Opening Balance' in rows[k]:
            to_del.append(k)
        elif 'Closing Balance' in rows[k]:
            last = k-len(to_del)
        else:
            rows[k] = rows[k].strip('\n').split('"')
    for e in to_del[::-1]:
        del rows[e]

    del rows[last:]

    temp = []
    final = []
    for i in range(len(rows)):
        if is_date(rows[i][0]):
            final.append(temp)
            temp = []
            temp.append(rows[i][0][:10])
            if len(rows[i]) < 6:
                try:
                    temp.append(rows[i][2]) if rows[i][2].isdigit(
                    ) else temp.append(rows[i][3])
                except IndexError:
                    print(rows[i], i)
                    temp.append('000')
                    messages.info(
                        request, 'There was an error reading the following. Please edit and update it manually  '+" ".join(rows))
                # temp.append(rows[i][2]) if rows[i][2].isdigit() else temp.append(rows[i][3])
            else:
                temp.append(rows[i][3])
            if rows[i][2] == ',,':
                temp.append('Credit')
            else:
                temp.append('Debit')
            temp.append(rows[i][1])
        else:
            if len(rows[i]) > 3:
                temp.append(rows[i][3])
            elif len(rows[i]) > 2:
                temp.append(rows[i][2])
    final.append(temp)

    final = final[1:]

    final_pakka = []
    for i in range(len(final)):
        temp = []
        temp = final[i][:3]
        temp.append(final[i][0][6:])
        name, acc = '', ''
        for k in range(3, len(final[i])-1):
            name += final[i][k]
        acc = final[i][-1]
        temp.append(name)
        temp.append(acc)
        final_pakka.append(temp)

    for i in range(len(final_pakka)):
        date = date_format(final_pakka[i][0])
        amount = amount_extract(final_pakka[i][1])
        type = final_pakka[i][2]
        fyear = int(final_pakka[i][3])
        name = final_pakka[i][4][:150]
        onaccof = final_pakka[i][5]
        typeMap = {'Credit': 'CR', 'Debit': 'DB'}
        token = ''.join(random.choices(
            string.ascii_letters+string.digits, k=7))

        Donor.objects.create(Date=date, Financial_Year=fyear, Type=typeMap[type], Amount=amount,
                             Cheque_Number=00000, From_To=name, Name='Mr. ', On_Account_Of=onaccof, Country='unknown', Remarks='No Remarks', Email='example@ex.com', Phone_Number=0000, Status='RU', Action=True, Token=token)

    return redirect('/')


def qrcode(hash, id):
    # String which represents the QR code
    s = "http://127.0.0.1:8000/records/"+hash+'/'
    # Generate QR code
    url = pyqrcode.create(s)
    # Create and save the png file naming "myqr.png"
    url.png(f'qrcodes/qr_{id}_{hash}.png', scale=3)


def receipt(request, pk=None, date=None, amount=None):

    D = Donor.objects.get(id=pk)

    rec_id = D.Token
    name = D.From_To
    onaccof = D.On_Account_Of

    hash = D.get_hashid()
    id = pk*2

    qrcode(hash, pk)
    # name = 'Mr Steven Jonathan Eleven Jani s/o Jim Hopper Joyce and all other casts including Nancy'
    # date = '01/01/2024'
    receipt_no = rec_id[:4] + str(id) + rec_id[4:]
    filenaam = 'Receipt_'+receipt_no+'.pdf'
    # onaccof = 'Steve Harrington'
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(55, 87, amount+'/-')  # amount
    if len(name) > 70:
        for i in range(70, -1, -1):
            if name[i] == ' ':
                index = i
                break
            else:
                index = 70
        can.drawString(170, 240, name[:index])
        can.drawString(43, 213, name[index+1:])
    else:
        can.drawString(170, 240, name)  # name
    can.drawImage(f'qrcodes/qr_{pk}_{hash}.png', 385, 30, width=60,
                  preserveAspectRatio=True, mask='auto')
    can.drawString(96, 186, num2words(
        int(float(amount)))+' only')  # amount again
    can.drawString(105, 133, onaccof)  # onaccof
    can.drawString(425, 290, date)  # date
    can.drawString(425, 266, receipt_no)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("1.pdf", "rb"))
    output = PdfFileWriter()
    # add the entry info (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    response = HttpResponse('text/pdf')
    response['Content-Disposition'] = f'attachment; filename={filenaam}'
    # outputStream = open(response, "wb")
    output.write(response)

    D.Status = 'RG'
    D.save()

    return response
    # Adress the issue of built on forward slash in the query which increases teh input fields in some cases of sownlaoding receipts and url for the link becomes unavailable.


def records(request, pk):
    J = Donor.objects.get(id=pk)
    return render(request, 'rec.html', {'reco': J})
    # need to add hash in url or add a slug feild in database and then search by slug field not id.
