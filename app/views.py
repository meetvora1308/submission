from operator import add
from urllib import response
from django.contrib.auth.models import User
from app.models import Address, Token
from .serializers import * 
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import  authentication_classes 
from django.contrib.auth import authenticate
from math import cos, asin, sqrt, pi

@authentication_classes([])
class LoginUserApi(ViewSet):
    def create(self,request):
        '''
            This api use to login user using username and password
        '''
        # getting the fields
        username = request.data.get('username')
        password = request.data.get('password')
        
        #  verify data is present 
        if not username:
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'Username required'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        
        if not password:
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'password required'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username,password=password)
        if not user:
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'incorrect email id or password'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        old_token = Token.objects.filter(user=user)
        if old_token:
            old_token.delete()
        
        token = Token.objects.create(user = user)
        serializer = UserSerializer(user,context={'request':request})
        data = serializer.data
        data.update({'token':token.key})
        response = {'status':status.HTTP_200_OK,
                    'message':'successfull',
                    'data':data}
        return Response(response,status=status.HTTP_200_OK)

@authentication_classes([])
class RegisterUserAPI(ViewSet):
    
    def create(self,request):
        username = request.data.get('username')
        print('username: ', username)
        first_name = request.data.get('first_name')
        last_name= request.data.get('last_name')
        email = request.data.get('email')
        password= request.data.get('password')
    
        
        if not username:
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'Username required'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        if not first_name : 
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'first_name required'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        if not last_name:
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'last_name required'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        if not email:
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'email required'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        if not password:
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'password required'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'Already Registered'
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(email=email).exists() :
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':'Already Registered'}
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            response = {'status':status.HTTP_400_BAD_REQUEST,
                        'message':"Already Registered"
                    }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create(username=username,email=email,
                                   first_name=first_name,last_name=last_name,
                                   is_active=True
                                   )
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        serializer = UserSerializer(user,context={'request':request})
        data = serializer.data 
        data.update({'token':token.key})
        response = {'status':status.HTTP_200_OK,
                    'message':'successfull',
                    'data':data
                    }
        return Response(response,status=status.HTTP_200_OK)


class StoringAddress(ViewSet):
    
    def list(self,request):
        """
            List of all address created by user
        """
        user = request.user
        all_address = Address.objects.filter(user=user)
        serializer = AddressSerializer(all_address,many=True)
        response = {"status":status.HTTP_200_OK,
                    "message":"successfull",
                    "data":serializer.data
                    }
        return Response(response,status=status.HTTP_200_OK)
    
    def create(self,request):
        """
          create new address for user
        """
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        address = request.data.get("address")
        user = request.user
        
        if not latitude:
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Latitude required"
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        if not longitude:
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Longitude required"
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        if not address:
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Address required"
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        if Address.objects.filter(user=user,latitude=latitude,longitude=longitude).exists():
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Address already exist"
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        Address.objects.create(user=user,latitude=latitude,longitude=longitude,address=address)
        response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Address saved successfully"
                    }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Update user address 
        """
        user = request.user
        
        if not Address.objects.filter(user=user,id=pk).exists():
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Invalid request"
                    }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        address = request.data.get("address")
        address_data = Address.objects.filter(user=user,id=pk).first()
        
        if latitude:
            address_data.latitude = latitude
        if longitude:
            address_data.longitude = longitude
        if address:
            address_data.address = address
        
        address_data.save()
        response = {"status":status.HTTP_400_BAD_REQUEST,
                    "message":"Address updated successfully"
                    }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self,request,pk=None):
        """Delete the address that user has created """
        user = request.user
        
        if not Address.objects.filter(user=user,id=pk).exists():
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Invalid request"
                    }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        Address.objects.filter(user=user,id=pk).delete()

        response = {"status":status.HTTP_200_OK,
                    "message":"Address deleted successfully"
                    }
        return Response(response,status=status.HTTP_200_OK)
        

class Search(ViewSet):
    def create(self,request):
        """
         search near by address that user has created
        """
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        user = request.user
        
        if not latitude:
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Latitude required"
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
        if not longitude:
            response = {"status":status.HTTP_400_BAD_REQUEST,
                        "message":"Longitude required"
                        }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        
        
        user_address = Address.objects.filter(user=user)
        
        
        lat = float(latitude)
        lng = float(longitude)
        miles_to_km = float(10) * 1.609
        km_to_radius = miles_to_km/2
        nearby = []
        for checkin in user_address:
            
            p = pi/180
            lat2 = float(checkin.lat)
            lon2 = float(checkin.long)
            a = 0.5 - cos((lat2-lat)*p)/2 + cos(lat*p) * cos(lat2*p) * (1-cos((lon2-lng)*p))/2
            dist = 12742 * asin(sqrt(a))
            if dist<km_to_radius:
                nearby.append(checkin) 
        
        serializer = AddressSerializer(nearby,many=True)
        response = {"status":status.HTTP_400_BAD_REQUEST,
                    "message":"Searched successfull",
                    "data":serializer.data
                    }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

        
        