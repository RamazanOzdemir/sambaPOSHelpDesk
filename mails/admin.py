from django.contrib import admin
from .models import Person,LastMessage,attachments,Message,MessageBlock


admin.site.register(Person)
admin.site.register(attachments)
admin.site.register(MessageBlock)
admin.site.register(Message)
admin.site.register(LastMessage)

