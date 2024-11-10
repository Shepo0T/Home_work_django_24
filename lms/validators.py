from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = value.get(self.field)
        if video_url and not video_url.startswith('https://www.youtube.com/'):
            raise ValidationError('Ссылка допустима только на видеоматериалы из Youtube')