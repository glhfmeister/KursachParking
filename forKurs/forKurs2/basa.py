from .models import *

def add_user(email, phone, password):
    a_user = Usero(mailo=email,phone=phone,passwordo=password)
    a_user.save()
def check_mailo_exist(email):
    mail = Usero.objects.filter(mailo=email)
    if not mail:
        return 1
    else:
        return 0
def check_phone_exist(phone):
    phone = Usero.objects.filter(phone=phone)
    print(phone)
    if not phone:
        return 1
    else:
        return 0

def checkExistCity(city):

    cityes = City.objects.filter(FullNameCity=city)
    return len(cityes)

def add_parking(city, address, quanity):
    checkExistCity(city)
    if checkExistCity(city) != 0:
        id_city = City.objects.filter(FullNameCity=city)[0]
        a_addr = Street(FullStreet=address, city_id=id_city)
        a_quan = Parking(quanityPlaces=quanity, Street_id=a_addr)
        a_addr.save()
        a_quan.save()
    else:
        a_city = City(FullNameCity=city)
        a_addr = Street(FullStreet=address, city_id=a_city)
        a_quan = Parking(quanityPlaces=quanity, Street_id=a_addr)
        a_city.save()
        a_addr.save()
        a_quan.save()

def add_order(id_place, id_user, id_park, time):
    time = time.strftime(("%d.%m.%Y %H:%M:%S"))
    create_o = Orders(occupiedPlace=id_place, statuso=True, usero_idusero=accept_obj_user(id_user), Parking_id=accept_obj_park(id_park), timeStart=time)
    create_o.save()
    print(accept_obj_user(id_user), accept_obj_park(id_park))

def accept_obj_user(id_us):
    return Usero.objects.filter(mailo=id_us)[0]

def accept_obj_park(id_park):
    return Parking.objects.filter(pk=id_park)[0]

def check_place_on_ord(id_park, place):
    a = accept_obj_park(id_park)
    if (Orders.objects.filter(Parking_id=a, occupiedPlace=place)):
        return True
    else:
        return False

def check_user_in_order(ord):
    if (len(ord) == 0):
        ord = "False"
    else:
        print (ord)
        timeSt = ord[0].timeStart
        print(timeSt)

        ord = ord[0].Parking_id.pk
        ord = Parking.objects.filter(pk=ord)[0].Street_id.pk
        ord = Street.objects.filter(pk=ord)[0]
        address = ord.FullStreet

        ord = ord.city_id.pk
        city = City.objects.filter(pk=ord)[0].FullNameCity

        #print (city, address)
        ord = "Город:" + city + " По адрессу: " + address + " Дата и время начала аренды: " + timeSt
    return ord

def pric(pk_us):
    priceHour = priceo.objects.all()[0].price

    print(priceHour)

    print(pk_us)
    timeStart = Orders.objects.filter(usero_idusero=pk_us)[0].timeStart
    timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    timeStart = timeStart.split(" ")
    daysStart = timeStart[0].split(".")

    dayStart = (int(daysStart[2]) * 365) + (int(daysStart[1]) * 30) + int(daysStart[0])
    minutesStart = (((dayStart * 24) + int(timeStart[1].split(":")[0])) * 60) + int(timeStart[1].split(":")[1])

    timeNow = timeNow.split(" ")
    daysNow = timeNow[0].split("-")

    dayNow = (int(daysNow[0]) * 365) + (int(daysNow[1]) * 30) + int(daysNow[2])
    minutesNow = (((dayNow * 24) + int(timeNow[1].split(":")[0])) * 60) + int(timeNow[1].split(":")[1])

    price = ((minutesNow - minutesStart) // 60 + 1) * priceHour
    return price