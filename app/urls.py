"""liveledger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import app.views

urlpatterns = [
    path('', app.views.RedirectHomeView.as_view()),
    path('home/', app.views.HomeView.as_view(), name='home'),
    path('index/', app.views.LedgerListView.as_view(), name='ledger-list'),
    path('create/', app.views.LedgerCreateView.as_view(), name='ledger-create'),
    path('delete/<pk>/', app.views.LedgerDeleteView.as_view(), name='ledger-delete'),
    path('share/<pk>/', app.views.LedgerShareView.as_view(), name='ledger-share'),
    path('share/<pk>/removeself/', app.views.LedgerSharedRemoveMeView.as_view(), name='ledger-share-remove-me'),
    path('share/<pk>/removeuser/<username>/', app.views.LedgerSharedUserRemoveView.as_view(), name='ledger-share-removeuser'),
    path('ledger/<ledgerid>/index/', app.views.LedgerItemListview.as_view(), name='ledgeritem-list'),
    path('ledger/<ledgerid>/create/', app.views.LedgerItemCreateView.as_view(), name='ledgeritem-create'),
    path('ledgeritem/<pk>/update/', app.views.LedgerItemUpdateView.as_view(), name='ledgeritem-update'),
    path('ledgeritem/<pk>/delete/', app.views.LedgerItemDeleteView.as_view(), name='ledgeritem-delete'),
    path('ledgeritem/<pk>/inquire/', app.views.LedgerItemInquireView.as_view(), name='ledgeritem-inquire'),
    path('forbidden/', app.views.ForbiddenView.as_view(), name='forbidden'),
]
