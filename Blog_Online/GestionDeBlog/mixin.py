from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

def categoria_required(categoria):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or getattr(request.user, 'categoria', None) != categoria:
                messages.error(request, 'No tienes permiso para acceder a esta sección.')
                return redirect('inicio')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator