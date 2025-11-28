# Luxor Propiedades – Proyecto Django

Este proyecto es una aplicación web desarrollada en **Django** que permite a los usuarios navegar por una página inmobiliaria y enviar a través de un formulario una consulta.  
El sistema envía mails al cliente informando sobre estas consultas, tambien tiene un panel de administración al cual se puede acceder registrándose mediante una doble verificación.

## Características principales

- Formulario validado en frontend con JavaScript.  
- Envío del formulario mediante Fetch API sin recargar la página.   
- Procesamiento del test y generación del perfil profesional desde Django.  
- Se simula el consumo de una API externa para traer novedades.
- Panel de administración de consultas (Estadísticas, Editar y eliminar consultas).
- Sistema de registro con doble validación (Admin debe registrar al usuario para permitirle registrarse).
- Envío de mail con código de validación para registrarse.

## Tecnologías utilizadas

- **Django**
- **Python**
- **JavaScript**
- **HTML + CSS**
- **Bootstrap**
- **PostgreSQL**

## Api utilizada    

- Para este trabajo, al no encontrar una API inmobiliaria gratuita y sencilla de implementar, se optó por realizar una implementación básica utilizando la API de **JSONPlaceholder**, simulando un panel de noticias en el inicio con el texto de relleno que provee dicha API.  
- API utilizada: http://jsonplaceholder.typicode.com/

---

## Credenciales del panel administración

username: postgres  
password: DjangoWeb2

nota: el mail solicitado en la consigna ya se encuentra autorizado para registro.
