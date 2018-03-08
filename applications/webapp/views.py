from django.shortcuts import render
from django.views import generic

from applications.tales import models as tales_models
# Create your views here.


class AuthorsList(generic.ListView):
    template_name = "webapp/authors_list.html"
    queryset = tales_models.Author.objects.all()
    context_object_name = "authors"


class TalesListByAuthor(generic.ListView):
    template_name = "webapp/tales_list.html"
    context_object_name = "tales"

    def get_queryset(self):
        return tales_models.Tale.objects.filter(author__id=self.kwargs.get('author_id', 0))


class App(generic.TemplateView):
    template_name = "webapp/app.html"

    def get_context_data(self, **kwargs):
        context = super(App, self).get_context_data(**kwargs)

        sentences = tales_models.TaleSentence.objects.filter(tale__id=self.kwargs.get('tale_id', 0)).order_by("id")
        if sentences:
            context['initial_sentence'] = sentences[0].id-1
            context['final_sentence'] = sentences[sentences.count()-1].id

        print(context)

        return context