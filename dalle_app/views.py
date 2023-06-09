from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from PIL import Image
from io import BytesIO
import openai
import requests
import os
from dotenv import load_dotenv
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .form import ContactForm

load_dotenv()  

openai.api_key = os.environ.get('OPENAI_API_KEY')

#OpenAI API를 통한 이미지 생성 요청함수
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        model="image-alpha-001"
    )

    image_url = response['data'][0]['url']
    image_data = requests.get(image_url).content

    return Image.open(BytesIO(image_data))

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

#클라이언트의 자바스크립트를 통해 서버로 제출된 Input 값을 generate_image 함수에 전달하여 클라이언트에 이미지를 반환함
def create_image(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt', '')
        image = generate_image(prompt)
        response = HttpResponse(content_type="image/png")
        image.save(response, "PNG")
        return response
    return HttpResponse(status=400)

def progress(request):
    progress_value = 100
    return JsonResponse({"progress": progress_value})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(
                subject,
                f"Name: {name}\nEmail: {email}\n\n{message}",
                email,
                ['kimdan5397@gmail.com'], # 대상 이메일 주소 입력
                fail_silently=False,
            )
            return redirect('contact_done')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})