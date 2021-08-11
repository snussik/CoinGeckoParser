from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ArbitSituation
from django.views.generic import FormView
from .forms import FilterForm
from functools import reduce
from django.core.paginator import Paginator
from django.http import QueryDict
from django.db.models import Q


class MainView(FormView):
	template_name = 'index.html'
	form_class = FilterForm

	def get_context_data(self, *args, **kwargs):
		context = super(MainView, self).get_context_data(*args, **kwargs)
		obj = Paginator(ArbitSituation.objects.all(), 20)
		context['object_list'] = obj.page(1).object_list
		return context

	def form_valid(self, form, *args, **kwargs):
		markets = form.cleaned_data.get('markets')
		profitUp = form.cleaned_data.get('profitUp')
		profitDown = form.cleaned_data.get('profitDown')
		volume = form.cleaned_data.get('volume')
		data = list()
		query = ArbitSituation.objects.all()
		if markets:
			if len(markets) > 1:
				for i in range(len(markets) - 1):
					for j in range(i+1, len(markets)):
						data.append(ArbitSituation.objects.filter(market1=markets[i]).filter(market2=markets[j]))
			elif len(markets) == 1:
				data.append(ArbitSituation.objects.filter(Q(market1=markets[0]) | Q(market2=markets[0])))
		if data:
			query = reduce(lambda x, y : x | y, data)
		if profitUp or profitDown:
			if profitUp:
				profitUp = 1 + profitUp/100
			else:
				profitUp = 1
			if profitDown:
				profitDown = 1 + profitDown/100
			else:
				profitDown = 100
			query = query.filter(profit__gte=profitUp).filter(profit__lte=profitDown)
		if volume:
			query = query.filter(volume__gte=volume)

		next_page = kwargs.get('p', 1)
		if next_page != 1:
			return query
		obj = Paginator(query, 20)
		query = list(obj.page(next_page).object_list.values())
		
		return render(self.request, self.template_name, context={'object_list': query, 
																	'form': form})

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			next_page = request.POST.get('p')
			if next_page:
				d = request.POST.copy()
				d.pop('p')
				d = d.get('data')
				d = QueryDict(d)
				form = FilterForm(d)
				next_page = int(next_page[0]) + 1
				if form.is_valid():
					print(form.cleaned_data)
					data = self.form_valid(form, p=next_page)					
				else:
					data = ArbitSituation.objects.all() 
				obj = Paginator(data, 20)
				context = list(obj.page(next_page).object_list.values())
				print(context)		
				return JsonResponse({'objs': context})
		else:
			f = FilterForm(request.POST)
			if f.is_valid():
				return self.form_valid(f)



	
