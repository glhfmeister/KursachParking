from django.shortcuts import render
from django.views import View
from .models import *
from .basa import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from datetime import datetime
from datetime import timedelta

# Create your views here.
class First_Page(View):
    def get(self, request):
        orders1 = Orders.objects.all()
        context = {
            "orders1": orders1
        }
        return render(request, 'index.html', context=context)

class MainPage(View):
    def get(self, request):
        mail = request.session.get("usero_mailo")
        adm = request.session.get("admin")

        if (adm):
            adm = 'True'
        else:
            adm = 'False'

        print(adm)
        print(mail)

        context = {
            'mail_user':mail,
            'admin': adm
        }
        return render(request, 'main.html', context=context)

class Register(View):
    def get(self, request):
        context = {}
        return render(request, 'registr.html', context=context)
    def post(self, request):
        context = {}
        mail = request.POST.get("email")
        phone = request.POST.get("phone_num")
        password = request.POST.get("passw")
        print(mail)
        print(phone)
        print(password)
        if not mail:
            context["error_message"] = "Вы не ввели почту"
            return render(request, 'registr.html', context=context)
        elif not phone:
            context["error_message"] = "Вы не ввели номер телефона"
            return render(request, 'registr.html', context=context)
        elif len(phone) != 11:
            context["error_message"] = "Вы не верно ввели номер телефона"
            return render(request, 'registr.html', context=context)
        elif not password:
            context["error_message"] = "Вы не ввели пароль"
            return render(request, 'registr.html', context=context)
        else:
            if check_mailo_exist(mail) == 1 and check_phone_exist(phone) == 1:
                add_user(mail, phone, password)
                return HttpResponseRedirect("/enter")
            else:
                context["error_message"] = "Телефон или почта уже используется"
                return render(request, 'registr.html', context=context)

class Enter(View):
    def get(self, request):
        context = {}
        return render(request, 'enter.html', context=context)
    def post(self, request):
        context = {}
        entered_mail = request.POST.get("Enter_mail")
        entered_pass = request.POST.get("Enter_pass")
        check_admin = Admins.objects.filter(adm_nick=entered_mail, adm_passw=entered_pass)
        print(len(check_admin))
        user_login = Usero.objects.filter(mailo=entered_mail, passwordo=entered_pass)

        if len(check_admin) != 0:
            request.session['usero_pk'] = check_admin[0].pk
            request.session['usero_mailo'] = check_admin[0].adm_nick
            print(check_admin[0].adm_nick)
            request.session['user'] = check_admin[0].adm_nick
            request.session['admin'] = "True"
            print(request.session['admin'])
            return HttpResponseRedirect("main")

        elif len(user_login) == 0:
            context["error_message"] = "Вы ввели неверные данные"
            return render(request, 'enter.html', context=context)


        else:
            request.session['usero_pk'] = user_login[0].pk
            print(user_login[0].pk)
            request.session['usero_mailo'] = user_login[0].mailo
            print(user_login[0].mailo)
            request.session['user'] = user_login[0].mailo
            return HttpResponseRedirect("main")

class Person_pg(View):
    def get(self, request):
        usero_id = request.session.get("usero_pk")
        mail = request.session.get("usero_mailo")
        adm = request.session.get("admin")

        ord = Orders.objects.filter(usero_idusero=usero_id)
        try:

            d1 = ord[0].timeStart
            print (d1)
            d2 = datetime.now()
            d2 = d2.strftime(("%d.%m.%Y %H:%M:%S"))
            print (d2)
        except:
            print("it's admin")
        #d3 = d2 - d1
        #print(d3)



        ord = check_user_in_order(ord)
        print (ord)


        context = {
            'usero_pk': usero_id,
            'mail_user': mail,
            'admin': adm,
            "ord": ord,
        }
        return render(request, 'person_page.html', context=context)
    def post(self, request):
        context = {}
        if request.method == "POST" and 'stop_arend' in request.POST:
            usero_id = request.session.get("usero_pk")
            return HttpResponseRedirect("../payed")

        else:
            try:
                request.session.pop("usero_mailo")
                request.session.pop("usero_pk")
                request.session.pop("user")
                request.session.pop("admin")
            except:
                print("don't can")
            print(request.session.get("user"))
            return HttpResponseRedirect("../main")

