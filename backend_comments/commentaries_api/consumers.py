from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "comments"
        self.room_group_name = "comments_list"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        parent = text_data_json['parent']
        id = text_data_json['id']
        user_name = text_data_json['user_name']
        to_delete = text_data_json['to_delete']
        date_published = text_data_json['date_published']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "comment_send",
                'content': content,
                'parent': parent,
                'id': id,
                'date_published': date_published,
                'to_delete': to_delete,
                'user_name': user_name

            }
        )

    async def comment_send(self, event):
        content = event['content']
        parent = event['parent']
        id = event['id']
        user_name = event['user_name']
        to_delete = event['to_delete']
        date_published = event['date_published']
        await self.send(text_data=json.dumps({
            'content': content,
            'parent': parent,
            'id': id, 
            'date_published': date_published,
            'to_delete': to_delete,
            'user_name': user_name
        },
        ensure_ascii=False))
    


# class AnswerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = "answers"
#         self.room_group_name = "answers_list"
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         content = text_data_json['content']
#         parent = text_data_json['parent']
#         id = text_data_json['id']
#         date_published = text_data_json['date_published']
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "comment_send",
#                 'content': content,
#                 'parent': parent,
#                 'id': id,
#                 'date_published': date_published

#             }
#         )

#     async def comment_send(self, event):
#         content = event['content']
#         parent = event['parent']
#         id = event['id']
#         date_published = event['date_published']
#         await self.send(text_data=json.dumps({
#             'content': content,
#             'parent': parent,
#             'id': id, 
#             'date_published': date_published
#         },
#         ensure_ascii=False))