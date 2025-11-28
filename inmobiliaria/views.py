from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ContactoForm, RegistroForm
from .models import Consulta, UsuarioPermitido
from .utils import clasificar_categoria, obtener_novedades_externas
from .serializers import ConsultaSerializer

# Create your views here.
def pagina_inicio(request):
    novedades = obtener_novedades_externas()

    context = {
        "novedades": novedades
    }

    return render(request, 'inmobiliaria/index.html', context)

def propiedades(request):
    return render(request, 'inmobiliaria/propiedades.html')

def contacto(request):
    form = ContactoForm()

    if request.method == "POST":
        form = ContactoForm(request.POST)

        if form.is_valid():
            consulta = form.cleaned_data

            categoria = clasificar_categoria(consulta["mensaje"])

            nueva = Consulta.objects.create(
                nombre=consulta["nombre"],
                email=consulta["email"],
                asunto=consulta["asunto"],
                mensaje=consulta["mensaje"],
                fecha=consulta["fecha"],
                categoria=categoria,
            )

            asunto_email = f"[{categoria}] Nueva consulta recibida"
            cuerpo = (
                f"Has recibido una nueva consulta.\n\n"
                f"Nombre: {nueva.nombre}\n"
                f"Email: {nueva.email}\n"
                f"Asunto: {nueva.asunto}\n"
                f"Fecha tentativa: {nueva.fecha}\n"
                f"Categoría asignada: {categoria}\n\n"
                f"Mensaje:\n{nueva.mensaje}"
            )

            try:
                send_mail(
                    asunto_email,
                    cuerpo,
                    settings.EMAIL_HOST_USER,
                    [settings.CLIENTE_EMAIL],
                    fail_silently=False
                )

                messages.success(request, "Tu consulta fue enviada correctamente.")
                form = ContactoForm()  # limpiar formulario luego del envío

            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {e}")

    return render(request, 'inmobiliaria/contacto.html', {'form': form})
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            # Verificar si está permitido
            try:
                permitido = UsuarioPermitido.objects.get(email=email)
            except UsuarioPermitido.DoesNotExist:
                messages.error(request, "Acceso restringido. No está autorizado a utilizar este sistema.")
                return render(request, "auth/registro.html", {"form": form})

            # Crear usuario desactivado
            usuario = form.save(commit=False)
            usuario.username = email
            usuario.is_active = False
            usuario.save()

            # Enviar mail con código
            asunto = "Validación de cuenta"
            mensaje = (
                f"Hola {usuario.first_name},\n\n"
                f"Tu código de validación es: {permitido.codigo_validacion}\n\n"
                f"Validá tu cuenta ingresando aquí:\n"
                f"https://luxor-site-webii.onrender.com/validar-cuenta/"
            )

            send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email])

            messages.success(
                request,
                "Le llegará un correo para validar su cuenta. Ingrese el código para activar su cuenta."
            )
            return redirect("validar_cuenta")

        else:
            # ACÁ va el error si el form es inválido
            messages.error(
                request,
                "Error al registrar la cuenta. Verifique los datos ingresados y que las contraseñas coincidan."
            )

    else:
        # SOLO carga el formulario, SIN mensajes
        form = RegistroForm()

    return render(request, "auth/registro.html", {"form": form})
def validar_cuenta(request):
    if request.method == "POST":
        email = request.POST.get("email")
        codigo = request.POST.get("codigo")

        try:
            permitido = UsuarioPermitido.objects.get(email=email)
        except UsuarioPermitido.DoesNotExist:
            messages.error(request, "Correo no permitido.")
            return render(request,"auth/validar_cuenta.html")

        # Comparar códigos
        if permitido.codigo_validacion != codigo:
            messages.error(request, "Código incorrecto.")
            return render(request,"auth/validar_cuenta.html")

        # Activar usuario
        try:
            usuario = User.objects.get(username=email)
        except User.DoesNotExist:
            messages.error(request, "El usuario no existe. Regístrese primero.")
            return redirect("registro")

        usuario.is_active = True
        usuario.save()

        messages.success(request, "Cuenta validada correctamente. Ya puede iniciar sesión.")
        return redirect("login")

    return render(request, "auth/validar_cuenta.html")

@login_required
def panel(request):
    consultas = Consulta.objects.all().order_by("-fecha_envio")

    # Estadísticas
    total = consultas.count()
    comercial = consultas.filter(categoria="Consulta Comercial").count()
    tecnica = consultas.filter(categoria="Consulta Técnica").count()
    rrhh = consultas.filter(categoria="Consulta de RRHH").count()
    general = consultas.filter(categoria="Consulta General").count()

    contexto = {
        "consultas": consultas,
        "total": total,
        "comercial": comercial,
        "tecnica": tecnica,
        "rrhh": rrhh,
        "general": general,
    }

    return render(request, "auth/panel.html", contexto)


@login_required
def editar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)

    if request.method == "POST":
        consulta.nombre = request.POST.get("nombre")
        consulta.email = request.POST.get("email")
        consulta.asunto = request.POST.get("asunto")
        consulta.mensaje = request.POST.get("mensaje")
        consulta.categoria = request.POST.get("categoria")
        consulta.save()

        messages.success(request, "Consulta modificada correctamente.")
        return redirect("panel")

    return render(request, "auth/editar_consulta.html", {"consulta": consulta})


@login_required
def eliminar_consulta(request, id):
    consulta = get_object_or_404(Consulta, id=id)
    consulta.delete()
    messages.success(request, "Consulta eliminada correctamente.")
    return redirect("panel")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("EMAIL RECIBIDO:", repr(email))
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Credenciales incorrectas.")
            return render(request, "auth/login.html")

        user = authenticate(request, username=user_obj.username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect("panel")
            else:
                messages.error(request, "Tu cuenta aún no fue validada.")
        else:
            messages.error(request, "Contraseña incorrecta.")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
class ConsultaListAPIView(generics.ListAPIView):
    queryset = Consulta.objects.all().order_by('-fecha_envio')
    serializer_class = ConsultaSerializer
