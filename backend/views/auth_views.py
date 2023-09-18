from django.http import  JsonResponse
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.contrib.auth.models import auth
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from backend.forms import UserRegistrationForm
from rest_framework import status

@csrf_exempt
# @api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username is an email or a phone number
        if '@' in username:
            user = authenticate(request, username=username, password=password)
        else:
            user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            user_data = {
                'id': user.id,
                'firstname': user.first_name,
                'email': user.email,
                'phone': user.phone,
                'user_role': user.user_role,
            }

            response_data = {
                'message': 'Successful',
                'user': user_data,
                'access_token': access_token,
                'status': status.HTTP_200_OK,
            }
            return JsonResponse(response_data, status=status.HTTP_200_OK)
         
        else:
            error_response = {'error': 'Wrong Email or Password', 'status': status.HTTP_400_BAD_REQUEST}
            return JsonResponse(error_response, status=status.HTTP_400_BAD_REQUEST)

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')  # Use 'username' to receive the email from the request
#         password = request.POST.get('password')
       
#         user = authenticate(request, email=username, password=password)

#         if user is not None:
#             auth_login(request,user)
#             # Generate token
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             # token, created = Token.objects.get_or_create(user=user)
#             return JsonResponse({
#                 'message': 'Successful',
#                 'user': {
#                     'id': user.id,
#                     'firstname': user.first_name,
#                     'email': user.email,
#                     'phone': user.phone,
#                     'user_role': user.user_role,
#                 },
#                 'access_token': access_token,
#                 'status': 200,
#             }, status=200)
         
#         else:
#             return JsonResponse({'error': 'Wrong Email or Password', 'status': 400}, status=400)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user_role = 'user'

            if get_user_model().objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already registered', 'status': 400}, status=400)

            new_user = get_user_model().objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                user_role=user_role,
            )
            new_user.set_password(password)
            new_user.save()

            return JsonResponse({'message': 'User register successful', 'status': 200}, status=200)
        else:
            return JsonResponse({'error': form.errors, 'status': 400}, status=400)

    elif request.method == 'GET':
        users = get_user_model().objects.all()

        data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'user_role': user.user_role
            }
            for user in users
        ]
        return JsonResponse({'message': 'Successful', 'data': data, 'status': 200}, status=200)