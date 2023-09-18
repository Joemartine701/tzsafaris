import json
import os
from django.http import JsonResponse
from django.conf import settings
from backend.models.tour_model import TourModel
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST','GET','PUT','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def tour(request, tour_id=None):
    if request.method == 'POST':
        try:
            # Handle file uploads
            image_path = None
            video_path = None

            if 'image' in request.FILES:
                image = request.FILES['image']
                # Save the image to the media directory
                image_path = os.path.join(settings.MEDIA_ROOT, 'images', image.name)
                with open(image_path, 'wb') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            if 'video' in request.FILES:
                video = request.FILES['video']
                # Save the video to the media directory
                video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video.name)
                with open(video_path, 'wb') as destination:
                    for chunk in video.chunks():
                        destination.write(chunk)

            # Rest of your code for creating a new tour
            tour_name = request.POST.get('tour_name')
            tour_location = request.POST.get('tour_location')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            tour_price = request.POST.get('tour_price')
            description = request.POST.get('description')
            tour_brand = request.POST.get('tour_brand')
            tour_budg_fooddrink = request.POST.get('tour_budg_fooddrink')
            tour_budg_transpt = request.POST.get('tour_budg_transpt')
            tour_budg_others = request.POST.get('tour_budg_others')

            tour = TourModel(
                tour_name=tour_name,
                tour_location=tour_location,
                start_date=start_date,
                end_date=end_date,
                tour_price=tour_price,
                image=image_path[len(settings.MEDIA_ROOT):] if image_path else '',
                video=video_path[len(settings.MEDIA_ROOT):] if video_path else '',
                description=description,
                tour_brand=tour_brand,
                tour_budg_fooddrink=tour_budg_fooddrink,
                tour_budg_transpt=tour_budg_transpt,
                tour_budg_others=tour_budg_others
                # Add other fields here based on your JSON data
            )
            tour.save()

            return JsonResponse({'message': 'Tour created successfully', 'image_url': tour.image.url, 'video_url': tour.video.url}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 400}, status=400)

    if request.method == 'GET':
        # Handle the GET request to retrieve tour data
        try:
            if tour_id:
                # Retrieve a specific tour by ID
                tour = get_object_or_404(TourModel, id=tour_id)
                tour_data = {
                    'id' : tour.id,
                    'tour_name': tour.tour_name,
                    'tour_location': tour.tour_location,
                    'start_date': tour.start_date,
                    'end_date': tour.end_date,
                    'tour_price': tour.tour_price,
                    'description': tour.description,
                    'tour_brand': tour.tour_brand,
                    'tour_budg_fooddrink': tour.tour_budg_fooddrink,
                    'tour_budg_transpt': tour.tour_budg_transpt,
                    'tour_budg_others': tour.tour_budg_others,
                    # Extract and include file URLs
                    'image_url': tour.image.url if tour.image else '',
                    'video_url': tour.video.url if tour.video else '',
                    'created_at' : tour.created_at,
                    'updated_at' : tour.updated_at,
                }
                return JsonResponse({'message': 'successfully', 'tour': tour_data}, status=200)
            else:
                # Retrieve all tours
                tours = TourModel.objects.all()
                tour_list = []

                for tour in tours:
                    tour_data = {
                        'id' : tour.id,
                        'tour_name': tour.tour_name,
                        'tour_location': tour.tour_location,
                        'start_date': tour.start_date,
                        'end_date': tour.end_date,
                        'tour_price': tour.tour_price,
                        'description': tour.description,
                        'tour_brand': tour.tour_brand,
                        'tour_budg_fooddrink': tour.tour_budg_fooddrink,
                        'tour_budg_transpt': tour.tour_budg_transpt,
                        'tour_budg_others': tour.tour_budg_others,
                        # Extract and include file URLs
                        'image_url': tour.image.url if tour.image else '',
                        'video_url': tour.video.url if tour.video else '',
                        'created_at' : tour.created_at,
                        'updated_at' : tour.updated_at,
                    }
                    tour_list.append(tour_data)

                return JsonResponse({'message': 'successfully', 'tour': tour_list}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'PUT':
        try:
            if tour_id:
                # Update an existing tour by ID
                tour = get_object_or_404(TourModel, id=tour_id)
                # Update tour fields based on your JSON data or form data
                # Example:
                tour.tour_name = request.POST.get('tour_name')
                tour.tour_location = request.POST.get('tour_location')
                # Update other fields as needed
                tour.save()
                return JsonResponse({'message': 'Tour updated successfully', 'image_url': tour.image.url, 'video_url': tour.video.url}, status=200)
            else:
                return JsonResponse({'error': 'Tour ID is missing in the request'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 400}, status=400)

    if request.method == 'DELETE':
        try:
            if tour_id:
                # Delete a specific tour by ID
                tour = get_object_or_404(TourModel, id=tour_id)
                tour.delete()
                return JsonResponse({'message': 'Tour deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Tour ID is missing in the request'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 400}, status=400)
