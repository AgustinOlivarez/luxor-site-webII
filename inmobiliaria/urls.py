from django.urls import path
from . import  views
from .views import ConsultaListAPIView
from .views import login_view, logout_view, registro, validar_cuenta, ConsultaListAPIView, panel, editar_consulta, eliminar_consulta,PasswordResetRequestView,PasswordResetConfirmCustomView

urlpatterns = [
    path('', views.pagina_inicio, name='index'),
    path('propiedades/', views.propiedades, name='propiedades'),
    path('contacto/', views.contacto, name='contacto'),
    path("api/consultas/", ConsultaListAPIView.as_view(), name="api_consultas"),
    path('registro/', registro, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('validar-cuenta/', validar_cuenta, name='validar_cuenta'),
    path('panel', panel, name='panel'),
    path("panel/editar/<int:id>/", editar_consulta, name="editar_consulta"),
    path("panel/eliminar/<int:id>/", eliminar_consulta, name="eliminar_consulta"),
    path('reset-password/',PasswordResetRequestView.as_view(),name='password_reset'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmCustomView.as_view(),name='password_reset_confirm'),
]