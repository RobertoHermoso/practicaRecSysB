"""practicaRecSysB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('populate/',views.populate_db),
    path('recommended-books/',views.recommended_books, name="rec"),
    path('similar-users/',views.similar_users, name="sim"),
    path('book-genre/',views.libro_genero_list,name='generos'),
    path('best-libros/', views.best_libros,name='mejores'),
    path('', views.home)
]
