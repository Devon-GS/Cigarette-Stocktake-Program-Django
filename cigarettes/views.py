from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import csv
import pandas as pd
from .models import Cigarette

def home(request):
    if request.method == 'POST':
        item_barcode = request.POST['barcode']
        item_name = request.POST['productName']
        item_stock = request.POST['stockLevel']
        
        try:
            # Create New Object
            new_item = Cigarette(barcode = item_barcode, product_name = item_name, stock_level = item_stock)
            new_item.save()
            return redirect('home')
        except:
            messages.success(request, "That Barcode already Exists")
            return redirect('home')
    else:
        return render(request, 'home.html', {})
    
def add_items(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        
        # Read in excel
        read_info = pd.read_excel(file, header=0)
        # Data to list
        data = read_info.to_numpy()
        
        for x in data:
            new_item = Cigarette(barcode = x[0], product_name = x[1], stock_level = x[2])
            new_item.save()
            
        messages.success(request, "Products Added Successfully")
        return redirect('add_items')
        
    else:
        return render(request, 'add_items.html', {})
        
    return render(request, 'add_items.html', {})



def add_sales(request):    
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        
        # Read in excel
        read_info = pd.read_excel(file, header=0)
        # Data to list
        data = read_info.to_numpy()
        
        for x in data:
            barcode = x[0]
            product = Cigarette.objects.get(barcode=barcode)
            current_sales = product.product_sales 
            product.product_sales = int(current_sales) + int(x[2])
            product.save()
            
        messages.success(request, "Sales Added Successfully")
        return redirect('add_sales')
    
    else:
        return render(request, 'add_sales.html', {})
        
    return render(request, 'add_sales.html', {})

def add_purchases(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        
        # Read in excel
        read_info = pd.read_excel(file, header=0)
        # Data to list
        data = read_info.to_numpy()
        
        for x in data:
            barcode = x[0]
            product = Cigarette.objects.get(barcode=barcode)
            current_purchases = product.product_purchases 
            product.product_purchases = int(current_purchase) + int(x[2])
            product.save()
            
        messages.success(request, "Purchases Added Successfully")
        return redirect('add_purchases')
    
    else:
        return render(request, 'add_purchases.html', {})
        
    return render(request, 'add_purchases.html', {})
    
def calculate(request):
    products = Cigarette.objects.all()
    
    k = []
    for x in products:
        barcode = x.barcode
        sales = int(x.product_sales)
        purchases = int(x.product_purchases)
        stock_level = int(x.stock_level)
        
        stock_on_hand = (stock_level + purchases) - sales
        
        l = [x.product_name, stock_level, purchases, sales, stock_on_hand]
        
        k.append(l)
    
    return render(request, 'calculate.html', {
        'k': k
    })


def calculate_stock_on_hand(request):
    products = Cigarette.objects.all()
    
    k = []
    for x in products:
        barcode = x.barcode
        sales = int(x.product_sales)
        purchases = int(x.product_purchases)
        stock_level = int(x.stock_level)
        
        stock_on_hand = (stock_level + purchases) - sales
        
        # Save Stock On Hand To Database
        product = Cigarette.objects.get(barcode=barcode)
        product.product_stock_on_hand = stock_on_hand
        product.save()
        
    messages.success(request, "Stock On Hand Calculated Successfully")
    return redirect('calculate')
    
    
def csv_download(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Stock On Hand.csv'
        
    # Create a csv writer
    writer = csv.writer(response)
        
    # Designate The Model
    cigarettes = Cigarette.objects.all()
      
    # Add column headings to the csv file
    writer.writerow(['Barcode', 'Product Name', 'Stock Level', 'Purchases', 'Sales', 'Stock On Hand'])
        
    # Loop Thu and output
    for c in cigarettes:
        writer.writerow([c.barcode, c.product_name, c.stock_level, c.product_purchases, c.product_sales, c.product_stock_on_hand])
        
    return response

def clean_database(request):
    products = Cigarette.objects.all()
    if request.method == "POST":
        x = request.POST["info"]
        if x == 'yes':
            for x in products:
                barcode = x.barcode
                product = Cigarette.objects.get(barcode=barcode)
                
                product.product_sales = '0'
                product.product_purchases = '0'
                product.stock_level = product.product_stock_on_hand 
                product.save()
            
            messages.success(request, "Database Cleaned Successfully")
            return redirect('calculate')
    
        else:
            messages.success(request, "Database NOT Cleaned")
            return redirect('calculate')
        
    
    return render(request, 'clean_database.html', {})

def reset_stock_levels(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        
        # Read in excel
        read_info = pd.read_excel(file, header=0)
        # Data to list
        data = read_info.to_numpy()
        
        for x in data:
            barcode = x[0]
            product = Cigarette.objects.get(barcode=barcode)
            product.stock_level = x[2]
            product.save()
            
        messages.success(request, "Stock Levels Reset Successfully")
        return redirect('reset_stock_levels')
    
    else:
        return render(request, 'reset_stock_levels.html', {})
        
    return render(request, 'reset_stock_levels.html', {})