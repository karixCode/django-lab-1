from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .forms import RegisterForm, UpdateForm
from .models import Question, Choice, User
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import logout

class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('polls:login')

class Profile(generic.DetailView):
    model = User
    template_name = 'polls/profile.html'

class DeleteUser(generic.DeleteView):
    model = User
    success_url = reverse_lazy('polls:index')

def logout_view(request):
    logout(request)
    return redirect('polls:index')

class UpdateUser(generic.UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other_user = User.objects.get(pk=self.kwargs['pk'])
        if self.request.user.pk != other_user.pk:
            raise Http404

        return context

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quest = Question.objects.get(pk=self.kwargs['pk'])
        if not quest.was_published_recently() and not self.request.user.is_superuser:
            raise Http404

        return context

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if not request.user.is_authenticated:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не вошли в аккаунт',
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор',
        })

    if question.voted_by.filter(id=request.user.id).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы уже приняли участие в голосовании',
        })

    question.voted_by.add(request.user)

    selected_choice.votes += 1
    selected_choice.save()
    question.votes += 1
    question.save()

    return redirect(reverse('polls:results', args=(question.id,)))