class Adm(View):
    def get(self, request):
        mail = request.session.get("usero_mailo")

        print(mail)
        print (request.path)

        cityes = City.objects.all()
        addreses = Street.objects.all()

        context = {
            "cityes": cityes,
            "addreses": addreses,
            'mail_user': mail,
            "admin": request.session.get("admin")
        }
        return render(request, 'adm.html', context=context)
    def post(self, request):
        if request.method == "POST" and 'city' in request.POST:
            context = {
                "cityes": City.objects.all(),
                "addreses": Street.objects.all(),
                'mail_user': request.session.get("usero_mailo"),
                "admin": request.session.get("admin")
            }
            entered_city = request.POST.get("city")
            if not entered_city:
                context["err2"] = "Вы не ввели город"
                return render(request, 'adm.html', context=context)
            entered_addr = request.POST.get("address")
            if not entered_addr:
                context["err2"] = "Вы не ввели адрес"
                return render(request, 'adm.html', context=context)
            entered_quan = request.POST.get("quanity")
            if not entered_quan:
                context["err2"] = "Вы не ввели количество мест"
                return render(request, 'adm.html', context=context)
            if int(entered_quan) < 1:
                context["err2"] = "Rоличество мест должно быть положительным"
                return render(request, 'adm.html', context=context)
            print(entered_city, entered_addr, entered_quan)
            add_parking(entered_city, entered_addr, entered_quan)
            context = {
                "cityes": City.objects.all(),
                "addreses": Street.objects.all(),
                'mail_user': request.session.get("usero_mailo"),
                'admin': request.session.get("admin")
            }
            return render(request, 'adm.html', context=context)

        if request.method == "POST" and 'price' in request.POST:
            context = {
                "cityes": City.objects.all(),
                "addreses": Street.objects.all(),
                'mail_user': request.session.get("usero_mailo"),
                "admin": request.session.get("admin")
            }
            newPrice = request.POST.get("price")
            if not newPrice:
                context["err1"] = "Вы не ввели цену"
                return render(request, 'adm.html', context=context)
            try:
                print(int(newPrice) + 5)
                if int(newPrice) < 0:
                    context["err1"] = "Цена должна быть положительной"
                    return render(request, 'adm.html', context=context)

                oldPrice = priceo.objects.all()[0]
                oldPrice.price = newPrice
                oldPrice.save()
                context = {
                    "cityes": City.objects.all(),
                    "addreses": Street.objects.all(),
                    'mail_user': request.session.get("usero_mailo"),
                    'admin': request.session.get("admin")
                }
                return render(request, 'adm.html', context=context)

            except:
                context["err1"] = "Ценой должно быть число"
                return render(request, 'adm.html', context=context)


class Del_park(View):
    def get(self, request, id):
        mail = request.session.get("usero_mailo")

        context = {
            'mail_user': mail
        }
        return render(request, 'del_park.html', context=context)
    def post(self, request, id):
        Del_quan = Parking.objects.filter(Street_id=id)
        Del_quan.delete()
        Del_p = Street.objects.filter(pk=id)
        id_c = Del_p[0].city_id.id
        print(id_c)
        check_city = Street.objects.filter(city_id=id_c)
        print(check_city)
        Del_p.delete()
        if len(check_city) == 0:
            print("Here")
            ci = City.objects.filter(pk=id_c)
            print(ci)
            ci.delete()

        context = {
            "cityes": City.objects.all(),
            "addreses": Street.objects.all(),
            'mail_user': request.session.get("usero_mailo"),
            'admin': request.session.get("admin")
        }

        return HttpResponseRedirect("../adm")

