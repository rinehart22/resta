from django.contrib.auth.decorators import login_required, permission_required
import random
from email.policy import default
from tokenize import group
from unicodedata import category
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
# Create your views here.
from datetime import datetime, timedelta, time

from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users, unauthenticated_user

from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models import Q

cart = []


@login_required(login_url='login')
def chef_view(request):
    dynamicdata = Chef.objects.all()
    context = {'dynamic': dynamicdata}
    return render(request, 'chef_view.html', context)


def filter_cat(request, id=None):
    categories = Category.objects.all()
    if id == None:
        cat = Products.objects.filter(category=1)
    else:
        cat = Products.objects.filter(category=id)
    return render(request, 'ex.html', {'cat': cat, 'categories': categories})


@login_required(login_url='login')
def add_to_cart(request, id):
    print(id, '!!!!!!!!!!!!!!!!!!!!!!!!!!1111111111111')
    dynamicdata = Products.objects.all()
    if request.user.is_authenticated:
        user = request.user.id
        user_instance = User.objects.get(id=user)
        var = Products.objects.get(pk=id)

        get_category = var.category
        print(get_category)

        get_chef = Chef.objects.filter(
            chef_availability=1, category_name=get_category, ).first()
        print(get_chef, '!!!!!!!!!!!')

        z = var.product_price
        print('pppppppppppppppppppppppppppppppppppppppppppp', z)
        # breakpoint()
        cart = OrderItem.objects.filter(
            product_name=var, user=user_instance, checkout_status='').exists()

        if cart:
            messages.info(request, 'product alreay there in cart')

            redirection = str('/filter_cat/' + str(var.category.id))
            return redirect(redirection)
            # return HttpResponseRedirect(reverse(str('/filter_cat/'+ str(var.category.id))))
        else:
            cart = OrderItem.objects.create(
                product_name=var, user=user_instance, price=var.product_price, prepared_by=get_chef, category_name=get_category, )
            print(cart)
            redirection = str('/filter_cat/' + str(var.category.id))
            return redirect(redirection)

        # return render(request, 'menu.html', context={'dynamic': dynamicdata, 'count': cart})


@login_required(login_url='login')
def cart_list(request):
    if request.user.is_authenticated:
        cart = OrderItem.objects.filter(
            user_id=request.user, checkout_status='')
        today = datetime.now().date()

        if request.method == 'POST':

            add = request.POST.get('add')
            remove = request.POST.get('remove')

            if add:
                var = OrderItem.objects.get(id=add).product_name

                product_cost = Products.objects.get(product_name=var)

                print('++++++++++++++++++', product_cost.product_price)
                product_qty_from_db = OrderItem.objects.get(id=add).quantity
                inc_qty = product_qty_from_db+1
                cart_data = OrderItem.objects.filter(id=add).update(
                    quantity=inc_qty, price=product_cost.product_price*inc_qty)

            elif remove:
                var1 = OrderItem.objects.get(id=remove).product_name
                product_cost1 = Products.objects.get(product_name=var1)
                try:
                    product_qty_from_db = OrderItem.objects.get(
                        id=remove).quantity
                    dc_qty = product_qty_from_db-1
                    cart_data = OrderItem.objects.filter(id=remove).update(
                        quantity=dc_qty, price=product_cost1.product_price*dc_qty)

                except:
                    messages.info(request, 'Please add item to the cart')

            # return render(request, 'cartlist.html', {'d':dy,'cart': cart,})

    dy = OrderItem.objects.filter(
        todayorders__gte=today, user_id=request.user, checkout_status='').aggregate(dy=Sum('price'))
    print(dy)
    context = {'cart': cart, 'd': dy}
    return render(request, 'cartlist.html', context)

    # if cart_data.id <= 0:
    #     cart_data.delete()

    # cart_data.remove[id]
    # if remove == 0:
    # del cart_data
    # if cart_data:
    #     quantity = Cart.objects.filter(items=product)
    #     print(quantity.items)
    #     if quantity:
    #         if remove:
    #             if quantity<=1:
    #                 cart.pop(product)
    #             else:
    #                 cart[product]  = quantity-1
    #         else:
    #             cart[product]  = quantity+1

    #     else:
    #         cart[product] = 1
    # else:
    #     cart = {}
    #     cart[product] = 1
    # for i in cart_items:
    #     cart = Products.objects.filter(product_name=i.items)

    # var = Cart.objects.filter(id__in=[0, -1])

    # cart.append(products)
    # cartitems.append(i)
    # print(cart)
    # for j in cart:
    #     print(j.product_name)
    # print(products)

    # t_id = request.session['category_id']
    # if id:
    #     var = Products.objects.get(id=t_id)
    # else:


