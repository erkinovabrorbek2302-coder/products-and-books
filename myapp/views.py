from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.http import JsonResponse
from .models import Maqola, Mahsulot, Comments
from myapp.forms import CommentForm, EmailPostForm
from django.core.mail import send_mail
from django.views import generic


def login_required_decorator(func):
    return login_required(func, login_url='/login/')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('/login/')


def login_page(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')


@login_required_decorator
def home(request):
    return render(request, 'home.html', {
        'maqolalar_soni': Maqola.objects.count(),
        'mahsulotlar_soni': Mahsulot.objects.count(),
        'izohlar_soni': Comments.objects.count(),
        'son_maqolalar': Maqola.objects.all()[:8],
        'son_mahsulotlar': Mahsulot.objects.all()[:8],
        'son_izoh': Comments.objects.filter(active=True).order_by('-created').first(),
    })


@login_required_decorator
def izohlar_list(request):
    izohlar = Comments.objects.filter(active=True).order_by('-created')
    return render(request, 'izohlar_list.html', {'izohlar': izohlar})


@login_required_decorator
def maqola_list(request):
    maqolalar = Maqola.objects.all()
    return render(request, 'maqola_list.html', {'maqolalar': maqolalar})


@login_required_decorator
def maqola_detail(request, pk):
    maqola = get_object_or_404(Maqola, pk=pk)
    comments = maqola.comments.filter(active=True)
    new_comment = None
    error_message = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            email = comment_form.cleaned_data['email']
            # ✅ Tekshirish: bu email allaqachon izoh qoldirganmi?
            if Comments.objects.filter(maqola=maqola, email=email).exists():
                error_message = "Siz bu maqolaga allaqachon izoh qoldirgansiz!"
            else:
                new_comment = comment_form.save(commit=False)
                new_comment.maqola = maqola
                new_comment.save()
                return redirect('myapp:maqola_detail', pk=maqola.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'maqola_detail.html', {
        'maqola': maqola,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment,
        'error_message': error_message,  # ✅ Xatolik xabari
    })


@login_required_decorator
def mahsulot_list(request):
    mahsulotlar = Mahsulot.objects.all()
    return render(request, 'mahsulot_list.html', {'mahsulotlar': mahsulotlar})


@login_required_decorator
def mahsulot_detail(request, pk):
    mahsulot = get_object_or_404(Mahsulot, pk=pk)
    return render(request, 'mahsulot_detail.html', {'mahsulot': mahsulot})


@login_required_decorator
def maqola_search(request):
    qidiruv = request.GET.get('nom', '')
    if qidiruv:
        natijalar = Maqola.objects.filter(nom__icontains=qidiruv)
    else:
        natijalar = Maqola.objects.all()
    return render(request, 'maqola_search.html', {'natijalar': natijalar, 'qidiruv': qidiruv})


@login_required_decorator
def api_maqolalar(request):
    maqolalar = Maqola.objects.all()
    date = []
    for maqola in maqolalar:
        date.append({
            'id': maqola.pk,
            'nom': maqola.nom,
            'muallifi': maqola.muallifi,
            'sarlavha': maqola.sarlavha,
            'tavsif': maqola.tavsif,
        })
        return JsonResponse(date, safe=False)


@login_required_decorator
def post_share(request, post_id):
    post = get_object_or_404(Maqola, id=post_id, holat='chop_etilgan')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)

            post_url = request.build_absolute_uri(post.get_absolute_url())
            sarlavha = f"{cd['name']} sizga {post.sarlavha} ni o'qishni taklif qildi."
            xabar = (
                f"Read {post.sarlavha} at {post_url}\n\n"
                f"{cd['name']}'s comment: {cd['comments']}"
            )

            send_mail(
                sarlavha,
                xabar,
                'erkinovabrorbek.2302@gmail.com',
                [cd['to']],
                fail_silently=False
            )
            sent = True
    else:
        form = EmailPostForm()

    # ✅ SHU QATORNI IF DAN TASHQARIGA CHIQARING!
    return render(request, 'post_share.html', {
        'post': post,
        'sent': sent,
        'form': form
    })


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('myapp:login_page')
    template_name = 'signup.html'
