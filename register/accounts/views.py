from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import re

def validate_username(username):
    """Validate username format"""
    if not username or len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, ""

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, ""

@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    """Handle user registration"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', '')
        
        if not email or not password or not username:
            return JsonResponse({
                'success': False,
                'message': 'Username, email and password are required'
            }, status=400)
        
        valid, error = validate_username(username)
        if not valid:
            return JsonResponse({
                'success': False,
                'message': error
            }, status=400)
        
        valid, error = validate_password(password)
        if not valid:
            return JsonResponse({
                'success': False,
                'message': error
            }, status=400)
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'User with this email already exists'
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Username already taken'
            }, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        if name:
            first_name = name.split()[0] if name else ''
            last_name = ' '.join(name.split()[1:]) if len(name.split()) > 1 else ''
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'username': user.username,
                'email': user.email,
                'name': user.get_full_name() or user.username
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Handle user login"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({
                'success': False,
                'message': 'Email and password are required'
            }, status=400)
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'email': user.email,
                    'name': user.get_full_name() or user.username
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid email or password'
            }, status=401)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@require_http_methods(["POST"])
def logout_view(request):
    """Handle user logout"""
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Logout successful'
    })


@require_http_methods(["GET"])
def user_status(request):
    """Check if user is authenticated"""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'email': request.user.email,
                'name': request.user.get_full_name() or request.user.username
            }
        })
    else:
        return JsonResponse({
            'authenticated': False
        })