@login_required(login_url='login')
def checkout(request):
    # if request.user.is_authenticated:
    #     user = request.user.id
    #     g = Group.objects.get(pk=2)
    #     print(g)

    #     chefname = User.objects.filter(groups=g)
    #     print(chefname, '#############################3')

    #     # for i in chefname:
    #     #     print(i.username,i.id)
    #     chef_one = Chef.objects.get(chef_name=2)
    #     print(chef_one)
    #     get_chef = Chef.objects.filter(
    #         chef_name=chef_one).first()

    #     print(get_chef, '$$$$$$$$$$$$$$$$$$')
    #     cart = OrderItem.objects.filter(user_id=request.user,
    #                                     checkout_status='', prepared_by=get_chef)  # user = request.user.id

    #     print(cart, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    if request.user.is_authenticated:
        cart = OrderItem.objects.filter(
            user_id=request.user, checkout_status='')

        today = datetime.now().date()
        dy = OrderItem.objects.filter(
            todayorders__gte=today, user_id=request.user, checkout_status='').aggregate(dy=Sum('price'))

        print(dy)
        # after checkout clear cart items
        # form = SignupForm()
        if request.method == 'POST':
            # form = SignupForm(request.POST)
            # # print(request.POST)
            # form.username = request.user.id
            # print('------------------------',form)

            if cart:

                users = User.objects.filter(
                    groups__name='chefs').values_list('id', flat=True)

                get_chef = Chef.objects.filter(
                    chef_availability=1,  chef_name=random.choice(users)).first()

                cart.update(checkout_status='completed',
                            prepared_by=get_chef)

            return redirect('/filter_cat')

    return render(request, 'check.html', {'cart': cart, 'd': dy})


# @permission_required('', raise_exception=True)
# @allowed_users(allowed_roles=[ ])
def orders(request):

    if request.user.is_authenticated:
        x = Group.objects.filter(user=request.user)
        print(x, '!__________________________')
        y = []
        for i in x:
            print('--------------------------')
            if i.name == 'Manager':
                print('--------------------------')
                z = i.name
                print(z, '!!!!')
                y.append(z)

                if request.method == 'POST':
                    try:
                        fromdate = request.POST.get('fromdate')

                        todate = request.POST.get('todate')

                        orders = OrderItem.objects.filter(
                            created_at__range=[fromdate, todate], user_id=request.user, checkout_status='completed')
                        print(orders)
                        return render(request, 'orders.html', {'orders': orders, 'y': y})
                    except Exception:
                        print('enter from and to')
                        return render(request, 'orders.html', {'y': y})
                return render(request, 'orders.html', {'y': y})
        orders = OrderItem.objects.filter(
            user_id=request.user, checkout_status='completed').order_by('-created_at')
        return render(request, 'orders.html', {'orders': orders})


@ login_required(login_url='login')
def cartlist_del(request, i):
    OrderItem.objects.get(pk=i).delete()
    return redirect('/cartlist')


def signup(request):
    form = SignupForm()
    if request.method == 'POST':  # TRUE
        print(request.POST)
        form = SignupForm(request.POST)
        print(form['username'])
        # groups=
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customers')
            group.user_set.add(user)
            return redirect('/login')
    context = {'form': form}
    return render(request, 'signup.html', context)


@ unauthenticated_user
def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                username = request.user.username
                messages.info(request, "Welcome "+username)
                return redirect('/')
            # else:
                # messages.error(request, "Invalid Username or Password")
                # return redirect('/login')
    return render(request, 'login.html')


def logoutt(request):  # get
    logout(request)
    return redirect('/')


# @allowed_users(allowed_roles=['admin'])
def chef_create(request):
    form = ChefForm()
    if request.method == 'POST':
        form = ChefForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('chef_view')
    context = {'form': form}
    return render(request, 'chef_create.html', context)


# @allowed_users(allowed_roles=['admin'])
def chef_read(request, id):
    dynamicdata = Chef.objects.get(pk=id)
    context = {'dynamic': dynamicdata}
    return render(request, 'chef_read.html', context)


# @allowed_users(allowed_roles=['admin'])
def chef_update(request, id):
    z = Chef.objects.get(pk=id)
    form = ChefForm(instance=z)  # old data
    if request.method == 'POST':
        form = ChefForm(request.POST, instance=z)
        if form.is_valid():
            form.save()
            return redirect('chef_view')
    context = {'form': form}
    return render(request, 'chef_update.html', context)


# @allowed_users(allowed_roles=['admin'])
def chef_delete(request, id):
    Chef.objects.get(pk=id).delete()
    messages.info(request, "data deleted")
    return render(request, 'chef_delete.html')


