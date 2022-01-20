import base64
from pathlib import Path

from captcha.image import ImageCaptcha
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CaptchaProvider(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        width = int(self.request.data.get('width'))
        height = int(self.request.data.get('height'))
        captcha_text = self.request.data.get('text')
        is_reveresed = self.request.data.get('is_reveresed')
        language = self.request.data.get('language')
        font = self.request.data.get('font') + ".TTF"

        image = ImageCaptcha(
            width=width,
            height=height,
            fonts=[
                r'/home/maedeh/Documents/Codes/Django/captcha_provider_workspace/captcha_provider/fonts/{font_name}'.format(
                    font_name=font),
            ])

        # Image captcha text
        captcha_text = captcha_text[::-1] if not is_reveresed else captcha_text

        # generate the image of the given text
        data = image.generate(captcha_text)

        # write the image on the given file and save it
        image.write(captcha_text, 'CAPTCHA.png')
        with open('CAPTCHA.png', "rb") as img_file:
            my_string = base64.b64encode(img_file.read())

        return Response(data=
        {
            'data': my_string.decode('utf-8')
        }, status=status.HTTP_200_OK)
