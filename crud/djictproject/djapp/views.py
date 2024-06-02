from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm

def index(request):
    items = Item.objects.all()
    return render(request, 'djapp/index.html', {'items': items})

def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ItemForm()
    return render(request, 'djapp/item_form.html', {'form': form})

def update_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ItemForm(instance=item)
    return render(request, 'djapp/item_form.html', {'form': form})

def delete_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('index')
    return render(request, 'djapp/item_confirm_delete.html', {'item': item})