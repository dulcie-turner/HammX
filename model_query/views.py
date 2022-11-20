from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def region_to_latlon(region):
    if region == "cambridge": 
        return [52.2053,0.1218]

def index(request):
    if request.method == "POST":
        template = loader.get_template('model_query/index.html')
        data = request.POST
        formData = {
            "region": data["region"],
            "latlon": region_to_latlon(data["region"]),
            "photoperiod": data["photoperiod"],
            "texture": data["texture"],
            "fertility": data["fertility"],
            "pH": data["pH"],
            "change": data["change"],
            "optimal": data["optimal"],
            "timescale": data["timescale"],
            "largeScale": False,
            "category": data["category"],
            "nutrients": data["nutrient"],
        }

        if "largeScale" in data:
            formData["largeScale"] = True

        print(formData)
        context = {"out": request.POST.keys()}
    else:
        template = loader.get_template('model_query/index.html')
        context = {"out": "not test"}
    return HttpResponse(template.render(context, request))


"""    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})"""