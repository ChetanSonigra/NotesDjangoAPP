from django.shortcuts import render

from Note.forms import NotesForm

from .models import Notes
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class NotesDeleteView(LoginRequiredMixin,DeleteView):
    model = Notes
    success_url = '/smart/notes'
    template_name = 'Note/notes_delete.html'
    login_url = "/login"

class NotesUpdateView(LoginRequiredMixin,UpdateView):
    model= Notes
    success_url= '/smart/notes'
    form_class = NotesForm
    context_object_name = 'note'
    login_url = "/login"
class NotesCreateView(LoginRequiredMixin,CreateView):
    model= Notes
    form_class = NotesForm
    template_name = 'Note/notes_form.html'
    success_url = '/smart/notes'
    login_url = "/login"
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'Note/notes_list.html'
    login_url = "/login"
    def get_queryset(self):
        return self.request.user.Notes.all()
class NotesDetailView(LoginRequiredMixin,DetailView):
    model = Notes
    template_name = 'Note/notes_detail.html'
    context_object_name = 'note'
    login_url = "/login"

def list(request):
    all_notes = Notes.objects.all()
    return render(request, 'Note/notes_list.html',{'notes': all_notes})

def details(request,pk):
    try:
        note = Notes.objects.get(pk=pk)
    except Notes.DoesNotExist:
        raise Http404("note does not exist.")
    return render(request,'Note/notes_detail.html',{'note': note})
