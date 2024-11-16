from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Profile
from .serializers import ProfileSerializer, CustomTokenObtainPairSerializer

class ProfileListCreateAPIView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    # GET method to list all profiles
    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data)

    # POST method to create a new profile
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveUpdateDestroyAPIView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Ensures that only authenticated users can access these views

    def get_object(self, user_id):
        try:
            return Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return None

    # GET method to retrieve a specific profile by user_id
    def get(self, request, user_id, *args, **kwargs):
        profile = self.get_object(user_id)
        if profile is not None:
            serializer = self.serializer_class(profile)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # PUT method to update a specific profile by user_id
    def put(self, request, user_id, *args, **kwargs):
        profile = self.get_object(user_id)
        if profile is not None:
            serializer = self.serializer_class(profile, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    # DELETE method to delete a specific profile by user_id
    def delete(self, request, user_id, *args, **kwargs):
        profile = self.get_object(user_id)
        if profile is not None:
            profile.delete()
            return Response({'detail': 'Profile deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
