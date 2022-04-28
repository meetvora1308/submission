from app.views import (LoginUserApi, RegisterUserAPI,StoringAddress, Search)
from rest_framework import routers

router = routers.DefaultRouter()

router.register('login_user',LoginUserApi,'social_login_api')
router.register('register_user',RegisterUserAPI,'subscription')

router.register("address",StoringAddress,'sotringapiAddress')
router.register("serch_address",Search,'sotringapiAddress')

urlpatterns = [
    
] + router.urls