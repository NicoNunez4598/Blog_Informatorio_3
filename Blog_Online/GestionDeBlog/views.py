import smtplib
from typing import Any
from django.shortcuts import render, redirect
from .models import Post, Categoria
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import Categoria, Usuario, Post, Comentario
from .forms import CustomUserCreationForm, CustomUserCreationForm2, ResetPasswordForm
from django.urls import reverse
from django.views.generic import FormView
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

# Create your views here.

def home(request):
    queryset = request.GET.get("buscar")
    post = Post.objects.filter(estado = True)
    if queryset:
        post = Post.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset)
        ).distinct()
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    return render(request, 'index.html', {'post':post})

def generales(request):
    queryset = request.GET.get("buscar")
    post = Post.objects.filter(estado = True, categoria = Categoria.objects.get(nombre__iexact = 'Generales'))
    if queryset:
        post = Post.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset),
            estado = True, 
            categoria = Categoria.objects.get(nombre__iexact = 'Generales')
        ).distinct()
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    return render(request, 'generales.html', {'post':post})

def realidadVirtual(request):
    queryset = request.GET.get("buscar")
    post = Post.objects.filter(estado = True, categoria = Categoria.objects.get(nombre__iexact = 'Realidad Virtual'))
    if queryset:
        post = Post.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset),
            estado = True, 
            categoria = Categoria.objects.get(nombre__iexact = 'Realidad Virtual')
        ).distinct()
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    return render(request, 'realidadVirtual.html', {'post':post})

def realidadAumentada(request):
    queryset = request.GET.get("buscar")
    post = Post.objects.filter(estado = True, categoria = Categoria.objects.get(nombre__iexact = 'Realidad Aumentada'))
    if queryset:
        post = Post.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset),
            estado = True, 
            categoria = Categoria.objects.get(nombre__iexact = 'Realidad Aumentada')
        ).distinct()
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    return render(request, 'realidadAumentada.html', {'post':post})

def educacionAmbiental(request):
    queryset = request.GET.get("buscar")
    post = Post.objects.filter(estado = True, categoria = Categoria.objects.get(nombre__iexact = 'Educacion Ambiental'))
    if queryset:
        post = Post.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset),
            estado = True, 
            categoria = Categoria.objects.get(nombre__iexact = 'Educacion Ambiental')
        ).distinct()
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    return render(request, 'educacionAmbiental.html', {'post':post})

def rvyraenea(request):
    queryset = request.GET.get("buscar")
    post = Post.objects.filter(estado = True, categoria = Categoria.objects.get(nombre__iexact = 'Realidad Virtual y Realidad Aumentada en Educacion Ambiental'))
    if queryset:
        post = Post.objects.filter(
            Q(titulo__icontains = queryset) |
            Q(descripcion__icontains = queryset),
            estado = True, 
            categoria = Categoria.objects.get(nombre__iexact = 'Realidad Virtual y Realidad Aumentada en Educacion Ambiental')
        ).distinct()
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    return render(request, 'rvyraenea.html', {'post':post})

def detallepost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comentarioslistados = Comentario.objects.filter(post=post)
    return render(request, 'post.html', {'detallepost':post, 'comentarioslistados':comentarioslistados})

@login_required

def registrarcomentario(request, pk):
    if request.method == "POST":
        contenido = request.POST.get('txtContenido', '')
        if contenido:
            autor = request.user
            post = get_object_or_404(Post, id=pk)
            comentario = Comentario.objects.create(contenido=contenido, autor=autor, post=post)
            messages.success(request, 'Se ha registrado un comentario')
        else:
            messages.error(request, 'El comentario no puede estar vacío')

    return redirect ('detallepost', slug=post.slug)

def eliminarcomentario(request, id):
    
    comentario = Comentario.objects.get(id=id)

    post = comentario.post

    comentario.delete()

    messages.success(request, 'Se ha eliminado el comentario seleccionado')

    return redirect('detallepost', slug=post.slug)

def exit(request):
    logout(request)
    return redirect('inicio')

def categorias(request):
    categoriaslistadas = Categoria.objects.all()
    return render(request, 'categorias.html', {"categoriaslistadas" : categoriaslistadas})

def registrarcategoria(request):

    nombre=request.POST['txtNombre']
    estado=True

    categoria = Categoria.objects.create(nombre=nombre, estado=estado)

    messages.success(request, 'Se ha registrado una categoria')

    return redirect('categorias')

