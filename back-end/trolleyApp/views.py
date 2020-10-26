import hashlib
from datetime import datetime
from json import JSONEncoder
from random import randrange

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder

from trolleyApp.models import User, Trolly, Occupied_trollies

from MQTTClient import MQTTClient
from point_generator import traverse_points
from update import update_database

# Create your views here.

@csrf_exempt
def register_user(request):
    """register a user in system"""
    if 'username' in request.POST.keys():
        this_username = request.POST['username']
    if 'email' in request.POST.keys():
        email = request.POST['email']
    if 'phone_number' in request.POST.keys():
        phone_number = request.POST['phone_number']
    if 'password' in request.POST.keys():
        password = request.POST['password']
        salt = str(randrange(10 ** 48, 10 ** 49))
        hashed_password = hashPassword(password, salt)
    if 'user_type' in request.POST.keys():
        user_type = request.POST['user_type']
    else:
        user_type = 1

    if User.objects.filter(username=this_username).count() != 0:
        return JsonResponse({
            'status': 'Error',
            'message': 'username was already defined'
        }, encoder=JSONEncoder)

    if User.objects.filter(phone_number=phone_number).count() != 0:
        return JsonResponse({
            'status': 'Error',
            'message': 'phone number is used before'
        }, encoder=JSONEncoder)
  
    if User.objects.filter(email=email).count() != 0:
        return JsonResponse({
            'status': 'Error',
            'message': 'Email is used before'
        }, encoder=JSONEncoder)
    
    # User.objects.create(username=this_username, email=email, phone_number=phone_number, 
    #     salt=salt, hashed_password=hashed_password)
    new_user = User(username=this_username, email=email, phone_number=phone_number, 
        salt=salt, hashed_password=hashed_password, user_type=user_type)
    new_user.save()
    return JsonResponse({
        'status' : 'ok',
        'message' : 'User registerd'
    }, encoder=JSONEncoder)


@csrf_exempt
def login(request):
    """login user"""
    if 'username' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'username field is empty'
        }, encoder=JSONEncoder)
    if 'password' not in request.POST.keys():
        return JsonResponse({
            'status': 'Error',
            'message': 'password field is empty'
        }, encoder=JSONEncoder)
    if 'user_type' in request.POST.keys() and request.POST['user_type'] != '':
        user_type = request.POST['user_type']
    else:
        user_type = 1

    this_username = request.POST['username']
    this_password = request.POST['password']
    if User.objects.filter(username=this_username).count() == 0:
        return JsonResponse({
            'status': 'Error', 
            'message': f'No user with username \"{this_username}\"'
        }, encoder=JSONEncoder)

    user_obj = User.objects.get(username=this_username)
    if int(user_obj.user_type) != int(user_type):
        return JsonResponse({
            'status': 'Error', 
            'message': 'user_type does not match'
        }, encoder=JSONEncoder)
    if hashPassword(this_password, user_obj.salt) == user_obj.hashed_password:
        return JsonResponse({
            'status': 'ok',
            'message': 'user loged in'
        }, encoder=JSONEncoder)
    else:
        return JsonResponse({
            'status': 'Error',
            'message': 'wrong password'
        }, encoder=JSONEncoder)
            
 
def hashPassword(password, salt):
    salted_password = salt + password
    return hashlib.md5(salted_password.encode()).hexdigest()


@csrf_exempt
def get_trolly_info(request):
    print('\n', '==' * 20, '\n')
    print(request.method)
    print('\n', '==' * 20, '\n')
    if request.method == 'GET':
        if 'id' in request.GET.keys():
            trolly_obj = Trolly.objects.get(trolley_id=request.GET['id'])
        return JsonResponse({
            'x': trolly_obj.x,
            'y': trolly_obj.y,
            'isOccupied': trolly_obj.isOccupied,
            'last_update': trolly_obj.last_update
        }, encoder=DjangoJSONEncoder)


@csrf_exempt
def register_trolly(request):
    print('\n', '==' * 20, '\n')
    print(request.POST) 
    print('\n', '==' * 20, '\n')

    if 'x' in request.POST.keys():
        x = request.POST['x']
    if 'y' in request.POST.keys():
        y = request.POST['y']
    if 'isOccupied' in request.POST.keys() and request.POST['isOccupied'] != '':
        isOccupied = request.POST['isOccupied']
    else:
        isOccupied = False
    if 'last_update' in request.POST.keys() and request.POST['last_update'] != '':
        last_update = request.POST['last_update']
    else:
        last_update = datetime.now()
    
    new_trolly = Trolly(x=x, y=y, isOccupied=isOccupied, last_update=last_update)
    new_trolly.save()
    return JsonResponse({
        'status': 'ok',
        'message': 'trolly added succsesfully',
        'id': new_trolly.trolley_id
    }, encoder=JSONEncoder)


