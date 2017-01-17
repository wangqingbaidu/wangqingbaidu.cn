from django.contrib import admin
from vmaig_system.models import Notification, Link

# Register your models here.


class NotificationAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('title', 'from_user', 'to_user', 'create_time')
    list_filter = ('create_time',)
    fields = ('title', 'is_read', 'text',
              'url', 'from_user', 'to_user', 'type')


class LinkAdmin(admin.ModelAdmin):
#     use var name in models to specify the object to display 
#     fileds specifies the add method, list_dispaly specifies the view method, list_filter specifies the filter of the list
    search_fields = ('title',)
    list_display = ('title', 'url', 'create_time')
    list_filter = ('create_time',)
    fields = ('title', 'url', 'type')


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Link, LinkAdmin)
