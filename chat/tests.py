from rest_framework import status
from rest_framework.test import APITestCase


class ChatCrudApiTests(APITestCase):
    def test_chat_crud_flow(self):
        ko_response = self.client.post(
            "/api/chat/languages/",
            {"code": "ko", "name": "Korean", "native_name": "한국어"},
            format="json",
        )
        de_response = self.client.post(
            "/api/chat/languages/",
            {"code": "de", "name": "German", "native_name": "Deutsch"},
            format="json",
        )

        self.assertEqual(ko_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(de_response.status_code, status.HTTP_201_CREATED)

        minsu_response = self.client.post(
            "/api/chat/users/",
            {
                "email": "minsu@example.com",
                "password": "password",
                "nickname": "민수",
                "preferred_language_code": "ko",
            },
            format="json",
        )
        hans_response = self.client.post(
            "/api/chat/users/",
            {
                "email": "hans@example.com",
                "password": "password",
                "nickname": "Hans",
                "preferred_language_code": "de",
            },
            format="json",
        )

        self.assertEqual(minsu_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(hans_response.status_code, status.HTTP_201_CREATED)

        minsu_id = minsu_response.data["id"]
        hans_id = hans_response.data["id"]

        room_response = self.client.post(
            "/api/chat/rooms/",
            {
                "room_type": "DM",
                "title": "민수와 Hans의 번역 채팅",
                "created_by": minsu_id,
            },
            format="json",
        )
        self.assertEqual(room_response.status_code, status.HTTP_201_CREATED)
        room_id = room_response.data["id"]

        for user_id, language_code in [(minsu_id, "ko"), (hans_id, "de")]:
            member_response = self.client.post(
                "/api/chat/members/",
                {
                    "chat_room": room_id,
                    "user": user_id,
                    "display_language_code": language_code,
                },
                format="json",
            )
            self.assertEqual(member_response.status_code, status.HTTP_201_CREATED)

        message_response = self.client.post(
            "/api/chat/messages/",
            {
                "chat_room": room_id,
                "sender": minsu_id,
                "original_language_code": "ko",
                "original_content": "안녕! 오늘 독일 날씨 어때?",
                "message_type": "TEXT",
            },
            format="json",
        )
        self.assertEqual(message_response.status_code, status.HTTP_201_CREATED)
        message_id = message_response.data["id"]

        translation_response = self.client.post(
            "/api/chat/translations/",
            {
                "message": message_id,
                "target_language_code": "de",
                "translated_content": "Hallo! Wie ist das Wetter heute in Deutschland?",
                "translation_status": "DONE",
                "provider": "Dummy",
            },
            format="json",
        )
        self.assertEqual(translation_response.status_code, status.HTTP_201_CREATED)

        list_response = self.client.get("/api/chat/messages/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

        patch_response = self.client.patch(
            "/api/chat/languages/ko/",
            {"native_name": "한국어"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        temp_language_response = self.client.post(
            "/api/chat/languages/",
            {"code": "en", "name": "English", "native_name": "English"},
            format="json",
        )
        self.assertEqual(temp_language_response.status_code, status.HTTP_201_CREATED)

        delete_response = self.client.delete("/api/chat/languages/en/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