@csrf_exempt
def register_trolly_by_code(request):
    print('\n', '==' * 20, '\n')
    print(request.POST)
    print('\n', '==' * 20, '\n')

    if 'x' in request.POST.keys():
        x = request.POST['x']
    if 'y' in request.POST.keys():
        y = request.POST['y']
    if 'id' in request.POST.keys() and request.POST['id'] != '':
        if int(request.POST['id']) <= 100:
            return JsonResponse({
                'status': 'Error',
                'message': 'id is less that 100'
            }, encoder=DjangoJSONEncoder)
        else:
            if Trolly.objects.filter(trolley_id=int(request.POST['trolley_id'])).count() != 0:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'id was assigned to another trolly'
                }, encoder=DjangoJSONEncoder)
            trolly_id = request.POST['id']
    if 'isOccupied' in request.POST.keys() and request.POST['isOccupied'] != '':
        isOccupied = request.POST['isOccupied']
    else:
        isOccupied = False
    if 'last_update' in request.POST.keys() and request.POST['last_update'] != '':
        last_update = request.POST['last_update']
    else:
        last_update = datetime.now()
    if Trolly.objects.filter(trolley_id=trolly_id).count() == 0: 
        new_trolly = Trolly(x=x, y=y, isOccupied=isOccupied, last_update=last_update, trolley_id=trolly_id)
        new_trolly.save()
        return JsonResponse({
            'status': 'ok',
            'message': 'trolly added succsesfully',
            'id': new_trolly.trolley_id
        }, encoder=JSONEncoder)
    else:
        trolly_obj = Trolly.objects.get(trolley_id=int(id))
        trolly_obj.x = float(x)
        trolly_obj.x = float(y)
        trolly_obj.last_update = datetime.now()
        trolly_obj.save()
        return JsonResponse({
            'status': 'ok',
            'message': 'trolly updated succesfully'
            }, encoder=DjangoJSONEncoder)



@csrf_exempt
def occupy_trolly(request):
    if request.method == 'POST':
        if 'trolly_id' in request.POST.keys():
            trolly_id = request.POST['trolly_id']
        else:
            return JsonResponse({
                'status': 'Error', 
                'message': 'trolly not mentioned'
            }, encoder=DjangoJSONEncoder)  
        if 'username' in request.POST.keys():
            username = request.POST['username']
        else:
            return JsonResponse({
                'status': 'Error', 
                'message': 'user not mentioned'
            }, encoder=DjangoJSONEncoder)
        
        user_obj = User.objects.get(username=username)
        trolly_obj = Trolly.objects.get(trolley_id=trolly_id)
        occupied_trollies_list = Occupied_trollies.objects.all()
        print('\n', '==' * 20, '\n')
        for i in occupied_trollies_list:
            if user_obj.username == i.user.username:
                return JsonResponse({
                    'status': 'Error',
                    'message': 'user has already occupied a trolly'
                }, encoder=DjangoJSONEncoder)
        for i in occupied_trollies_list:
            if int(trolly_obj.trolley_id) == int(trolly_id):
                return JsonResponse({
                    'status': 'Error',
                    'message': 'The trolly has been accupied yet'
                }, encoder=DjangoJSONEncoder)

        trolly_obj.isOccupied = True
        occ_obj = Occupied_trollies(user=user_obj, trolly=trolly_obj)
        occ_obj.save()
        trolly_obj.save()
        # occ_obj = Occupied_trollies.objects.get(user=user_obj)
        return JsonResponse({
            'status': 'ok',
            'message': f'trolly {trolly_obj.trolley_id} occupied by user {username}',
            'occupy_id': f'{occ_obj.occupied_id}'
        }, encoder=DjangoJSONEncoder)
    else:
        return JsonResponse({
            'status': 'Error',
            'message': 'GET request not defined for this address'
        }, encoder=DjangoJSONEncoder)
        

@csrf_exempt
def get_available_trollies(request):
    if request.method == 'POST':
        if 'username' in request.POST.keys():
            username = request.POST['username']
        else:
            return JsonResponse({
                'status': 'Error',
                'message': 'username was not mentioned'
            }, encoder=DjangoJSONEncoder)
        
        occupied_trollies_list = Occupied_trollies.objects.all()
        for i in occupied_trollies_list:
            if i.user.username == username:
                return JsonResponse({
                    '0': {
                        'status': 'ok',
                        'message': 'user already has occupied a trolly',
                        'id': i.trolly.trolley_id,
                        'x': i.trolly.x,
                        'y': i.trolly.y
                        }
                }, encoder=DjangoJSONEncoder)
        
        response_json = dict()
        not_occupied_trollies_list = Trolly.objects.filter(isOccupied=False)
        for ind, trolly in enumerate(not_occupied_trollies_list):
            inner_dict = dict()
            inner_dict['id'] = trolly.trolley_id
            inner_dict['x'] = trolly.x
            inner_dict['y'] = trolly.y
            response_json[str(ind)] = inner_dict
        return JsonResponse(response_json, encoder=DjangoJSONEncoder)


@csrf_exempt
def free_trolly(request):
    if request.method == 'POST':
        if 'trolly_id' in request.POST.keys() and request.POST['trolly_id'] != '':
            trolly_id = request.POST['trolly_id']
        else:
            return JsonResponse({
                'status': 'Error',
                'message': 'trolly_id was not mentioned'
            }, encoder=DjangoJSONEncoder)
        
        occupied_trollies_list = Occupied_trollies.objects.all()
        for i in occupied_trollies_list:
            if int(i.trolly.trolley_id) == int(trolly_id):
                i.trolly.isOccupied = False
                i.trolly.save()
                i.delete()
                return JsonResponse({
                    'status': 'ok',
                    'message': f'trolly {trolly_id} is free now'
                }, encoder=DjangoJSONEncoder)
        return JsonResponse({
            'status': 'Error',
            'message': 'trolly was not occupied before'
        }, encoder=DjangoJSONEncoder)


mqttc = MQTTClient()
mqttc.start()
mqttc.subscribe('GPS')
mqttc.loop_start()

traverse_points()
update_database()
