from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sluiceApp.models import Inventory
from sluiceApp.serializers import InventorySerializer

from drf_spectacular.utils import extend_schema

# Create your views here.

@extend_schema(
    request=InventorySerializer
)
@api_view(['GET', 'POST'])
def inventory_list(request):
    
    if request.method == 'GET':
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

@extend_schema(
    request=InventorySerializer
)
@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, id, format=None):
    
    try:
        item = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        return status(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        serializer = InventorySerializer(item)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = InventorySerializer(instance=item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        pass

@api_view(['PUT'])
def reduce_stock(request, id, format=None):
    try:
        item = Inventory.objects.get(id=id)
    except Inventory.DoesNotExist:
        return status(status=status.HTTP_404_NOT_FOUND)
    
    
    #update
    if request.method == 'PUT':
        
        #once item found, check if it can be reduced
        if item.reduce_stock(request.data['amount_used']):
            data = {
                'name' : item.name,
                'stock' : item.stock
            }
            serializer = InventorySerializer(instance=item, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            stock = item.stock
            reduce_amount = request.data['amount_used']
            resp_msg = f'Can\' reduce item by {reduce_amount}!\nCurrent stock: {stock}.\n Check amount requested.'
            return Response(
                {'ERROR':resp_msg},
                )
        

            
        

        