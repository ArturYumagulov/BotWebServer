from django.shortcuts import render
from urllib.parse import quote_plus
# Create your views here.
import base64
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import VCard


def whatsapp_share_link(vcard):
    # Формируем ссылку на WhatsApp с сообщением и ссылкой на vCard
    vcard_url = "https://service.tranzit-oil.com/contacts/vcard/{}/download/".format(vcard.pk)  # URL для скачивания vCard
    message = f"Сохраните этот контакт: {vcard.full_name} - {vcard.phone_number} - {vcard.email}\nDownload vCard: {vcard_url}"
    return f"https://wa.me/?text={quote_plus(message)}"



# Функция для создания ссылки Telegram
def telegram_share_link(vcard):
    # Формируем ссылку для Telegram с сообщением и ссылкой на vCard
    vcard_url = f"https://service.tranzit-oil.com/contacts/vcard/{vcard.pk}/download/" # URL для скачивания vCard
    message = f"Сохраните этот контакт: {vcard.full_name} - {vcard.phone_number} - {vcard.email}\nDownload vCard: {vcard_url}"
    return f"https://t.me/share/url?url={quote_plus(vcard_url)}&text={quote_plus(message)}"


def download_vcard_with_photo(request, pk):
    vcard = get_object_or_404(VCard, pk=pk)
    # Преобразование изображения в base64
    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_base64 = image_to_base64(vcard.photo.path)  # Путь к изображению

    # Формируем данные vCard с фото
    vcard_data = f"""BEGIN:VCARD
VERSION:3.0
N;CHARSET=utf-8:{vcard.full_name}
FN;CHARSET=utf-8:{vcard.full_name}
TEL;TYPE=CELL:{vcard.phone_number}
EMAIL;TYPE=INTERNET:{vcard.email}
ADR;TYPE=WORK:{vcard.address.full_address}
GEO:{vcard.address.coordinates}
PHOTO;ENCODING=BASE64;TYPE=JPEG:{image_base64}
    """
    if vcard.company:
        vcard_data += f"ORG;CHARSET=utf-8:{vcard.company}\n"
    if vcard.job_title:
        vcard_data += f"TITLE;CHARSET=utf-8:{vcard.job_title} {vcard.company}\n"
    if vcard.website:
        vcard_data += f"URL:{vcard.website}\n"

    vcard_data += "END:VCARD"

    # Создаем HttpResponse с нужным типом контента
    response = HttpResponse(vcard_data, content_type="text/vcard")
    response['Content-Disposition'] = f'attachment; filename="{vcard.full_name}.vcf";filename*=UTF-8"{vcard.full_name}.vcf"'


    return response


def index(request, email):
    vcard = get_object_or_404(VCard, email=email)
    whatsapp_link = whatsapp_share_link(vcard)
    telegram_link = telegram_share_link(vcard)
    return render(request, 'vcard_detail.html', {
        'vcard': vcard,
        'whatsapp_link': whatsapp_link,
        'telegram_link': telegram_link,
    })
