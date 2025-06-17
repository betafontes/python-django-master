from cars.models import Car
from cars.forms import CarModelForm
from django.db.models import Q
from django.views.generic import ListView, CreateView, DetailView, UpdateView


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


class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response({'new_car_form': form})    


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car'] = self.object
        return context    


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarModelForm
    template_name = 'car_update.html'
    success_url = '/cars/'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response({'car_update_form': form})