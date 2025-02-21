from django.contrib import admin
from .models import *

admin.site.register(Pessoa)
admin.site.register(Funcionario)
admin.site.register(EPI)
admin.site.register(EntregaEpi)
admin.site.register(DevolverEpi)


