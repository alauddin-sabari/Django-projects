Including steps for configuring PostgreSQL and registering the model in `admin.py` with specific columns.

---

#### **Slide 1: Project Setup**

**Title: Project Setup**

- **Step 1:** Install Django
  - `pip install django`
- **Step 2:** Create a Django Project
  - `django-admin startproject myproject`
- **Step 3:** Navigate to Project Directory
  - `cd myproject`
- **Step 4:** Create a Django App
  - `python manage.py startapp myapp`

---

#### **Slide 2: Configure the App**

**Title: Configure the App**

- **Step 1:** Add the App to Installed Apps
  - Open `myproject/settings.py`
  - Add `'myapp',` to `INSTALLED_APPS`
- **Step 2:** Install PostgreSQL and `psycopg2-binary`
  - `pip install psycopg2-binary`
- **Step 3:** Configure PostgreSQL Database
  - Update `myproject/settings.py` with PostgreSQL settings:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mydatabase',
            'USER': 'mydatabaseuser',
            'PASSWORD': 'mypassword',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
  - Ensure PostgreSQL server is running and the database `mydatabase` is created.

---

#### **Slide 3: Create Models**

**Title: Create Models**

- **Step 1:** Define a Model
  - Open `myapp/models.py`
  - Add the following code:
    ```python
    from django.db import models

    class Item(models.Model):
        name = models.CharField(max_length=100)
        description = models.TextField()

        def __str__(self):
            return self.name
    ```
- **Step 2:** Create and Apply Migrations
  - `python manage.py makemigrations`
  - `python manage.py migrate`

---

#### **Slide 4: Register Model in Admin**

**Title: Register Model in Admin**

- **Step 1:** Register the Model
  - Open `myapp/admin.py`
  - Add the following code to register the `Item` model and specify the columns:
    ```python
    from django.contrib import admin
    from .models import Item

    class ItemAdmin(admin.ModelAdmin):
        list_display = ('name', 'description')

    admin.site.register(Item, ItemAdmin)
    ```

---

#### **Slide 5: Create Forms**

**Title: Create Forms**

- **Step 1:** Define a Form
  - Create a file `myapp/forms.py`
  - Add the following code:
    ```python
    from django import forms
    from .models import Item

    class ItemForm(forms.ModelForm):
        class Meta:
            model = Item
            fields = ['name', 'description']
    ```

---

#### **Slide 6: Create Views**

**Title: Create Views**

- **Step 1:** Define Views
  - Open `myapp/views.py`
  - Add the following code:
    ```python
    from django.shortcuts import render, redirect
    from .models import Item
    from .forms import ItemForm

    def index(request):
        items = Item.objects.all()
        return render(request, 'myapp/index.html', {'items': items})

    def create_item(request):
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = ItemForm()
        return render(request, 'myapp/item_form.html', {'form': form})

    def update_item(request, pk):
        item = Item.objects.get(pk=pk)
        if request.method == 'POST':
            form = ItemForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = ItemForm(instance=item)
        return render(request, 'myapp/item_form.html', {'form': form})

    def delete_item(request, pk):
        item = Item.objects.get(pk=pk)
        if request.method == 'POST':
            item.delete()
            return redirect('index')
        return render(request, 'myapp/item_confirm_delete.html', {'item': item})
    ```

---

#### **Slide 7: Configure URLs**

**Title: Configure URLs**

- **Step 1:** Define App URLs
  - Create a file `myapp/urls.py`
  - Add the following code:
    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.index, name='index'),
        path('item/new/', views.create_item, name='create_item'),
        path('item/<int:pk>/edit/', views.update_item, name='update_item'),
        path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
    ]
    ```
- **Step 2:** Include App URLs in Project URLs
  - Open `myproject/urls.py`
  - Add the following code:
    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('myapp.urls')),
    ]
    ```

---

#### **Slide 8: Create Templates**

**Title: Create Templates**

- **Step 1:** Create Template Directory
  - Create a directory `myapp/templates/myapp`
- **Step 2:** Create Base Template
  - Create `myapp/templates/myapp/base.html`
  - Add the following code:
    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django CRUD</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            {% block content %}
            {% endblock %}
        </div>
    </body>
    </html>
    ```
- **Step 3:** Create Index Template
  - Create `myapp/templates/myapp/index.html`
  - Add the following code:
    ```html
    {% extends 'myapp/base.html' %}

    {% block content %}
    <h1>Items</h1>
    <a href="{% url 'create_item' %}" class="btn btn-primary mb-2">Add New Item</a>
    <ul class="list-group">
        {% for item in items %}
            <li class="list-group-item d-flex justify-content-between align-items-center">
                {{ item.name }}
                <span>
                    <a href="{% url 'update_item' item.pk %}" class="btn btn-warning btn-sm">Edit</a>
                    <form action="{% url 'delete_item' item.pk %}" method="post" class="d-inline">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                    </form>
                </span>
            </li>
        {% endfor %}
    </ul>
    {% endblock %}
    ```

---

#### **Slide 9: Create Form Template**

**Title: Create Form Template**

- **Step 1:** Create Form Template
  - Create `myapp/templates/myapp/item_form.html`
  - Add the following code:
    ```html
    {% extends 'myapp/base.html' %}

    {% block content %}
    <h1>{% if form.instance.pk %}Edit{% else %}New{% endif %} Item</h1>
    <form method="post">
        {% csrf_token %}
        <div class="form-group">
            {{ form.as_p }}
        </div>
        <button type="submit" class="btn btn-success">Save</button>
        <a href="{% url 'index' %}" class="btn btn-secondary">Cancel</a>
    </form>
    {% endblock %}
    ```

---

#### **Slide 10: Create Delete Confirmation Template**

**Title: Create Delete Confirmation Template**

- **Step 1:** Create Delete Confirmation Template
  - Create `myapp/templates/myapp/item_confirm_delete.html`
  - Add the following code:
    ```html
    {% extends 'myapp/base.html' %}

    {% block content %}
    <h1>Delete Item</h1>
    <p>Are you sure you want to delete "{{ item.name }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit" class="btn btn-danger">Delete</button>
        <a href="{% url 'index' %}" class="btn btn-secondary">Cancel</a>
    </form>
    {% endblock %}
    ```

---

#### **Slide 11: Run the Server**

**Title: Run the Server**

- **Step 1:** Start the Development Server
  - `python manage.py runserver`
- **Step 2:** Open Browser and Navigate to
  - `http://127.0.0.1:8000/`

---

---

This completes the setup and implementation of a Django CRUD application using PostgreSQL. You can now add, edit, and delete items through the web interface. Congratulations on building your first Django CRUD project!

---

