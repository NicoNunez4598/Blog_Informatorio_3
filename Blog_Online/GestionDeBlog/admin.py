from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria

class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario

class CategoriaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [ 'nombre' ]
    list_display = [ 'nombre', 'estado', 'fecha_creacion', ]
    resource_class = CategoriaResource

class UsuarioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = [ 'first_name', 'last_name', 'email' ]
    list_display = [ 'first_name', 'last_name', 'email', 'username', 'is_staff' ]
    resource_class = UsuarioResource

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Post)
admin.site.register(Comentario)