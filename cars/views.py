from django.shortcuts import render, redirect
from cars.models import Car
from cars.forms import CarModelForm
from django.views import View
from django.db.models import Q

class CarsView(View):
    def get(self, request):
        cars = Car.objects.all().order_by('model')
        search = request.GET.get('search')

        if search:
            query = Q(model__icontains=search) | Q(brand__name__icontains=search) | Q(plate__icontains=search)

            # tentar converter para int/float para aplicar nos campos numéricos
            if search.isdigit():
                query |= Q(factory_year=search) | Q(model_year=search)
            try:
                value = float(search.replace(',', '.'))
                query |= Q(value=value)
            except ValueError:
                pass
            cars = cars.filter(query)

        return render(request, 'cars.html', {'cars': cars})


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