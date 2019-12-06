from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from imbox import Imbox
from .models import Person, LastMessage, attachments, Message, MessageBlock
from datetime import datetime
import timeinterval


class MailConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.room_group_name = 'chat_%s' % self.room_name
        self.mail_group_name = 'new_mail_coming'

        # Join room group
        await self.channel_layer.group_add(
            self.mail_group_name,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.mail_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def ccc(self,event):
        while True:
            await asyncio.sleep(2)
            await self.send(text_data=json.dumps({
            'message': 'message'
        }))

    async def new_coming(self,event):
        async def call():
            print("websocet contect kurdu ve 100 sn bir new message istiyor!!!")
            imbox = Imbox('imap.gmail.com',
                          username='dene6606@gmail.com',
                          password='Kartal1903',
                          ssl=True,
                          ssl_context=None,
                          starttls=False)
            last_message = MessageBlock.objects.last()
            ll = LastMessage.objects.all()[0]

            if last_message != None:
                ll.date = last_message.date
                ll.save()
            last_message_date = ll.date
            print(last_message_date, "consemer içinden son mesaj zamanı")
            all_inbox_messages = imbox.messages(date__gt=last_message_date)
            new_messages = []
            instance_new_messages = []
            for uid, message in all_inbox_messages:
                d = message.date.replace('(GMT)', '').strip()
                date = datetime.strptime(d, '%a, %d %b %Y %H:%M:%S %z')
                if date > last_message_date:
                    # uid = message.message_id.replace('<','').replace('@mail.gmail.com>','')
                    subject = message.subject
                    my_attachments = message.attachments
                    print('*****************Sadece gelen mesaj öncekileri istemiyoruz************************')
                    cc = message.body['html'][0]
                    print(cc.partition("<br>"))
                    print('*****************************************')
                    instance = cc.partition('<br>')
                    only_coming_message = instance[0]
                    from_name = message.sent_from[0]['name']
                    from_email = message.sent_from[0]['email']
                    to_name = message.sent_to[0]['name']
                    to_email = message.sent_to[0]['email']
                    body_plain = message.body['plain'][0]
                    body_html = only_coming_message
                    date = date
                    incoming = Message(
                        message_type='incoming',
                        uid=uid,
                        subject=subject,
                        name=from_name,
                        email=from_email,
                        body_plain=body_plain,
                        body_html=body_html,
                        date=date,
                    )
                    # incoming.mail_attachments.add()
                    incoming.save()
                    new_messages.append(incoming)
                    instance_new_messages.append(incoming)
                    print('yenimail eklendi db-ye ve new_mails array ine eklendi eklendi')

            all_message_blocks = MessageBlock.objects.all()
            message_blocks = [[e.email, e.subject] for e in  all_message_blocks]
            print(message_blocks, "Query deneme")
            for message in new_messages:
                for message_block in all_message_blocks:
                    if message_block.messages.filter(subject='Re:{}'.format(message.subject),email=message.email).exists():
                        print('cevap message ı geldi')
                        instance_new_messages = [x for x in instance_new_messages if x != message]

            print(instance_new_messages,'Buda hiç bir messaga bloğunda olmayan mesagges')
            new_blocks = [
                MessageBlock(
                    subject=nw_blk.subject,
                    name=nw_blk.name,
                    email=nw_blk.email,
                    date=nw_blk.date
                )
                for nw_blk in instance_new_messages
            ]
            print(new_blocks,"news blocks listesi")
            for i in range(len(new_blocks)):
                new_blocks[i].save()
                new_blocks[i].messages.add(instance_new_messages[i])
            await self.send(text_data=json.dumps({
                'message': 'message'
            }))
#            reply_array = []
#            # my_incoming = []
#            # all_incoming = []
#            for mail in new_coming_message:
#                reply_persons = mail.reply_persons.all()
#                reply_p = serializers.serialize('json', reply_persons)
#                reply_array.append(reply_p)
#                for attach in my_attachments:
#                    print('#######################################')
#                    print(io.BytesIO(attach['content']))
#                    # atch = attachments(attach['filename'], attach['content'])
#                    # atch.save()
#                # if person in reply_persons:
#                #    my_incoming.append([mail,reply_persons])
#                # all_incoming.append([mail,reply_persons])
#       
#            new_msg = serializers.serialize('json', new_coming_message)
#            reply_json = json.dumps(reply_array)
#            data = {'reply': reply_json, 'new_msg': new_msg}
#            return JsonResponse(data)
        call()
        timeinterval.start(100000,call)