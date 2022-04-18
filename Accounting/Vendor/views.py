from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Vendor, Bill, BillItem

from . import urls as vendor_urls
from . import tables as vendor_tables
from . import forms as vendor_forms
import re


@login_required
def vendors(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company
    # Vendor.objects.create(name='kashif', contact='02323', email='abc@gmail.com', type='REGULAR', company=company)
    vendors = Vendor.objects.filter(company=company)
    # for v in vendors:
    #     v.delete()
    #     v.save()
    context = {
        'vendors': vendors,
        "nav": {
            "parent_active": "vendor",
            "child_active": "vendor",
        },
    }
    return render(request, "accounting/vendor/index.html", context)


@login_required
def vendors2(request):
    company = request.user.userprofile.companyprofilemodel

    # vendors = Vendor.objects.filter(company=company)
    queryset = company.vendor_set.all()
    context = {
        "title": "Manage Vendors",
        "actions": [
            {
                "title": "Create",
                "icon": "fas fa-plus",
                "classes": "btn btn-xs btn-white btn-icon-only width-auto commonModal",
                "href": "javascript:;",
                "attributes": [
                    {
                        "name": "data-size",
                        "value": "2xl"
                    },
                    {
                        "name": "data-url",
                        "value": vendor_urls.create_vendors()
                    },
                    {
                        "name": "data-ajax-popup",
                        "value": "true"
                    }, {
                        "name": "data-title",
                        "value": "Create New Designation"
                    }, {
                        "name": "data-toggle",
                        "value": "modal"
                    }, {
                        "name": "data-target",
                        "value": "#commonModal"
                    }
                ]
            },
            {
                "title": "Export",
                "icon": "fa fa-file-excel",
                "classes": "btn btn-xs btn-white btn-icon-only width-auto",
                "href": "javascript:;",
                "attributes": [
                ]
            },
            {
                "title": "Import",
                "icon": "fa fa-file-csv",
                "classes": "btn btn-xs btn-white btn-icon-only width-auto",
                "href": "javascript:;",
                "attributes": [

                ]
            }
        ],
        "tables": [
            {
                # "title": "Vendors",
                "table": vendor_tables.VendorTable(queryset)
            },
        ],
        "form": {
            "action": vendor_urls.create_vendors(),
            "form": vendor_forms.VendorForm()
        }

    }
    return render(request, "accounting/list-entries.html", context)


@login_required
def get_vendor_detail(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    context = {
        'vendor': vendor,
        "nav": {
            "parent_active": "vendor",
            "child_active": "vendor",
        },
    }
    return render(request, "accounting/vendor/details.html", context)


@login_required
def add_vendor(request):
    if request.method == "POST":
        type = request.POST.get("type")
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        billing_name = request.POST.get("billing_name")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        billing_phone = request.POST.get("billing_phone")
        zip = request.POST.get("zip")
        address = request.POST.get("address")
        ssn = request.POST.get("ssn")
        ein = request.POST.get("ein")
        if request.user.userprofile.role == 'COMPANY':
            company = request.user.userprofile.companyprofilemodel
        else:
            company = request.user.userprofile.employeeprofilemodel.company.company

        Vendor.objects.create(vendor_type=type, company=company, name=name, contact=contact, email=email,
                              billing_name=billing_name, country=country, state=state, city=city,
                              billing_phone=billing_phone, zip=zip, address=address, ssn=ssn,
                              ein=ein)

        messages.success(request, 'Vendor Created!')

        return redirect('vendors')


@login_required
def edit_vendor(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    if request.method == "POST":
        vendor.type = request.POST.get("type")
        vendor.name = request.POST.get("name")
        vendor.email = request.POST.get("email")
        vendor.contact = request.POST.get("contact")
        vendor.billing_name = request.POST.get("billing_name")
        vendor.country = request.POST.get("country")
        vendor.state = request.POST.get("state")
        vendor.city = request.POST.get("city")
        vendor.billing_phone = request.POST.get("billing_phone")
        vendor.zip = request.POST.get("zip")
        vendor.address = request.POST.get("address")
        vendor.ssn = request.POST.get("ssn")
        vendor.ein = request.POST.get("ein")
        vendor.save()
        messages.success(request, 'Vendor Edited Successfully')
        return redirect('vendors')
    else:
        context = {
            'vendor': vendor,
            "nav": {
                "parent_active": "vendor",
                "child_active": "vendor",
            },

        }
        form_html = render_to_string("accounting/vendor/edit_form.html", context, request)
        return JsonResponse(form_html, safe=False)


@login_required
def delete_vendor(request, pk):
    vendor = Vendor.objects.get(pk=pk)
    vendor.delete()

    messages.success(request, 'Vendor Deleted Successfully')

    return redirect('vendors')


@login_required
def vendor_bills(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company
    vendors = Vendor.objects.filter(company=company)
    form = request.POST
    if form:
        vendor = Vendor.objects.get(id=form.get('vender_id'))

        numbers_of_bill_item = int((len(list(form.keys())) - 5) / 8)

        bill = Bill.objects.create(company=company, vendor=vendor, bill_number=form.get('bill_number'),
                                   bill_date=form.get('bill_date'), due_date=form.get('due_date'),
                                   notes=form.get('notes'))
        print(numbers_of_bill_item)
        bill_items = []
        for i in range(0, numbers_of_bill_item):
            print(form.get(f'items[{i}][item]'))
            bill_items.append({
                'bill': bill,
                'item': form.get(f'items[{i}][item]'),
                'quantity': form.get(f'items[{i}][quantity]'),
                'price': form.get(f'items[{i}][price]'),
                'amount': ((float(form.get(f'items[{i}][price]')) * float(form.get(f'items[{i}][quantity]'))) - float(
                    form.get(f'items[{i}][discount]'))) + float(form.get(f'items[{i}][itemTaxPrice]')),
                'tax': form.get(f'items[{i}][itemTaxPrice]'),
                'discount': form.get(f'items[{i}][discount]'),
                'description': form.get(f'items[{i}][description]'),
            })
        for item in bill_items:
            BillItem.objects.create(**item)
        messages.success(request, 'Bill and Its Items are Added!')
        print(bill_items)
    context = {
        'vendors': vendors,

        "nav": {
            "parent_active": "vendor",
            "child_active": "vendor",
        },
    }
    return render(request, 'accounting/vendor/vendor_create_bill.html', context)
