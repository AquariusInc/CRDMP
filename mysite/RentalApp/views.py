from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
from .models import Store, Customer, Car, Order
from django.db.models import Count
import json
import datetime
from datetime import date, datetime
import re

from .helperfuncs.helperfuncs import chartJSData, chartJSData_bracket, chartJSData_bracket_dt_yr
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .models import MyUser


# Create your views here.
# from django.core import serializers

def home(request):
    return render(request, 'home.html')
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # replace this with success message
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # return redirect('home')
            #
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def customers_table(request):
    if request.GET.get('search_field'):
        field = request.GET['search_field']
        query = request.GET['search_box']

        if field == "name":
            data = Customer.objects.filter(name__contains=query)
        elif field == "id":
            data = Customer.objects.filter(id__contains=query)
        elif field == "address":
            data = Customer.objects.filter(address__contains=query)
        elif field == "phone":
            data = Customer.objects.filter(phone__contains=query)
        elif field == "gender":
            data = Customer.objects.filter(gender__contains=query)
        elif field == "occupation":
            data = Customer.objects.filter(occupation__contains=query)


        paginator = Paginator(data, 25)  # Show 25 contacts per page
        page = request.GET.get('page')
        customers = paginator.get_page(page)

        return render(request, 'customers_table.html', {'data': customers, 'query': query, 'field': field})


    data = Customer.objects.all()

    paginator = Paginator(data, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    customers = paginator.get_page(page)

    return render(request, 'customers_table.html', {'data': customers})


@csrf_exempt
def rental_table(request):
    if request.GET.get('start_date') and request.GET.get('search_field'):
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        start_date_datetime = datetime.strptime(start_date, '%b %d, %Y')
        end_date_datetime = datetime.strptime(end_date, '%b %d, %Y')

        field = request.GET.get('search_field')
        query = request.GET.get('search_box')

        if field == "id":
            data = Order.objects.filter(id__contains=query, createDate__gte=start_date_datetime, createDate__lte=end_date_datetime)
        elif field == "car_id":
            data = Order.objects.filter(car__id__contains=query, createDate__gte=start_date_datetime, createDate__lte=end_date_datetime)
        elif field == "customer_id":
            data = Order.objects.filter(customer__id__contains=query, createDate__gte=start_date_datetime, createDate__lte=end_date_datetime)
        elif field == "pickup_id":
            data = Order.objects.filter(pickupStore__id__contains=query, createDate__gte=start_date_datetime, createDate__lte=end_date_datetime)
        elif field == "return_id":
            data = Order.objects.filter(returnStore__id__contains=query, createDate__gte=start_date_datetime, createDate__lte=end_date_datetime)

        paginator = Paginator(data, 25)  # Show 25 contacts per page
        page = request.GET.get('page')
        orders = paginator.get_page(page)

        return render(request, 'rental_table.html', {'orders': orders, 'query': query, 'field': field})

    if request.GET.get('start_date'):
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']

        start_date_datetime = datetime.strptime(start_date, '%b %d, %Y')
        end_date_datetime = datetime.strptime(end_date, '%b %d, %Y')

        data = Order.objects.filter(createDate__gte=start_date_datetime, createDate__lte=end_date_datetime)

        paginator = Paginator(data, 25)  # Show 25 contacts per page
        page = request.GET.get('page')
        orders = paginator.get_page(page)

        return render(request, 'rental_table.html', {'orders': orders})

    if request.GET.get('search_field'):
        field = request.GET.get('search_field')
        query = request.GET.get('search_box')

        if field == "id":
            data = Order.objects.filter(id__contains=query)
        elif field == "car_id":
            data = Order.objects.filter(car__id__contains=query)
        elif field == "customer_id":
            data = Order.objects.filter(customer__id__contains=query)
        elif field == "pickup_id":
            data = Order.objects.filter(pickupStore__id__contains=query)
        elif field == "return_id":
            data = Order.objects.filter(returnStore__id__contains=query)

        paginator = Paginator(data, 25)  # Show 25 contacts per page
        page = request.GET.get('page')
        orders = paginator.get_page(page)

        return render(request, 'rental_table.html', {'orders': orders, 'query': query, 'field': field})

    data = Order.objects.all()

    paginator = Paginator(data, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    orders = paginator.get_page(page)

    return render(request, 'rental_table.html', {'orders': orders})


def customer_data(request):
    data = Customer.objects.all()
    order = Order.objects.all()
	
	# Occupation counts - done
    occupationSQL = data.values('occupation').annotate(total=Count('occupation')).order_by('-total')
    occupation = chartJSData(occupationSQL, 'occupation')
	
	# Gender counts - done
    genderSQL = data.values ('gender').annotate(total=Count('gender')).order_by('-total')
    gender = chartJSData(genderSQL, 'gender')
    
    #repeat customers - done
    customerSQL = order.values ('customer').annotate(total=Count('customer')).order_by('total')
    customer = chartJSData(customerSQL, 'customer', chartType="line")
       
	
	#Customer counts
    idSQL = data.values ('id').annotate(total=Count('id'))
    id = chartJSData(idSQL, 'id', chartType="line")
	
	# Age Counts
    dob_data = chartJSData_bracket_dt_yr(data, 'dob', start_date=date(1930,1,1), increment=10, bracketCount=6)
   
    #customer counter over time - temp 
    orderSQl = chartJSData_bracket_dt_yr(order, 'createDate', start_date=date(2000,1,1), increment=1, bracketCount=10)
    #poo = chartJSData(orderSQL, 'createDate', chartType="line")
 
    # holding dict
    js_dict = {
            'occupation': occupation,
            'gender': gender,
			'id':id,
            'dob': dob_data,
            'customer':customer,
            'createDate':orderSQl
    }
    # Serialize dict into json to use in HTML file
    js_data = json.dumps(js_dict)
	
    return render(request, 'visualise_customer_data.html', {'js_data': js_data})
	
	

def rental_data(request):

    data = Customer.objects.all()
    order = Order.objects.all()
    store = Store.objects.all()
    car = Car.objects.all()

    returnStoreSQL = order.values('returnStore').annotate(total=Count('returnStore')).order_by('-total')
    returnStore = chartJSData(returnStoreSQL, 'pickupStore__name',maxLabels = 15)

    pickupStoreSQL = order.values('pickupStore').annotate(total=Count('pickupStore')).order_by('-total')
    pickupStore = chartJSData(pickupStoreSQL, 'pickupStore__name', maxLabels = 15)

    bodyTypeSQL = car.values('bodyType').annotate(total=Count('bodyType')).order_by('-total')
    bodyType = chartJSData(bodyTypeSQL, 'bodyType', maxLabels=15)

    # totalCountSQL = order.values('id').annotate(total=Count('id')).order_by('-total')
    # totalCount = chartJSData(totalCountSQL, 'pickupStore__name', maxLabels=15)

    js_dict = {
        'returnStore': returnStore,
        'pickupStore': pickupStore,
        'bodyType' : bodyType
    }
    js_data = json.dumps(js_dict)
    return render(request, 'visualise_rental_data.html', {'js_data': js_data})
    # #occupation = chartJSData(occupationSQL, 'occupation')
    # pie3d = FusionCharts("pie3d","ex2", "100%", "400", "chart-1", "json",
    #     # The data is passed as a string in the `dataSource` as parameter.
    # """{
    #     "chart": {
    #         "caption": "Rental Returns",
    #
    #         "showValues":"1",
    #         "showPercentInTooltip" : "0",
    #         "numberPrefix" : "%",
    #         "enableMultiSlicing":"1",
    #         "theme": "fusion"
    #     },
    #     "data": [{
    #         "label": "Equity",
    #         "value": "300000"
    #     }, {
    #         "label": "Debt",
    #         "value": "230000"
    #     }, {
    #         "label": "Bullion",
    #         "value": "180000"
    #     }, {
    #         "label": "Real-estate",
    #         "value": "270000"
    #     }, {
    #         "label": "Insurance",
    #         "value": "20000"
    #     }]
    # }""")
    # return render(request, 'visualise_rental_data.html', {'output': pie3d.render(), 'chartTitle': 'Returns Data Visualization'})



def vehicle_data(request):
    data = Car.objects.all()

    # Bodytypes counts
    bodytypesSQL = data.values('bodyType').annotate(total=Count('bodyType')).order_by('-total')
    bodyTypes = chartJSData(bodytypesSQL, 'bodyType')

    # Make counts
    makeSQL = data.values('make').annotate(total=Count('make')).order_by('-total')
    make = chartJSData(makeSQL, 'make')

    # Model counts
    modelSQL = data.values('model').annotate(total=Count('model')).order_by('-total')
    model = chartJSData(modelSQL, 'model', maxLabels=20)

    # Year Bracket counts
    year = chartJSData_bracket(data, 'year', start=1950, increment=10, bracketCount=10)

    # Price Bracket counts
    price = chartJSData_bracket(data, 'priceNew', increment=10000, bracketCount=25)

    # Seating counts
    seatingSQL = data.values('seatingCapacity').annotate(total=Count('seatingCapacity')).order_by('-total')
    seating = chartJSData(seatingSQL, 'seatingCapacity')

    # DriveTrain counts
    driveTrainSQL = data.values('standardTransmission').annotate(total=Count('standardTransmission')).order_by('-total')
    driveTrain = chartJSData(driveTrainSQL, 'standardTransmission', maxLabels=20)

    # holding dict
    js_dict = {
        'bodyTypes': bodyTypes,
        'make': make,
        'model': model,
        'year': year,
        'price': price,
        'seating': seating,
        'driveTrain': driveTrain
    }
    # Serialize dict into json to use in HTML file
    js_data = json.dumps(js_dict)

    return render(request, 'visualise_vehicle_data.html', {'js_data': js_data})


def read_store_data(request):
    with open('/Users/aidan/Desktop/data_in_store.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in reader:
            if row[0] == 'Store_ID':
                continue

            null_bool = False
            for item in row:
                if item == "NULL":
                    null_bool = True

            if null_bool:
                continue

            new = {}

            # stores

            new['Store_ID'] = int(row[0])
            new['Store_Name'] = row[1].strip()
            new['Store_Address'] = row[2].strip()
            new['Store_Phone'] = row[3].strip()
            new['Store_City'] = row[4].strip()
            new['Store_State_Name'] = row[5].strip()

            # # orders
            #
            new['Order_ID'] = int(row[6])
            new['Order_CreateDate'] = row[7]
            new['Pickup_Or_Return'] = row[8]
            new['Pickup_Or_Return_Date'] = row[9]
            #
            # customers

            new['Customer_ID'] = int(row[10])
            new['Customer_Name'] = row[11].strip()
            new['Customer_Phone'] = re.sub('[*]', '', row[12])
            # new['Customer_Addresss'] = re.sub('["]')
            new['Customer_Brithday'] = row[14].strip()
            new['Customer_Occupation'] = row[15].strip()
            new['Customer_Gender'] = row[16].strip()


            new['Car_ID'] = int(row[17])
            new['Car_MakeName'] = row[18].strip()
            new['Car_Model'] = row[19].strip()
            new['Car_Series'] = row[20].strip()
            new['Car_SeriesYear'] = row[21].strip()
            new['Car_PriceNew'] = float(row[22])
            new['Car_EngineSize'] = float(row[23][:-1])
            new['Car_FuelSystem'] = row[24].strip()
            new['Car_TankCapacity'] = float(row[25][:-1])
            new['Car_Power'] = float(row[26][:-2])
            new['Car_SeatingCapacity'] = float(row[27])
            new['Car_StandardTransmission'] = row[28].strip()
            new['Car_BodyType'] = row[29].strip()
            new['Car_Drive'] = row[30].strip()
            new['Car_Wheelbase'] = float(row[31][:-2])

            if new['Pickup_Or_Return'] == 'Pickup':
                if not Order.objects.filter(id=new['Order_ID']):
                    order = Order()
                    order.id = new['Order_ID']
                    print(order.id)
                    order.createDate = datetime.date(int(new['Order_CreateDate'][0:4]),int(new['Order_CreateDate'][4:6]), int(new['Order_CreateDate'][6:8]))
                    order.pickupDate = datetime.date(int(new['Pickup_Or_Return_Date'][0:4]),int(new['Pickup_Or_Return_Date'][4:6]), int(new['Pickup_Or_Return_Date'][6:8]))
                    order.customer = Customer.objects.get(id=new['Customer_ID'])
                    order.car = Car.objects.get(id=new['Car_ID'])
                    order.pickupStore = Store.objects.get(id=new['Store_ID'])

                    order.save()

            if new['Pickup_Or_Return'] == 'Return':
                if not Order.objects.filter(returnStore=new['Store_ID']):
                    try:
                        order = Order.objects.get(id=new['Order_ID'])

                    except:
                        order = Order()
                        order.id = new['Order_ID']
                        order.car = Car.objects.get(id=new['Car_ID'])
                        order.customer = Customer.objects.get(id=new['Customer_ID'])
                        order.createDate = datetime.date(int(new['Order_CreateDate'][0:4]),
                                                         int(new['Order_CreateDate'][4:6]),
                                                         int(new['Order_CreateDate'][6:8]))

                    print(order.id)

                    order.returnStore = Store.objects.get(id=new['Store_ID'])
                    order.returnDate = datetime.date(int(new['Pickup_Or_Return_Date'][0:4]),int(new['Pickup_Or_Return_Date'][4:6]), int(new['Pickup_Or_Return_Date'][6:8]))

                    order.save()

            # if not Store.objects.filter(id=new['Store_ID']):
            #     store = Store()
            #     store.id = new['Store_ID']
            #     store.name = new['Store_Name']
            #     store.address = new['Store_Address']
            #     store.phone = new['Store_Phone']
            #     store.state = new['Store_State_Name']
            #     store.city = new['Store_City']
            #
            #     store.save()

            # if not Customer.objects.filter(id=new['Customer_ID']):
            #     customer = Customer()
            #     customer.id = new['Customer_ID']
            #
            #     print(customer.id)
            #
            #     customer.name = new['Customer_Name']
            #     customer.phone = new['Customer_Phone']
            #     customer.address = new['Customer_Addresss']
            #     customer.occupation = new['Customer_Occupation']
            #     customer.gender = new['Customer_Gender']
            #
            #     birthday = new['Customer_Brithday'].split('/')
            #
            #     print(birthday)
            #
            #     customer.dob = datetime.datetime(1900+ int(birthday[2]), int(birthday[1]), int(birthday[0]))
            #
            #
            #     customer.save()

            # if not Car.objects.filter(id=new['Car_ID']):
            #     car = Car()
            #     car.id = new['Car_ID']
            #
            #     print(car.id)
            #
            #     car.make = new['Car_MakeName']
            #     car.model = new['Car_Model']
            #     car.series = new['Car_Series']
            #     car.priceNew = new['Car_PriceNew']
            #     car.engineSize = new['Car_EngineSize']
            #     car.fuelSystem = new['Car_FuelSystem']
            #     car.power = new['Car_Power']
            #     car.seatingCapacity = new['Car_SeatingCapacity']
            #     car.standardTransmission = new['Car_StandardTransmission']
            #     car.bodyType = new['Car_BodyType']
            #     car.drive = new['Car_Drive']
            #     car.wheelBase = new['Car_Wheelbase']
            #     car.tankCapacity = new['Car_TankCapacity']
            #     car.year = new['Car_SeriesYear']
            #
            #     car.save()

    return HttpResponse("OK")


def read_central_db(request):
    with open('/Users/aidan/Desktop/data_in_central_db.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in reader:
            if row[0] == 'Order_ID':
                continue

            null_bool = False
            for item in row:
                if item == "NULL":
                    null_bool = True

            if null_bool:
                continue

            new = {}

            # stores

            # new['Store_ID'] = int(row[3])
            # new['Store_Name'] = row[1].strip()
            # new['Store_Address'] = row[2].strip()
            # new['Store_Phone'] = row[3].strip()
            # new['Store_City'] = row[4].strip()
            # new['Store_State_Name'] = row[5].strip()

            # # orders
            #
            new['Order_ID'] = int(row[0])
            new['Order_CreateDate'] = row[1]
            new['Pickup_Or_Return_Date'] = row[9]
            new['Pickup_Date'] = row[2]
            new['Return_Date'] = row[9]
            new['Return_Store'] = row[10]
            #
            # customers

            # new['Customer_ID'] = int(row[16])
            # new['Customer_Name'] = row[11].strip()
            # new['Customer_Phone'] = re.sub('[*]', '', row[12])
            # new['Customer_Addresss'] = re.sub('["]')
            # new['Customer_Brithday'] = row[14].strip()
            # new['Customer_Occupation'] = row[15].strip()
            # new['Customer_Gender'] = row[16].strip()
            #
            #  cars

            # new['Car_ID'] = int(row[23])
            # new['Car_MakeName'] = row[18].strip()
            # new['Car_Model'] = row[19].strip()
            # new['Car_Series'] = row[20].strip()
            # new['Car_SeriesYear'] = row[21].strip()
            # new['Car_PriceNew'] = float(row[22])
            # new['Car_EngineSize'] = float(row[23][:-1])
            # new['Car_FuelSystem'] = row[24].strip()
            # new['Car_TankCapacity'] = float(row[25][:-1])
            # new['Car_Power'] = float(row[26][:-2])
            # new['Car_SeatingCapacity'] = float(row[27])
            # new['Car_StandardTransmission'] = row[28].strip()
            # new['Car_BodyType'] = row[29].strip()
            # new['Car_Drive'] = row[30].strip()
            # new['Car_Wheelbase'] = float(row[31][:-2])

            # if new['Pickup_Or_Return'] == 'Pickup':
            #     if not Order.objects.filter(id=new['Order_ID']):
            #         order = Order()
            #         order.id = new['Order_ID']
            #         print(order.id)
            #         order.createDate = datetime.date(int(new['Order_CreateDate'][0:4]),int(new['Order_CreateDate'][4:6]), int(new['Order_CreateDate'][6:8]))
            #         order.pickupDate = datetime.date(int(new['Pickup_Or_Return_Date'][0:4]),int(new['Pickup_Or_Return_Date'][4:6]), int(new['Pickup_Or_Return_Date'][6:8]))
            #         order.customer = Customer.objects.get(id=new['Customer_ID'])
            #         order.car = Car.objects.get(id=new['Car_ID'])
            #         order.pickupStore = Store.objects.get(id=new['Store_ID'])
            #
            #         order.save()
            #
            # if new['Pickup_Or_Return'] == 'Return':
            #     if not Order.objects.filter(returnStore=new['Store_ID']):
            #         try:
            #             order = Order.objects.get(id=new['Order_ID'])
            #
            #         except:
            #             order = Order()
            #             order.id = new['Order_ID']
            #             order.car = Car.objects.get(id=new['Car_ID'])
            #             order.customer = Customer.objects.get(id=new['Customer_ID'])
            #             order.createDate = datetime.date(int(new['Order_CreateDate'][0:4]),
            #                                              int(new['Order_CreateDate'][4:6]),
            #                                              int(new['Order_CreateDate'][6:8]))
            #
            #         print(order.id)
            #
            #         order.returnStore = Store.objects.get(id=new['Store_ID'])
            #         order.returnDate = datetime.date(int(new['Pickup_Or_Return_Date'][0:4]),int(new['Pickup_Or_Return_Date'][4:6]), int(new['Pickup_Or_Return_Date'][6:8]))
            #
            #         order.save()

            print(new)

            order = Order.objects.get(id=new['Order_ID'])

            count = Order.objects.filter(id=new['Order_ID']).exclude(returnStore__isnull=True).count()

            if count < 1:
                order.returnStore = Store.objects.get(id=new['Return_Store'])
                order.returnDate = datetime.date(int(new['Return_Date'][0:4]),
                                                 int(new['Return_Date'][4:6]),
                                                 int(new['Return_Date'][6:8]))
                order.save()

            # if not Store.objects.filter(id=new['Store_ID']):
            # store = Store()
            # store.id = new['Store_ID']
            # store.name = new['Store_Name']
            # store.address = new['Store_Address']
            # store.phone = new['Store_Phone']
            # store.state = new['Store_State_Name']
            # store.city = new['Store_City']
            #
            # store.save()
            # print('new store')

            # if not Customer.objects.filter(id=new['Customer_ID']):
            # customer = Customer()
            # customer.id = new['Customer_ID']
            #
            # print(customer.id)
            #
            # customer.name = new['Customer_Name']
            # customer.phone = new['Customer_Phone']
            # customer.address = new['Customer_Addresss']
            # customer.occupation = new['Customer_Occupation']
            # customer.gender = new['Customer_Gender']
            #
            # birthday = new['Customer_Brithday'].split('/')
            #
            # print(birthday)
            #
            # customer.dob = datetime.datetime(1900+ int(birthday[2]), int(birthday[1]), int(birthday[0]))
            #
            #
            # customer.save()
            # print('new customer')

            # if not Car.objects.filter(id=new['Car_ID']):
            # car = Car()
            # car.id = new['Car_ID']
            #
            # print(car.id)
            #
            # car.make = new['Car_MakeName']
            # car.model = new['Car_Model']
            # car.series = new['Car_Series']
            # car.priceNew = new['Car_PriceNew']
            # car.engineSize = new['Car_EngineSize']
            # car.fuelSystem = new['Car_FuelSystem']
            # car.power = new['Car_Power']
            # car.seatingCapacity = new['Car_SeatingCapacity']
            # car.standardTransmission = new['Car_StandardTransmission']
            # car.bodyType = new['Car_BodyType']
            # car.drive = new['Car_Drive']
            # car.wheelBase = new['Car_Wheelbase']
            # car.tankCapacity = new['Car_TankCapacity']
            # car.year = new['Car_SeriesYear']
            #
            # car.save()
            # print('new car')

    return HttpResponse("OK")
