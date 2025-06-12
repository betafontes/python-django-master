from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm
from django.views import View
from django.db.models import Q
from django.views.generic import ListView


class CarListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('model')
        search = self.request.GET.get('search')
        if search:
            query = Q(model__icontains=search) | Q(brand__name__icontains=search) | Q(plate__icontains=search)
            if search.isdigit():
                query |= Q(factory_year=search) | Q(model_year=search)
            try:
                value = float(search.replace(',', '.'))
                query |= Q(value=value)
            except ValueError:
                pass
            queryset = queryset.filter(query)
        return queryset


class NewCarView(View):
    def get(self, request):
        new_car_form = CarModelForm()
        return render(request, 'new_car.html', {'new_car_form': new_car_form})

    def post(self, request):
        new_car_form = CarModelForm(request.POST, request.FILES)
        if new_car_form.is_valid():
            new_car_form.save()
            return redirect('cars_list')
        return render(request, 'new_car.html', {'new_car_form': new_car_form})