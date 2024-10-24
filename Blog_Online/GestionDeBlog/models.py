from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Categoria(models.Model):
    
    id = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre de la Categoria', max_length=100, null=False, blank=False)
    estado = models.BooleanField('Categoria Activa / Categoria Desactivada', default=True)
    fecha_creacion = models.DateField('Fecha de Creacion', auto_now=False, auto_now_add=True)

    class Meta:

        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
    
    def __str__(self):
        
        return self.nombre

class Usuario(AbstractUser):

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    @property
    def nombre(self):
        return self.first_name
    
    @property
    def apellido(self):
        return self.last_name
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Post(models.Model):

    id = models.AutoField(primary_key=True)
    titulo = models.CharField('Titulo', max_length=150, blank=False, null=False)
    slug = models.CharField('Slug', max_length=100, blank=False, null=False)
    descripcion = models.CharField('Descripcion', max_length=255, blank=False, null=False)
    contenido = RichTextField()
    imagen = models.URLField(max_length=255, blank=False, null=False)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    estado = models.BooleanField('Publicado / No Publicado', default=True)
    fecha_creacion = models.DateField('Fecha de Creacion', auto_now=False, auto_now_add=True)

    class Meta:

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        
        return self.titulo

class Comentario(models.Model):
    
    id = models.AutoField(primary_key=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contenido = models.CharField('Contenido', max_length=200, blank=False, null=False)
    fecha_creacion = models.DateField('Fecha de Creacion', auto_now=False, auto_now_add=True)

    class Meta:

        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'