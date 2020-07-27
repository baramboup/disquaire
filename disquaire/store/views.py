from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Album, Artist, Contact, Booking 
from .forms import ContactForm

# Create your views here.
def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {'albums': albums}
    return render(request, 'store/index.html', context)


def detail(request, album_id):
    id = int(album_id) # make sure we have an integer.
    album = get_object_or_404(Album, pk=id)
    artists_name = ", ".join([artist.name for artist in album.artists.all()])
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            email=request.POST.get('email')
            form=Contact.objects.filter(email=email).get()    

        booking = Booking(
                contact=form,
                album=album
                ).save()
        album.available=False
        album.save()
        context={'booking':booking}
        return render(request, 'store/merci.html', context)    
                
    else:
        form = ContactForm()
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture,
        'form': form 
    }

    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET.get('query')
    title = request.GET.get('title')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__contains=query)
 
    title = "Resultats pour la requete %s"%query
    context = {
        'albums': albums,
        'title': title
    }         
    return render(request, 'store/search.html', context)   


def listing(request) :
    albums_list = Album.objects.all()
    paginator = Paginator(albums_list,2)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    context = {
        'albums': albums,
    }         
    return render(request, 'store/listing.html', context)