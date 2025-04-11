from django.contrib import admin
from .models import SimulatorCategory, SimulatorType, Simulators


admin.site.register(Simulators)
admin.site.register(SimulatorType)
admin.site.register(SimulatorCategory)

