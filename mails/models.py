from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class Person (models.Model):
    objects = models.Manager()
    COLOR_CHOICES = [
        ('#e53935', 'Kırmızı'),
        ('#1976d2', 'Mavi'),
        ('#00796b', 'Yeşil'),
        ('#ffeb3b', 'Sarı'),
        ('#f4511e', 'Turuncu'),
        ('#546e7a', 'Gri'),
        ('#5e35b1', 'Mor'),
    ]
    uid = models.CharField(max_length=50,default=uuid.uuid4())
    person = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50,default='')
    personColor = models.CharField(max_length=15,choices=COLOR_CHOICES,default='#1976d2',)
    is_Super_Person = models.BooleanField(default=False)
    wait_to_reply = models.ManyToManyField('MessageBlock', related_name='incomingemails',blank=True)
    position = models.CharField(max_length=30,default='')

    def __str__(self):
        self.full_name=("{} {}".format(self.first_name.capitalize(), self.last_name.capitalize()))
        return self.full_name
    def avatar(self):
        return ("{} {}".format(self.first_name[0], self.last_name[0])).upper()



class MessageBlock(models.Model):
    objects = models.Manager()
    uid = models.CharField(max_length=50, default=uuid.uuid4())
    subject = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=100)
    tag = models.ManyToManyField('Tag',related_name='tag',blank=True)
    messages = models.ManyToManyField('Message',related_name='messages')
    reply_persons = models.ManyToManyField('Person', related_name='name_persons',blank=True)
    date = models.DateTimeField(auto_now=False, default=datetime(1990, 1, 1))

    class Meta:
        ordering = ['date']
    def __str__(self):
        return self.subject


class Message(models.Model):
    objects = models.Manager()
    message_type = models.CharField(max_length=50)
    uid = models.CharField(max_length=50)
    subject = models.CharField(max_length=250)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    body_plain = models.TextField()
    body_html = models.TextField()
    date = models.DateTimeField(auto_now=False)
    person = models.ManyToManyField('Person', related_name='name_person',blank=True)
    mail_attachments = models.ManyToManyField('attachments',blank=True)



    def __str__(self):
        return self.subject


class attachments(models.Model):
    objects = models.Manager()
    file = models.FileField()


class LastMessage(models.Model):
    objects = models.Manager()
    date = models.DateTimeField(default=datetime(1990,1,1 ))

    def __str__(self):
        return str(self.date)


class Tag(models.Model):
    objects = models.Manager()
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.tag_name)