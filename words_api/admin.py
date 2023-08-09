from django.contrib import admin
from .models import Word
from .models import Statistic
from .models import RateLimiter

# Register your models here.
admin.site.register(Word)
admin.site.register(Statistic)
admin.site.register(RateLimiter)