def edicioncategoria(request, id):

    categoria = Categoria.objects.get(id=id)

    return render(request, 'edicionCategorias.html', {"categoria":categoria})

def editarcategoria(request):

    id = request.POST['numberid']
    nombre=request.POST['txtNombre']
    estado=request.POST['estado']

    categoria = Categoria.objects.get(id=id)
    categoria.nombre = nombre
    categoria.estado = estado

    categoria.save()

    messages.success(request, 'Se ha editado con exito la categoria seleccionada')

    return redirect('categorias')

def eliminarcategoria(request, id):
    
    categoria = Categoria.objects.get(id=id)

    categoria.delete()

    messages.success(request, 'Se ha eliminado la categoria seleccionada')

    return redirect('categorias')

def usuarios(request):
    usuarioslistados = Usuario.objects.all()
    return render(request, 'usuarios.html', {"usuarioslistados" : usuarioslistados})

def registrarusuario(request):
    default_data = {'categoria': 'Colaborador'}
    data = {
        'form' : CustomUserCreationForm2(initial=default_data)
    }
    if request.method == 'POST':
        user_creation_form_2 = CustomUserCreationForm2(data=request.POST)
        if user_creation_form_2.is_valid():
            user_creation_form_2.save()
    return render(request, 'registrarUsuario.html', data)

def edicionusuario(request, username):

    usuario = Usuario.objects.get(username=username)

    return render(request, 'edicionUsuarios.html', {"usuario":usuario})

def editarusuario(request):

    username = request.POST['username']
    first_name = request.POST['txtNombres']
    last_name = request.POST['txtApellidos']
    email = request.POST['email']

    usuario = Usuario.objects.get(username=username)
    usuario.first_name = first_name
    usuario.last_name = last_name
    usuario.email = email

    usuario.save()

    messages.success(request, 'Se ha editado con exito el usuario seleccionado')

    if request.user.is_superuser:
        return redirect('usuarios')
    else:
        return redirect('inicio')

def eliminarusuario(request, username):
    
    usuario = Usuario.objects.get(username=username)

    usuario.delete()

    messages.success(request, 'Se ha eliminado el usuario seleccionado')

    return redirect('usuarios')

def posts(request):
    if request.user.is_superuser or request.user.categoria == 'Colaborador':
        postslistados = Post.objects.all()
    categoriaslistadas = Categoria.objects.all()
    return render(request, 'posts.html', {"postslistados" : postslistados, "categoriaslistadas" : categoriaslistadas})

def registrarpost(request):

    titulo = request.POST['txtTitulo']
    slug = request.POST['txtSlug']
    descripcion = request.POST['txtDescripcion']
    contenido = request.POST['txtContenido']
    imagen = request.POST['txtImagen']
    autor = request.user
    categoria = request.POST['categoria']
    categoria = Categoria.objects.get(id=categoria)
    estado = True

    post = Post.objects.create(titulo=titulo, slug=slug, descripcion=descripcion, contenido=contenido, imagen=imagen, autor= autor, categoria=categoria, estado=estado)

    messages.success(request, 'Se ha registrado un post')

    return redirect('posts')

def edicionpost(request, id):

    post = Post.objects.get(id=id)

    return render(request, 'edicionPost.html', {"post":post})

def editarpost(request):

    id = request.POST['numberid']
    titulo = request.POST['txtTitulo']
    slug = request.POST['txtSlug']
    descripcion = request.POST['txtDescripcion']
    contenido = request.POST['txtContenido']
    imagen = request.POST['txtImagen']

    post = Post.objects.get(id=id)
    post.titulo = titulo
    post.slug = slug
    post.descripcion = descripcion
    post.contenido = contenido
    post.imagen = imagen

    post.save()

    messages.success(request, 'Se ha editado con exito el post seleccionado')

    return redirect('posts')

def eliminarpost(request, id):
    
    post = Post.objects.get(id=id)

    post.delete()

    messages.success(request, 'Se ha eliminado el post seleccionado')

    return redirect('posts')

def register(request):
    default_data = {'categoria': 'Registrado'}
    data = {
        'form' : CustomUserCreationForm(initial=default_data)
    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('inicio')
    return render(request, 'registration/register.html', data)

class ResetPassword(PasswordResetView):
    template_name = 'registration/resetPassword.html'

class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'registration/passwordDone.html'

class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = 'registration/passwordConfirm.html'

class ResetPasswordComplete(PasswordResetCompleteView):
    template_name = 'registration/passwordComplete.html'