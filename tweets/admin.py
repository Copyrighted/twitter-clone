from django.contrib import admin

# Register your models here.
from .models import Tweet

class TweetAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']

    # def __str__(self):
    #     return self.content #can display content for tweets

    class Meta:
        model = Tweet

admin.site.register(Tweet, TweetAdmin)

