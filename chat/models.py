from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    participants = models.ManyToManyField(
        to=User, related_name="rooms", verbose_name="Участники"
    )
    name = models.CharField("Название комнаты", max_length=150)
    room_name = models.SlugField("Слаг комнаты", max_length=150, unique=True)
    created_at = models.DateTimeField(
        "Дата создания комнаты", auto_now_add=True
    )

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Комната",
    )
    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Отправитель",
    )
    content = models.TextField("Текст сообщения")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Последнее обновление", auto_now=True)
    is_seen = models.BooleanField("Прочитано", default=False)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["-created_at"])]

    def __str__(self):
        return f"Author {self.sender.username} - Room {self.room.name}"