# @allowed_users(allowed_roles=['admin'])
def chef_data(request):
    today = datetime.now().date()
    dynamicdata = Chef.objects.all()
    compl = OrderItem.objects.filter(
        status='complete', todayorders__gte=today).count()
    incom = OrderItem.objects.filter(
        status='incomplete', todayorders__gte=today).count()
    context = {'dynamic': dynamicdata}
    return render(request, 'chef_data.html', context)


# order Views
# @allowed_users(allowed_roles=['admin'])
def order_create(request):  # When user clicks on create order this fuciton will trigger
    form = OrderItemForm()  # first render empty form || return render(request, 'order_create.html', context) || this code will take the form variable from here and it will render the empty form
    # when user clicks the submit button after filling the order details this line will get execute, if this IF condition stisfies we will enter in to the loop.
    if request.method == 'POST':
        # This line of code will get all the data and files that are added in the form by user.
        form = OrderItemForm(request.POST, request.FILES)
        # Now the request is containing all the data that is entered by the user, out of that data we need only category. this line of code will bring what is the category that user selected.
        get_category = request.POST.get('category_name')
        # if the data entered in the form by user is a valid data, then enter in to the loop.
        if form.is_valid():
            # From the existing orders we have to filter the orders which are incomplete and the category that user selected. this is being done just to get the chef's who are still working on the pirticular category, so that we can assign this order to the chef who is still preparing that category order.
            geting_prepared = OrderItem.objects.filter(
                status='incomplete', category_name=get_category)
            # print('+++++++++++++',geting_prepared)
            # if you get the list of chefs who are working on the same category, then enter in to the loop.
            if geting_prepared:
                chef_dict = {}  # define an empty dict, this dict will have the {chef:orders_completed}
                # breakpoint()
                # iterate over the list of chefs(Querysets).
                for i in geting_prepared:
                    # get the chef names who are preparing the incomplete orders.
                    chef_name_q = i.prepared_by
                    # print('----------------------',chef_name_q)
                    # out of chefs who are preparing the incomplete orders, get their completed_orders number.
                    get_chef = Chef.objects.filter(chef_name=chef_name_q).values_list(
                        'orders_completed', flat=True)
                    for i in get_chef:  # get the filtered list of chefs orders that are completed
                        # create a dict || dict['sravan'] = 2, dict['ravan'] = 3, chef_dict[sushanth]:1
                        chef_dict[chef_name_q] = i
                # print('DICT',chef_dict)
                # Get the chefs orders who had prepared the less orders in a day.#get the key where the value is minimum#https://www.codegrepper.com/code-examples/python/how+to+find+the+minimum+value+in+a+dictionary+python
                chef_final = min(chef_dict, key=chef_dict.get)
                get_chef = Chef.objects.get(chef_name=chef_final)
                obj = form.save(commit=False)
                obj.prepared_by = get_chef
                obj.save()
            else:  # if the chef's are idle and not preparing any orders in line. all the existing orders are completed, if new order is comming up then assign the order to any available chef.
                get_chef = Chef.objects.filter(
                    chef_availability=1, category_name=get_category).first()
                obj = form.save(commit=False)  # instace: hold before you save.
                # before you save the customer order in database, assign a chef who is idle.
                obj.prepared_by = get_chef
                obj.save()  # save to DB

        return redirect('order_view')
    context = {'form': form}
    return render(request, 'order_create.html', context)


# def order_view(request, year= datetime.now().year, month= datetime.now().strftime('%B')):

    # dynamicdata = OrderItem.objects.filter(todayorders__gte=today, todayorders__lte=today)

    # start = todayorders(2012, 12, 11)
    # end =  todayorders(2012, 4, 30)
    # new_end = end + datetime.timedelta(days=1)

    # dynamicdata = OrderItem.objects.filter( todayorders =[start, new_end])
    # start=datetime(2021, 4, 30)
    # end=datetime(2022,4,30)

    # dynamicdata = OrderItem.objects.filter(todayorders=[start_date,end_date])
    # dynamicdata = OrderItem.objects.filter(pd.date_range(start= '2021, 4, 30', end='2022,4,30'))
    # order_list = OrderItem.objects.filter
    # if request.method == 'POST':
    #     search = request.POST['search_order']
    #     today = datetime.now()
    #     current_year= today.year

    #     dynamicdata= OrderItem.objects.filter(todayorders__year  = year)

    #     return redirect(request, 'order_view.html', context= {'dynamic': dynamicdata})
    # month = month.capitalize()
    # month_number= 12
    # month_number = list(calendar.month_number).index(month)
    # month_number = int(month_number)

    # cal = HTMLCalendar().formatmonth(year, month_number)
    # today = datetime.now()
    # current_year= today.year
    # dynamicdata= OrderItem.objects.filter(todayorders__year  = year ,
    #                                         todayorders__month= month_number)

    # time = now.strftime( '%I:%M  %p')
    # return redirect(request, 'order_view.html', context= {'dynamic': dynamicdata})

