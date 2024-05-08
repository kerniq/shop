from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage
from .forms import UserBioForm, UploadFileForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:

    message = ''
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES["myfile"]
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            if myfile.size < 1_048_576:
                filename = fs.save(myfile.name, myfile)
                print('saved file', filename)
                message = 'saved file'
            else:
                message = 'size of file over 1MB'
    else:
        form = UploadFileForm()

    context = {
        'message': message,
        'form': form
    }

    return render(request, "requestdataapp/file-upload.html", context=context)
