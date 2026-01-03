from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Tell JWT to use email as login field
    username_field = 'email'

    def validate(self, attrs):
        # attrs contains 'email' and 'password'
        data = super().validate(attrs)
        # Include extra user info
        data.update({
            "user_id": self.user.id,
            "email": self.user.email,
            "is_staff": self.user.is_staff,
        })
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
