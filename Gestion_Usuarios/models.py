from django.db import models
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    ROLES = [
        (1, 'Administrador'),
        (2, 'Abogado'),
        (3, 'Auxiliar Administrativo'),
        (4, 'Asistente'),
    ]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Cambiado de 'correo' a 'email'
    password = models.CharField(max_length=128)  # Cifrada
    rol = models.IntegerField(choices=ROLES)

    def save(self, *args, **kwargs):
        # Cifrar la contraseña antes de guardar
        if not self.pk or Usuario.objects.filter(pk=self.pk).exists():
            self.password = make_password(self.password)
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "Usuarios"
