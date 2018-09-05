from django.shortcuts import render
from django.http import HttpResponse
import csv
from .models import Store, Customer, Order, Car
import datetime
import re
# Create your views here.


def home(request):
    return render(request, 'home.html')


def customers_table(request):
    return render(request, 'customers_table.html')


def rental_table(request):
    return render(request, 'rental_table.html')


def customer_data(request):
    return render(request, 'visualise_customer_data.html')


def rental_data(request):
    return render(request, 'visualise_rental_data.html')


def vehicle_data(request):
    return render(request, 'visualise_vehicle_data.html')


# def read_store_data(request):
#     with open('/Users/aidan/Desktop/data_in_store.txt', newline='') as csvfile:
#         reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
#         for row in reader:
#             if row[0] == 'Store_ID':
#                 continue
#
#             null_bool = False
#             for item in row:
#                 if item == "NULL":
#                     null_bool = True
#
#             if null_bool:
#                 continue
#
#             new = {}
#
#             # stores
#
#             new['Store_ID'] = int(row[0])
#             # new['Store_Name'] = row[1].strip()
#             # new['Store_Address'] = row[2].strip()
#             # new['Store_Phone'] = row[3].strip()
#             # new['Store_City'] = row[4].strip()
#             # new['Store_State_Name'] = row[5].strip()
#
#
#             # # orders
#             #
#             new['Order_ID'] = int(row[6])
#             new['Order_CreateDate'] = row[7]
#             new['Pickup_Or_Return'] = row[8]
#             new['Pickup_Or_Return_Date'] = row[9]
#             #
#             # customers
#
#             new['Customer_ID'] = int(row[10])
#             # new['Customer_Name'] = row[11].strip()
#             # new['Customer_Phone'] = re.sub('[*]', '', row[12])
#             # new['Customer_Addresss'] = row[13].strip()
#             # new['Customer_Brithday'] = row[14].strip()
#             # new['Customer_Occupation'] = row[15].strip()
#             # new['Customer_Gender'] = row[16].strip()
#             #
#             #  cars
#
#             new['Car_ID'] = int(row[17])
#             # new['Car_MakeName'] = row[18].strip()
#             # new['Car_Model'] = row[19].strip()
#             # new['Car_Series'] = row[20].strip()
#             # new['Car_SeriesYear'] = row[21].strip()
#             # new['Car_PriceNew'] = float(row[22])
#             # new['Car_EngineSize'] = float(row[23][:-1])
#             # new['Car_FuelSystem'] = row[24].strip()
#             # new['Car_TankCapacity'] = float(row[25][:-1])
#             # new['Car_Power'] = float(row[26][:-2])
#             # new['Car_SeatingCapacity'] = float(row[27])
#             # new['Car_StandardTransmission'] = row[28].strip()
#             # new['Car_BodyType'] = row[29].strip()
#             # new['Car_Drive'] = row[30].strip()
#             # new['Car_Wheelbase'] = float(row[31][:-2])
#
#             # if new['Pickup_Or_Return'] == 'Pickup':
#             #     if not Order.objects.filter(id=new['Order_ID']):
#             #         order = Order()
#             #         order.id = new['Order_ID']
#             #         print(order.id)
#             #         order.createDate = datetime.date(int(new['Order_CreateDate'][0:4]),int(new['Order_CreateDate'][4:6]), int(new['Order_CreateDate'][6:8]))
#             #         order.pickupDate = datetime.date(int(new['Pickup_Or_Return_Date'][0:4]),int(new['Pickup_Or_Return_Date'][4:6]), int(new['Pickup_Or_Return_Date'][6:8]))
#             #         order.customer = Customer.objects.get(id=new['Customer_ID'])
#             #         order.car = Car.objects.get(id=new['Car_ID'])
#             #         order.pickupStore = Store.objects.get(id=new['Store_ID'])
#             #
#             #         order.save()
#
#             if new['Pickup_Or_Return'] == 'Return':
#                 if not Order.objects.filter(returnStore=new['Store_ID']):
#                     try:
#                         order = Order.objects.get(id=new['Order_ID'])
#
#                     except:
#                         order = Order()
#                         order.id = new['Order_ID']
#                         order.car = Car.objects.get(id=new['Car_ID'])
#                         order.customer = Customer.objects.get(id=new['Customer_ID'])
#                         order.createDate = datetime.date(int(new['Order_CreateDate'][0:4]),
#                                                          int(new['Order_CreateDate'][4:6]),
#                                                          int(new['Order_CreateDate'][6:8]))
#
#                     print(order.id)
#
#                     order.returnStore = Store.objects.get(id=new['Store_ID'])
#                     order.returnDate = datetime.date(int(new['Pickup_Or_Return_Date'][0:4]),int(new['Pickup_Or_Return_Date'][4:6]), int(new['Pickup_Or_Return_Date'][6:8]))
#
#                     order.save()
#
#             # if not Store.objects.filter(id=new['Store_ID']):
#             #     store = Store()
#             #     store.id = new['Store_ID']
#             #     store.name = new['Store_Name']
#             #     store.address = new['Store_Address']
#             #     store.phone = new['Store_Phone']
#             #     store.state = new['Store_State_Name']
#             #     store.city = new['Store_City']
#             #
#             #     store.save()
#
#             # if not Customer.objects.filter(id=new['Customer_ID']):
#             #     customer = Customer()
#             #     customer.id = new['Customer_ID']
#             #
#             #     print(customer.id)
#             #
#             #     customer.name = new['Customer_Name']
#             #     customer.phone = new['Customer_Phone']
#             #     customer.address = new['Customer_Addresss']
#             #     customer.occupation = new['Customer_Occupation']
#             #     customer.gender = new['Customer_Gender']
#             #
#             #     birthday = new['Customer_Brithday'].split('/')
#             #
#             #     print(birthday)
#             #
#             #     customer.dob = datetime.datetime(1900+ int(birthday[2]), int(birthday[1]), int(birthday[0]))
#             #
#             #
#             #     customer.save()
#
#             # if not Car.objects.filter(id=new['Car_ID']):
#             #     car = Car()
#             #     car.id = new['Car_ID']
#             #
#             #     print(car.id)
#             #
#             #     car.make = new['Car_MakeName']
#             #     car.model = new['Car_Model']
#             #     car.series = new['Car_Series']
#             #     car.priceNew = new['Car_PriceNew']
#             #     car.engineSize = new['Car_EngineSize']
#             #     car.fuelSystem = new['Car_FuelSystem']
#             #     car.power = new['Car_Power']
#             #     car.seatingCapacity = new['Car_SeatingCapacity']
#             #     car.standardTransmission = new['Car_StandardTransmission']
#             #     car.bodyType = new['Car_BodyType']
#             #     car.drive = new['Car_Drive']
#             #     car.wheelBase = new['Car_Wheelbase']
#             #     car.tankCapacity = new['Car_TankCapacity']
#             #     car.year = new['Car_SeriesYear']
#             #
#             #     car.save()
#
#
#
#
#
#     return HttpResponse("OK")
