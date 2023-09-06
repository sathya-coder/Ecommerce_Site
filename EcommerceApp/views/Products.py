from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.Products import *
from ..serializers.Products import *
from rest_framework.filters import SearchFilter
from django.db import models
from django.core.mail import send_mail
from datetime import datetime, timedelta
import random
import string




class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_update(self, serializer):
        instance = serializer.save()
        reviews = Review.objects.filter(product=instance)
        total_ratings = reviews.count()
        if total_ratings > 0:
            average_rating = sum(review.rating for review in reviews) / total_ratings
            instance.average_rating = average_rating
            instance.total_ratings = total_ratings
            instance.save()


class ProductAllList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartAddProduct(APIView):

    def post(self, request):
        
        # if not self.request.user.is_authenticated:
        #     raise AuthenticationFailed("User must be authenticated to add products to the cart.")

        # user = self.request.user
        serializer = CartUpdateSerializer(data=request.data)
        # request.session['cart_items'] = cart_items.count()
        if serializer.is_valid():
            product_ids = serializer.validated_data['product_ids']
            user = serializer.validated_data['user']

            # Assuming 'product_ids' is a list of product IDs
            products_to_add = Product.objects.filter(product_ids=product_ids)
            # Get or create the user's cart
            cart, created = Cart.objects.get_or_create(user=user)

            # Add products to the cart
            cart.products.add(*products_to_add)
            # cart.products = [{'id': product.name} for product in products_to_add]

            return Response({'message': 'Products added to cart'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'user'


class CheckoutView(APIView):
    def get(self, request, user_id):
        try:
            user = Register.objects.get(id=user_id)
            cart, _ = Cart.objects.get_or_create(user=user_id)
            products = cart.products.all()

            serializer = CheckoutSerializer({
                'user_details': user,
                'products': products,
                'payment_option': 'Cash on Delivery'  # Set the default payment option
            })

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Register.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)






class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '').strip()
        queryset = Product.objects.all()

        if search_query:
            first_two = search_query[:2]
            last_two = search_query[-2:]

            queryset = queryset.filter(
                (models.Q(name__icontains=first_two) & models.Q(name__icontains=last_two)) |
                (models.Q(description__icontains=first_two) & models.Q(description__icontains=last_two))
            )

        return queryset





class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ProductReviewsListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)


class ProductVariantListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class ProductVariantsListAPIView(generics.ListAPIView):
    serializer_class = ProductVariantSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductVariant.objects.filter(product_id=product_id)




class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    




from django.core.mail import send_mail

def send_reset_email(email, token):
    subject = 'Password Reset Link'
    message = f'Click the following link to reset your password: {token}'
    from_email = 'vigneshmurugan.dev@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = Register.objects.get(email=email)
                token = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
                reset_token = PasswordResetToken.objects.create(user=user, token=token)
                reset_token.expires_at = datetime.now() + timedelta(hours=1)
                reset_token.save()
                # Send the reset link with the token via email
                send_reset_email(email, token)  # Implement this function to send an email
                return Response({'message': 'Password reset link sent successfully.'})
            except Register.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            now = datetime.now()
            try:
                reset_token = PasswordResetToken.objects.get(token=token, expires_at__gte=now)
                user = reset_token.user
                user.set_password(password)
                user.save()
                reset_token.delete()
                return Response({'message': 'Password reset successfully.'})
            except PasswordResetToken.DoesNotExist:
                return Response({'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class coupungeneration(generics.ListCreateAPIView):
    queryset = Coupun.objects.all()
    serializer_class = CoupunSerializer



class userapplycoupun(APIView):

    def post(self, request):
        
        
        serializer = CoupunSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            coupun_code = serializer.validated_data['coupun_code']
            # percent_with_price = serializer.validated_data['percent_with_price']
            expiry_date = serializer.validated_data['expiry_date']
            
            # Assuming 'product_ids' is a list of product IDs
            if Coupun.objects.filter(coupun_code=coupun_code, expiry_date__gte=expiry_date).exists():

                if UsedCoupuns.objects.filter(user_id=user_id, status='0').exists():
                    # serializer = UsedCoupunsSerializer({
                    coupon = UsedCoupuns.objects.filter(user_id=user_id, status='0').first()
                    coupon.status = '1'
                    coupon.save()
                    # })
                    return Response({'message': 'Coupun Applied'}, status=status.HTTP_200_OK)
                elif UsedCoupuns.objects.filter(user_id=user_id, status='1').exists():
                    return Response({'message': 'Already Used'}, status=status.HTTP_200_OK)
                else:
                    coupon = Coupun.objects.get(coupun_code=coupun_code, expiry_date__gte=expiry_date)
                    serializer = UsedCoupunsSerializer(data={
                        'coupun_code_id': coupon.id,  # You may need to adjust this field based on your model
                        'user_id': user_id,
                        'status': '1'  # Set the default status
                    })
                    if serializer.is_valid():
                        serializer.save()
                    return Response({'message': 'Coupun Applied'}, status=status.HTTP_200_OK)
                    
            else:
                return Response({'message': 'Not Valid Coupun'}, status=status.HTTP_200_OK)
            # Get or create the user's cart
            

                # return Response({'message': 'Products added to cart'}, status=status.HTTP_200_OK)

        # return Response({'message': 'Coupun Applied'}, status=status.HTTP_200_OK)
    
class usercoupundelete(APIView):
    def post(self, request):  
        serializer = CoupunSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            coupun_code = serializer.validated_data['coupun_code']
            
            # Assuming 'product_ids' is a list of product IDs
            if Coupun.objects.filter(coupun_code=coupun_code).exists():
                if UsedCoupuns.objects.filter(user_id=user_id, status='1').exists():
                    coupon = UsedCoupuns.objects.filter(user_id=user_id, status='1').first()
                    coupon.status = '0'
                    coupon.save()
                    return Response({'message': 'Coupon Cancelled. Try again later.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'User has not used this coupon.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid Coupon.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class coupunlist(generics.ListCreateAPIView):
    queryset = UsedCoupuns.objects.all()
    serializer_class = UsedCoupunsSerializer
