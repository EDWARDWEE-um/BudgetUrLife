from django.db.models.aggregates import Count
from .forms import ExpenseForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Expense, Project, Category
from django.views.generic import CreateView
from django.utils.text import slugify
import json
from django.db.models import Sum
# Create your views here.
def project_list(request):
    project_list = Project.objects.all()
    return render(request,'budget/project-list.html',{'project_list':project_list})
def project_projections(request):
    if request.method == 'GET':
        category_list = Category.objects.filter(project=project)
        totalexpense = Expense.objects.filter(project=project).values('category__name').order_by('category').annotate(total_price=Sum('amount'))
        expensename = Expense.objects.filter(project=project).values('title','amount','category__name')
        return render(request,'budget/project-projections.html', {'project':project, 'expense_list': project.expenses.all(),'category_list':category_list,'totalexpense':totalexpense,'expensename':expensename})
 

def project_detail(request, project_slug):
    # fetch the correct project
    project = get_object_or_404(Project, slug=project_slug)
    if request.method == 'GET':
        category_list = Category.objects.filter(project=project)
        totalexpense = Expense.objects.filter(project=project).values('category__name').order_by('category').annotate(total_price=Sum('amount'))
        expensename = Expense.objects.filter(project=project).values('title','amount','category__name')
        return render(request,'budget/project-detail.html', {'project':project, 'expense_list': project.expenses.all(),'category_list':category_list,'totalexpense':totalexpense,'expensename':expensename})
    elif request.method == 'POST':
        # Process the form
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']
            category = get_object_or_404(Category , project=project , name=category_name)
            
            Expense.objects.create(
                project=project,
                title=title,
                amount=amount,
                category=category,
            ).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()
        return HttpResponse('')

    return HttpResponseRedirect(project_slug)

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'budget/add-project.html'
    fields = ('name', 'budget')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.save()

        categories = self.request.POST['categoriesString'].split(',')
        for category in categories :
            Category.objects.create(
                project=Project.objects.get(id=self.object.id),
                name=category
            ).save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return slugify(self.request.POST['name'])