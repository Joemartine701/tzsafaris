from django.http import  JsonResponse
from django.contrib.auth import get_user_model, authenticate, login as auth_login
from django.contrib.auth.models import auth
from django.shortcuts import get_object_or_404
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



@csrf_exempt
def edit_user(request, user_id):
    if request.method == 'GET':
        try:
            # Retrieve the user by ID
            user = get_object_or_404(get_user_model(), id=user_id)

            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'user_role': user.user_role,
            }

            return JsonResponse({'message': 'Successfully retrieved user data', 'user': user_data, 'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 400}, status=400)

@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        try:
            user = request.user  # Get the currently logged-in user

            # Update user fields based on your JSON data or form data
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')

            # Save the updated user profile
            user.save()

            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'user_role': user.user_role,
            }

            return JsonResponse({'message': 'User profile updated successfully', 'user': user_data, 'status': 200}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 400}, status=400)
