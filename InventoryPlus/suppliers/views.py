from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .forms import SupplierForm
from .models import Supplier
from django.contrib import messages
# Create your views here.


def add_supplier_view(request:HttpRequest):

    supplier_form = SupplierForm()

    if request.method == "POST":
        
        supplier_form = SupplierForm(request.POST, request.FILES)
        if supplier_form.is_valid():
            supplier_form.save()
            messages.success(request, "Supplier added successfully", extra_tags="alert-success")
            return redirect('main:home_view')
        else:
            messages.error(request, "Can't added supplier, not valid form", extra_tags="alert-danger")
            print("not valid form", supplier_form.errors)
    
    return render(request, "suppliers/add_supplier.html", {"supplier_form":supplier_form})


def all_suppliers_view(request:HttpRequest, supplier_id):
    if supplier_id =="all":
        suppliers = Supplier.objects.all()
    else:
        suppliers  = Supplier.objects.filter(pk=supplier_id)
    # products = Product.objects.filter(category__name = product_param).order_by("-expiry_date")
    # products = Product.objects.filter(suppliers__id__in=[product_param]).order_by("-expiry_date")
    # supplier  = Supplier.objects.filter(pk=product_param)

    return render(request, "suppliers/all_suppliers.html", { 'suppliers':suppliers})




def supplier_detail_view(request:HttpRequest, supplier_id:int):

    supplier = Supplier.objects.get(pk=supplier_id)

    return render(request, 'suppliers/supplier_detail.html', {"supplier" : supplier})


def delete_supplier_view(request:HttpRequest, supplier_id:int):
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.delete()
        messages.success(request, "Deleted Supplier successfully", extra_tags="alert-success")
    except Exception as e:
        print(e)
        messages.error(request, "Deleted Supplier successfully", extra_tags="alert-danger")
    return redirect("main:home_view")


def update_supplier_view(request:HttpRequest, supplier_id:int):
    supplier = Supplier.objects.get(pk=supplier_id)
    if request.method == "POST":
        #using SupplierForm for updating
        supplier_form = SupplierForm(instance=supplier, data=request.POST, files=request.FILES)
        if supplier_form.is_valid():
             supplier_form.save()
             messages.success(request, "Updated Supplier successfully", extra_tags="alert-success")
        else:
            print( supplier_form.errors)
            messages.error(request, f"Can't update supplier..{supplier_form.errors}", extra_tags="alert-danger")
        return redirect("suppliers:supplier_detail_view", supplier_id=supplier.id)

    return render(request, "suppliers/update_supplier.html", {"supplier": supplier})
