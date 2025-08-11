from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from bson import ObjectId

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that reads the access token from cookies
    and works with MongoDB ObjectIds
    """
    
    def authenticate(self, request):
        print("Authenticating with CookieJWTAuthentication")
        
        raw_token = request.COOKIES.get('access')
        
        if raw_token is None:
            print("No access token found in cookies")
            return None
        
        try:
            # Validate the token
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            
            if user:
                print(f"Authentication successful for user: {user.email}")
                return (user, validated_token)
            else:
                print("User not found")
                return None
                
        except TokenError as e:
            print(f"Token validation failed: {e}")
            return None
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def get_user(self, validated_token):
        """
        Get user from token - handle MongoDB ObjectId
        """
        try:
            user_id = validated_token.get('user_id')
            print(f"Looking for user with ID: {user_id}")
            
            from tasks.models import User  
            
            # For MongoDB-ObjectId
            user = User.objects.get(id=ObjectId(user_id))
            return user
                
        except User.DoesNotExist:
            print(f"User with ID {user_id} not found")
            return None
        except Exception as e:
            print(f"Error getting user from token: {e}")
            return None