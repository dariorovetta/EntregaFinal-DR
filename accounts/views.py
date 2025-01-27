from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from accounts.forms import UserRegisterForm, UserEditForm, MiCambioDePassword
from accounts.models import ExtensionUsuario

# Vista del login
def login_request(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            extensionusuario, es_nuevo = ExtensionUsuario.objects.get_or_create(user=request.user)

            return redirect('Inicio')

    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {'form': form})


# Vista para crear usuario
def register(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("Inicio")

    else:
        form = UserRegisterForm()

    return render(request, "accounts/registro.html", {"form": form})


# Vista de los datos del usuario
@login_required
def perfil(request):
    return render(request, 'accounts/perfil.html', {})


# Vista de editar perfil de usuario
@login_required
def editarPerfil(request):

    # Instancia del login
    user = request.user

    # Si es metodo POST hago lo mismo que el agregar
    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST, request.FILES)

        if miFormulario.is_valid():

            informacion = miFormulario.cleaned_data

            # Datos que se modificaran
            user.first_name = informacion['first_name']
            user.last_name = informacion['last_name']
            user.email = informacion['email']
            user.extensionusuario.avatar = informacion['avatar']
            user.extensionusuario.descripcion = informacion['descripcion']
            user.extensionusuario.red_social = informacion['red_social']

            user.extensionusuario.save()
            user.save()

            return redirect('Perfil')

    else:
        miFormulario = UserEditForm(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'avatar': user.extensionusuario.avatar,
                'descripcion': user.extensionusuario.descripcion,
                'red_social': user.extensionusuario.red_social,
            }
        )

    return render(request, "accounts/editarPerfil.html", {"miFormulario": miFormulario, "usuario": user})


# Vista para cambiar contraseña
class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/cambiarContrasenia.html'
    success_url = '/perfil/'
    form_class = MiCambioDePassword
