from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, FormView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.db.models import Count, Q
from django.utils import timezone

from .forms import RegisterUserForm, LoginUserForm, JoinEventForm, ContactForm
from .models import Event, Registration, Category

# View for the Homepage
class HomeView(ListView):
    model = Event
    template_name = 'general/home.html'
    context_object_name = 'events'

    # Method that classifies the events per categories
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding categories to the context
        context['categories'] = Category.objects.annotate(event_count=Count('events') # 'events' is the related_name we put in models
        )
        return context

    # Method that helps finding an event with a word
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Event.objects.all().order_by('-start_datetime')
        
        if query:
            # Trying to find a word that contains the word on the title or locations            
            object_list = object_list.filter(
                Q(title__icontains=query) | Q(location__icontains=query)
            )
        return object_list


# View to Login Users
class UserLoginView(FormView):
    form_class = LoginUserForm
    template_name = 'general/login.html'
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user_found = authenticate(self.request, username=username, password=password)

        if user_found is not None:
            login(self.request, user_found)
            messages.info(self.request, f'Welcome {user_found.username} 🙌')
            return redirect('home')
        else:
            messages.error(self.request, 'User or password wrong ❌')
            return self.form_invalid(form)


# View for logout
def logout_view(request):
    username = request.user.username
    logout(request)
    messages.info(request, f'Goodbye {username}👋 ​')
    return redirect('home')


# View to Register users
class RegistrationUserView(FormView):
    form_class = RegisterUserForm
    template_name = 'general/register.html'
    success_url = reverse_lazy('home')

    # Login the user automatically
    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f'Welcome to Falcon Events, {user.username}! Your account has been succesfully created.')
        login(self.request, user)
        return super().form_valid(form)


# View to list all Events
class EventListView(ListView):
    model = Event
    template_name = 'general/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# View to check the details of an Event
class EventDetailView(DetailView):
    model = Event
    template_name = 'general/event_detail.html'
    context_object_name = 'event'


# Protected view for joining an event
class JoinEventView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form = JoinEventForm(request.POST)
        
        if form.is_valid():
            num_guests = form.cleaned_data['guests']
            total_requested = 1 + num_guests # User + guests

        # Space enough?
        if total_requested > event.slots_left:
            messages.error(request, f"Sorry, there are only {event.slots_left} spaces left.")
            return redirect('event_detail', pk=pk)

        # Already registered?
        if Registration.objects.filter(user=request.user, event=event).exists():
            messages.warning(request, "You already join this event!")
        else:
            Registration.objects.create(user=request.user, event=event, guests=num_guests)
            messages.success(request, f"Cool, you joined the event with {num_guests} guests!. We sent you an email with the confirmation.")
        
        return redirect('my_events')


# CCBV to filter per category
class CategoryDetailView(ListView):
    model = Event
    template_name = 'general/event_list.html' # Reusing this template
    context_object_name = 'events'

    def get_queryset(self):
        # Applying the filter on the events with the slug of the category in the URL
        return Event.objects.filter(category__slug=self.kwargs['slug'])


# CCBV to check a list of the events
class MyEventsViews(LoginRequiredMixin, ListView): # LoginRequiredMixin doesn't allow anyone if not registered
    model = Registration
    template_name = 'general/my_events.html'
    context_object_name = 'registrations'

    def get_queryset(self):
        # The user is only allowed to see the events he joined
        return Registration.objects.filter(
            user=self.request.user
        ).select_related('event').order_by('-registered_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # Filtering the user's register
        user_regs = Registration.objects.filter(user=self.request.user).select_related('event')
        
        # Classifying the date of event
        context['upcoming_events'] = user_regs.filter(event__start_datetime__gte=now).order_by('event__start_datetime')
        context['past_events'] = user_regs.filter(event__start_datetime__lt=now).order_by('-event__start_datetime')
        
        return context


# CCBV to cancel registration on Events
class CancelRegistrationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Finding the ID of the Registration
        registration = get_object_or_404(Registration, pk=pk, user=request.user)
        event_title = registration.event.title
        registration.delete()
        
        messages.success(request, f"You have successfully cancelled your registration for {event_title}.")
        return redirect('my_events')


# Method for the Calendar
class CalendarView(TemplateView):
    template_name = 'general/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.all()
        return context


# Method for the Contact View
class ContactView(FormView):
    template_name = 'general/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for your message, we will contact you shortly  🚀')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was a mistake with the form, please check the fields.')
        return super().form_invalid(form)