class Choice_ad(View):
    def get(self, request):
        mail = request.session.get("usero_mailo")

        print(mail)

        context = {
            "cityes": City.objects.all(),
            "addreses": Street.objects.all(),
            'mail_user': request.session.get("usero_mailo"),
            'admin': request.session.get("admin")
        }
        return render(request, 'choice_address.html', context=context)

    def post(self, request):
        print(request.session.get("usero_mailo"))
        context = {
            'mail_user': request.session.get("usero_mailo"),
            'admin': request.session.get("admin")
        }
        return render(request, 'choice_place.html', context=context)

class Choice_pl(View):
    def get(self, request, id):
        quan = Parking.objects.filter(Street_id=id)[0].quanityPlaces
        request.session['id_park'] = Parking.objects.filter(Street_id=id)[0].pk
        ord = Orders.objects.filter(Parking_id=request.session.get('id_park'))
        mainArr = []
        for i in range (quan):
            if (Orders.objects.filter(Parking_id=request.session.get('id_park'), occupiedPlace=i+1)):
                mainArr.append((i+1)/1000)
            else:
                mainArr.append(i + 1)
        print (mainArr)

        context = {
            "price": priceo.objects.all(),
            'mail_user': request.session.get("usero_mailo"),
            'admin': request.session.get("admin"),
            'places': mainArr,
            'ord': ord,
        }
        return render(request, 'choice_place.html', context=context)

class Arend_p(View):
    def get(self, request, id):
        check_ord = Orders.objects.filter(usero_idusero=accept_obj_user(request.session.get("usero_mailo")))
        if len(check_ord) != 0:
            context = {
                "price": priceo.objects.all(),
                'mail_user': request.session.get("usero_mailo"),
                'admin': request.session.get("admin"),
                'alr_occup': 'True',
            }
        else:
            context = {
                "price": priceo.objects.all(),
                'mail_user': request.session.get("usero_mailo"),
                'admin': request.session.get("admin"),
                'alr_occup': 'False',
            }
        return render(request, 'arend_place.html', context=context)
    def post(self,request, id):
        context={}
        print (request.session.get("id_park"))
        time = datetime.now()

        add_order(id, request.session.get("usero_mailo"), request.session.get("id_park"), time)
        return HttpResponseRedirect("../person_page")

class End_a(View):
    def post(self, request):
        mail = request.session.get("usero_mailo")
        context = {
            'mail_user': mail,
        }
        return render(request, 'payed.html', context=context)
class Pay(View):
    def get(self, request):
        pk_us = Usero.objects.filter(mailo=request.session.get("usero_mailo"))[0].pk
        price = pric(pk_us)
        print(price)

        context = {
            "price": price
        }
        return render(request, 'payed.html', context=context)
    def post(self, request):
        context = {}
        entered_num_card = request.POST.get("num")
        entered_year = request.POST.get("year")
        entered_cvc = request.POST.get("cvc")

        if (not entered_num_card) or (not entered_year) or (not entered_cvc):
            pk_us = Usero.objects.filter(mailo=request.session.get("usero_mailo"))[0].pk
            price = pric(pk_us)
            context["err"] = "Одно или несколько полей незаполненно"
            context["price"] = price
            return render(request, 'payed.html', context=context)
        if len(entered_num_card) == 12 and int(entered_num_card) > 0 and len(entered_year) == 4 and int(entered_year) > 0 and len(entered_cvc) == 3 and int(entered_cvc) > 0:
            pk_us = Usero.objects.filter(mailo=request.session.get("usero_mailo"))[0].pk
            Orders.objects.filter(usero_idusero=pk_us).delete()
            return HttpResponseRedirect("../main")
        else:
            pk_us = Usero.objects.filter(mailo=request.session.get("usero_mailo"))[0].pk
            price = pric(pk_us)
            context["err"] = "Введены несуществующие данные карты"
            context["price"] = price
            return render(request, 'payed.html', context=context)
