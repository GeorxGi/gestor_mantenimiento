#
# ARCHIVO QUE PERMITE ASIGNAR FACILMENTE RUTAS A LAS VISTAS DE LA APLICACION
# ELIMINANDO LA NECESIDAD DE REPETIR CODIGO EN EL MAIN
#

import flet as ft

_views_registry = {}

def register_view(route: str):
    """Decorador para registrar vistas"""
    def decorator(view_class):
        if route in _views_registry:
            raise ValueError(f"La ruta '{route}' ya está registrada")
        _views_registry[route] = view_class
        return view_class
    return decorator

def get_view(page: ft.Page, route: str):
    """Obtiene una vista construida para la ruta especificada"""
    view_class = _views_registry.get(route)
    if view_class is None:
        return None
    return view_class(page).build()

def debug_routes():
    """Muestra las rutas registradas (para diagnóstico)"""
    print("Rutas registradas:")
    for route, view in _views_registry.items():
        print(f"- {route}: {view.__name__}")