# @allowed_users(allowed_roles=['admin'])
def order_view(request):
    today = datetime.now().date()
    compl = OrderItem.objects.filter(
        status='complete', todayorders__gte=today).count()
    incompl = OrderItem.objects.filter(
        status='incomplete', todayorders__gte=today).count()
    dynamicdata = OrderItem.objects.filter(todayorders__gte=today)
    dy = OrderItem.objects.filter(
        todayorders__gte=today).aggregate(dy=Sum('price'))

    # ddata= OrderItem.objects.filter(sum(price = today))

    if request.method == 'POST':
        fromdate = request.POST.get('fromdate')
        # print('fromdata', fromdate)
        todate = request.POST.get('todate')
        # print('todata', todate)
        # search = OrderItem.objects.raw('select id,category_name_id, product_name_id, quantity,price,description,created_at,allocation,table_no, prepared_by_id,status, customer_id,todayorders from kritunga_orderitem where created_at between  "'+fromdate+'"  and "'+todate+'" ')
        search = OrderItem.objects.filter(created_at__range=[fromdate, todate])
        dy = OrderItem.objects.filter(
            created_at__range=[fromdate, todate]).aggregate(dy=Sum('price'))

        return render(request, 'order_view.html', context={'dynamic': search, 'd': dy})

    return render(request, 'order_view.html', context={'dynamic': dynamicdata, 'compl': compl, 'incompl': incompl, 'd': dy})


# @allowed_users(allowed_roles=['admin'])
def order_read(request, id):
    dynamicdata = OrderItem.objects.get(pk=id)
    context = {'dynamic': dynamicdata}
    return render(request, 'order_read.html', context)


# @allowed_users(allowed_roles=['admin'])
def order_update(request, id):
    z = OrderItem.objects.get(pk=id)
    form = OrderItemForm(instance=z)  # old data
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=z)
        if form.is_valid():
            form.save()
            return redirect('order_view')
    context = {'form': form}
    return render(request, 'order_update.html', context)


# @allowed_users(allowed_roles=['admin'])
def order_completed(request, id):
    OrderItem.objects.filter(pk=id).update(status='complete')
    chef_who_compltd_order = OrderItem.objects.filter(
        pk=id).values_list('prepared_by', flat=True)
    # orders_chef = Chef.objects.get(chef_name = chef_who_compltd_order)
    # # orders_chef_obj =
    # total_orders = orders_chef+1
    # Chef.objects.filter(chef_name = chef_who_compltd_order).update(orders_completed = total_orders )
    messages.info(request, "Order completed")
    return redirect('order_view')


# @allowed_users(allowed_roles=['admin'])
def order_delete(request, id):
    OrderItem.objects.get(pk=id).delete()
    messages.info(request, "data deleted")
    return redirect('order_view')


# @allowed_users(allowed_roles=['admin'])
def chef_orders(request, id):
    # roup = Group.objects.get(name='chefs')

    # print(users, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')

    # user = User.objects.get(Q(username=users[0]) or Q(username=users[1]))
    # print(user)

    # chef = Chef.objects.filter(chef_name=user)
    # print(chef, '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    chefdata = Chef.objects.get(id=id)
    # print(chefdata)
    today = datetime.now().date()
    dynamicdata = OrderItem.objects.filter(
        prepared_by=chefdata, todayorders__gte=today)
    compl = OrderItem.objects.filter(
        prepared_by=chefdata, status="complete", todayorders__gte=today).count()
    incompl = OrderItem.objects.filter(
        prepared_by=chefdata, status="incomplete").count()

    orders = OrderItem.objects.filter(
        prepared_by=chefdata, todayorders__gte=today, checkout_status='completed').order_by('-created_at')

    context = {'dynamic': dynamicdata, 'compl': compl,
               'incompl': incompl, 'orders': orders}
    return render(request, 'chef_order_view.html', context)


# @allowed_users(allowed_roles=['admin'])
def table_orders(request):
    if request.method == 'POST':
        search = request.POST['search']
        today = datetime.now().date()

        table = OrderItem.objects.filter(
            table_no=search, todayorders__gte=today)
        # print(table)
        # for i in table:
        # 	print(i.product_name)
        compl = OrderItem.objects.filter(
            status='complete', table_no=search, todayorders__gte=today).count()
        incom = OrderItem.objects.filter(
            status='incomplete', table_no=search, todayorders__gte=today).count()

        return render(request, 'table_order.html', context={'table': table, 'compl': compl, 'incom': incom})
    return render(request, 'table_order.html')
