import base64

from captcha.image import ImageCaptcha
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CaptchaProvider(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        width = int(self.request.query_params.get('width'))
        height = int(self.request.query_params.get('height'))

        image = ImageCaptcha(
            width=width,
            height=height,
            fonts=[
                '/home/maedeh/Documents/Codes/Django/captcha_provider_workspace/captcha_provider/fonts/B-NAZANIN.TTF',
            ])

        # Image captcha text
        captcha_text = 'همطاف'

        # generate the image of the given text
        data = image.generate(captcha_text)

        # write the image on the given file and save it
        image.write(captcha_text, 'CAPTCHA.png')
        with open('CAPTCHA.png', "rb") as img_file:
            my_string = base64.b64encode(img_file.read())

        return Response(data=my_string.decode('utf-8'), status=status.HTTP_200_OK)