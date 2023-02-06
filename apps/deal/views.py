from django.http import Http404
from django.shortcuts import render
from rest_framework import permissions, status, filters
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import generics, views
import csv

from rest_framework.views import APIView

from .models import Customer, Gem, Deal, File
from .serializers import CustomerSerializer, DealSerializer, FileSerializer
import chardet


def deal_to_db(filename):
    with open(filename, encoding='utf-8') as r_file:
        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.reader(r_file, delimiter = ",")
        # Счетчик для подсчета количества строк и вывода заголовков столбцов
        count = 0
        # Считывание данных из CSV файла
        for row in file_reader:
            if count == 0:
                # Вывод строки, содержащей заголовки для столбцов
                print(f'    {", ".join(row)}')
            else:
                if Gem.objects.filter(name=row[1]).exists():
                    gem = Gem.objects.get(name=row[1])
                    if Deal.objects.filter(username=row[0]).exists():
                        deal = Deal.objects.get(username=row[0])
                        deal.gems.add(gem)
                        deal.spent_money += int(row[2])
                        deal.save()
                    else:
                        deal = Deal.objects.create(
                            username=row[0],
                            spent_money=int(row[2])
                        )
                        deal.save()
                        deal.gems.add(gem)
                else:
                    gem2 = Gem.objects.create(name=row[1])
                    gem2.save()
                    if Deal.objects.filter(username=row[0]).exists():
                        deal = Deal.objects.get(username=row[0])
                        deal.gems.add(gem2)
                        deal.spent_money += int(row[2])
                        deal.save()
                    else:
                        deal = Deal.objects.create(
                            username=row[0],
                            spent_money=int(row[2])
                        )
                        deal.save()
                        deal.gems.add(gem2)
                Customer.objects.create(
                    username=row[0],
                    item=row[1],
                    total=row[2],
                    quantity=row[3],
                    date=row[4],
                )
                print(f'    {row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} ')
            count += 1
        print(f'Всего в файле {count} строк.')


class DealCreateView(views.APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request):
        deal_to_db('deals.csv')
        return Response(status=status.HTTP_200_OK)


class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = CustomerSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['username', 'item', 'total', 'quantity']
    search_fields = ['username', 'item', 'total', 'quantity', 'date']


class ClientListView(generics.ListAPIView):
    queryset = Deal.objects.filter()
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = CustomerSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['username', 'item', 'total', 'quantity']
    search_fields = ['username', 'item', 'total', 'quantity', 'date']


class CustomerDetailView(views.APIView):
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    parser_classes = [JSONParser, MultiPartParser]

    def get(self, request, username):
        customers = Customer.objects.filter(username=username)
        spent_money = 0
        for customer in customers:
            spent_money += customer.total
        data = {
            'username': username,
            'spent_money': spent_money
        }
        return Response(data, status=status.HTTP_200_OK)


class DealListView(generics.ListAPIView):
    queryset = Deal.objects.order_by('-spent_money')
    permission_classes = [permissions.AllowAny]
    # authentication_classes = []
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = DealSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['username', 'spent_money', 'gems__name']
    search_fields = ['username', 'spent_money', 'gems__name']


class UploadFileView(generics.CreateAPIView):
    queryset = File.objects.all()
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = FileSerializer


class FileReadAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializers = FileSerializer(data=request.data)
        if serializers.is_valid():
            file = File.objects.create(
                file=request.data['file']
            )
            file.save()
            deal_to_db(file.file.path)
            return Response({'Файл был обработан без ошибок'}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
