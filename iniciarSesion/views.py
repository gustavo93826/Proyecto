from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
import json
from Gestion_Usuarios.models import Usuario


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            print(f"Recibido email: {email}, password: {password}")  # Verificar los datos recibidos

            if not email or not password:
                return JsonResponse({'error': 'Se requieren email y contraseña'}, status=400)

            try:
                user = Usuario.objects.get(email=email)
                print(f"Usuario encontrado: {user.nombre}, contrasena: {user.password}")  # Imprime el nombre del usuario encontrado
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

            print(f"Contraseña ingresada: {password}")  # Verificar la contraseña cifrada en la base de datos

            if check_password(password, user.password):
                print("Contraseña válida")
                return JsonResponse({'rol': user.rol}, status=200)
            else:
                print("Contraseña inválida")
                return JsonResponse({'error': 'Credenciales inválidas'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de datos no válido'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Ocurrió un error interno: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido. Usa POST.'}, status=405)


# Nueva función para probar hashing de contraseñas
def test_password_hashing(request):
    password_plain = "123"
    password_hashed = make_password(password_plain)
    is_valid = check_password(password_plain, password_hashed)
    return JsonResponse({
        "plain_password": password_plain,
        "hashed_password": password_hashed,
        "is_valid": is_valid
    })
