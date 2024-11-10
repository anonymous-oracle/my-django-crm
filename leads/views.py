from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Lead, Agent, Category
from . import forms
from . import utils
from agents import mixins

# Create your views here.

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = forms.CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    # queryset = Lead.objects.all() # the queryset of the model that has to be listed
    context_object_name = "leads" # this will rename the default context variable which is called as objects_list to leads

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False) # if organiser, fetches all the leads of that organisation based on the userprofile
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False) # if agent, then fetches the leads based on the particular agent organisation for the logged in user
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs) # simply demonstrates the ListView class's get method to handle requests
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            unassigned_leads = Lead.objects.filter(agent__isnull=True, organisation=user.userprofile) # unassigned leads of the user's organisation if the user is an organisor
            context.update({
                "unassigned_leads": unassigned_leads            
        })
        return context


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = "lead"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile) # if organiser, fetches all the leads of that organisation based on the userprofile
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation) # if agent, then fetches the leads based on the particular agent organisation for the logged in user
            queryset = queryset.filter(agent__user = user)
        return queryset

class LeadCreateView(mixins.OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = forms.LeadModelForm

    def post(self, request, *args, **kwargs):
        return super().post(self, request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse('leads:home')

    # this method was selected based on the method in super class of the CreateView
    def form_valid(self, form): # if form is valid an email will be sent
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        send_mail(subject="Lead created", message="Visit the website to view the changes",
                  from_email='test@test.com', recipient_list=['test2@test.com'])
        # this is how the form validation works
        return super(LeadCreateView, self).form_valid(form)

class LeadUpdateView(mixins.OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = forms.LeadModelForm

    def get_success_url(self) -> str:
        return reverse('leads:detail', kwargs={'pk':self.kwargs.get('pk')})
    
    def get_queryset(self) -> QuerySet[Any]:
        # allows update only for the organiser
        return Lead.objects.filter(organisation=self.request.user.userprofile) # if organiser, fetches all the leads of that organisation based on the userprofile

class LeadDeleteView(mixins.OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self) -> str:
        return reverse('leads:home')
    
    def get_queryset(self) -> QuerySet[Any]:
        # allows delete only for the organiser
        return Lead.objects.filter(organisation=self.request.user.userprofile)

class AssignAgentView(mixins.OrganiserAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = forms.AssignAgentForm

    def get_success_url(self):
        return reverse('leads:home')
    
    def get_form_kwargs(self):
        kwargs = super(AssignAgentView, self).get_form_kwargs()
        kwargs.update({
            # "pk": self.kwargs.get('pk'),
            "request": self.request # in the post request of the form, all kwargs that have been set here will be available
        })
        # kwargs.update(self.kwargs) # updating the get request kwargs

        # print(f"\n\nGET Form kwargs data:\n{self.kwargs}\n\n")

        return kwargs
    
    def form_valid(self, form: Any) -> HttpResponse:

        # print(f"\n\nForm cleaned data:\n{form.cleaned_data}\n\n")
        # print(f"\n\nPOST Form kwargs data:\n{self.get_form_kwargs()}\n\n")
        
        selected_agent = form.cleaned_data.get('agent')

        lead = Lead.objects.get(id=self.kwargs.get('pk')) # self.kwargs will contain the URL params that is sent across the request
        lead.agent = selected_agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset 
    
class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        if user.is_organiser:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset 
    
class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = forms.LeadCategoryUpdateForm

    def get_success_url(self) -> str:
        return reverse('leads:detail', kwargs={'pk':self.get_object().id})
    
    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        if user.is_organiser:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user = user)
        return queryset


    ########################################################################################################################################
    # commenting out the get_context_override for this view since the leads of the category being referred can be accessed from the template itself 
    ########################################################################################################################################

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
        
    #     # qs = Lead.object.filter(category=self.get_object()) # get_object() function returns the specific object that is currently being referred by the detail view; this is a special method which is a part of generic.DetailView

    #     qs = self.get_object().lead_set.all() # since category has a foreign key reference to leads it is a one to many relationship from category to leads, so since the model is Lead, we take the prefix to be 'lead' and then add 'set'; it is set because all foreign key references refer to unique leads


    #     context.update({
    #         "leads": qs
    #     })
    #     return context


def landing_page(request: HttpRequest):
    return render(request=request, template_name='landing.html')

def lead_list(request: HttpRequest):

    # context = {
    #     "name" : request.GET.get('name','anonymous')
    # }

    # return HttpResponse("Hello from home page")
    leads = Lead.objects.all()
    context = {"leads": leads}
    return render(
        request=request, template_name="leads/lead_list.html", context=context
    )


def second_home_page(request: HttpRequest):
    return render(request=request, template_name="second_page.html")


def lead_detail(request: HttpRequest, pk):
    lead = Lead.objects.get(id=pk)
    context = {"lead": lead}
    return render(
        request=request, template_name="leads/lead_detail.html", context=context
    )


# def lead_create(request: HttpRequest):
#     if request.method.lower() == 'post':
# form = forms.LeadForm(request.POST)
# if form.is_valid():
#     if not form.cleaned_data.get('agent'):
#         form.cleaned_data.update(agent = Agent.objects.first())
#     lead = Lead.objects.create(**form.cleaned_data)
#     lead.save()
#     return redirect('/leads')
#             # return HttpResponse(f"Created a lead for {form.cleaned_data.get('first_name')}")
#     elif request.method.lower() == 'get':
#         context = {
#             "form": forms.LeadForm()
#         }
#         return render(request=request, template_name='leads/lead_create.html', context = context)
#     else:
#         response = HttpResponse()
#         response.status_code = 404
#         response.content = "<h1>Not found</h1>"
#         return response


def lead_create(request: HttpRequest):
    if request.method.lower() == "post":
        post_data = request.POST.dict()
        form = forms.LeadModelForm(post_data)
        if form.is_valid():
            if not form.cleaned_data.get("agent"):
                agent = utils.assign_agent_for_lead()
                post_data.update(agent=agent)
                form = forms.LeadModelForm(post_data)
            form.save()  # for a model form, calling the .save() method after validation is sufficient to save the lead details
            return redirect("/leads")
            # return HttpResponse(f"Created a lead for {form.cleaned_data.get('first_name')}")
    elif request.method.lower() == "get":
        context = {"form": forms.LeadModelForm()}
        return render(
            request=request, template_name="leads/lead_create.html", context=context
        )
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "<h1>Not found</h1>"
        return response


# def lead_update(request: HttpRequest, pk):
#     if request.method.lower() == 'get':
#         lead = Lead.objects.get(id=pk)
#         context = {
#             'lead': lead,
#             'form': forms.LeadForm()
#         }
#         return render(request=request, template_name='leads/lead_update.html', context=context)
#     elif request.method.lower() == 'post':
#         form = forms.LeadForm(request.POST)
#         if form.is_valid():
#             if not form.cleaned_data.get('agent'):
#                 form.cleaned_data.update(agent = Agent.objects.first())
#             Lead.objects.filter(id=pk).update(**form.cleaned_data)
#         return redirect('/leads')
#     else:
#         response = HttpResponse()
#         response.status_code = 404
#         response.content = "<h1>Not found</h1>"
#         return response


def lead_update(request: HttpRequest, pk):

    lead = Lead.objects.get(id=pk)
    if request.method.lower() == "get":
        context = {"lead": lead, "form": forms.LeadModelForm(instance=lead)}
        return render(
            request=request, template_name="leads/lead_update.html", context=context
        )
    elif request.method.lower() == "post":
        form = forms.LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            if not form.cleaned_data.get("agent"):
                lead.agent = utils.assign_agent_for_lead()
            form.save()
        return redirect("/leads")
    else:
        response = HttpResponse()
        response.status_code = 404
        response.content = "<h1>Not found</h1>"
        return response


def lead_delete(request: HttpRequest, pk):
    Lead.objects.get(id=pk).delete()
    return redirect("/leads")
