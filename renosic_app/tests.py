from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Activity
from django.db.models import Count # 使用する場合はインポート

# ---
# Customer Model のテスト (setUpに依存しないテスト)
# ---

class CustomerModelTests(TestCase):
    
    # test_is_empty は、setUpがないこのクラスでは成功します。
    def test_is_empty(self): 
        saved_customers = Customer.objects.all()
        self.assertEqual(saved_customers.count(), 0) 
        
    def test_create_customer(self):
        # データベースが空であることを確認 (0件)
        self.assertEqual(Customer.objects.count(), 0) 

        # 顧客を1件作成する
        customer = Customer.objects.create(
            company_name="テスト株式会社",
            contact_name="テスト 太郎",
            email="test@example.com"
        )
        
        # 作成後に顧客が1件になったことを確認 (1件)
        saved_customers = Customer.objects.all()
        self.assertEqual(saved_customers.count(), 1) # <--- ここで 1 になることを確認

        self.assertEqual(saved_customers[0].company_name, "テスト株式会社")


# ---
# Customer List View のテスト (認証やデータ表示を検証)
# ---

class CustomerViewTests(TestCase):
    
    # 1. setUpメソッドを一つに統一し、必要なデータ（ユーザー、顧客）を全て作成します。
    def setUp(self):
        # ユーザーオブジェクトの作成
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')

        # 担当顧客の作成 (self.userが担当)
        self.customer = Customer.objects.create(
            company_name='自分の担当顧客',
            contact_name="担当者A",
            email="a@example.com",
            user=self.user # 担当者
        )
        
        # 他人の顧客の作成 (other_userが担当)
        Customer.objects.create(
            company_name='他人の担当顧客',
            contact_name="担当者B",
            email="b@example.com",
            user=self.other_user
        )

    def test_login_required(self):
        """
        ログインしていないユーザーは顧客リストにアクセスできず、ログインページにリダイレクトされることを確認。
        """
        response = self.client.get(reverse('customer_list'))

        # ステータスコードが302 (リダイレクト) であることを確認
        self.assertEqual(response.status_code, 302)

        # リダイレクト先がログインURLであることを確認
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_users_can_see_their_data(self):
        """
        ログインしたユーザーが自分の担当顧客のリストを正常に閲覧できることを確認。
        """
        self.client.force_login(self.user)

        response = self.client.get(reverse('customer_list'))

    
        self.assertEqual(response.status_code, 200)

        # 自分の担当顧客名が表示されていることを確認
        self.assertContains(response, "自分の担当顧客")
        

    def test_cannot_see_others_data(self):
        """
        ログインしたユーザーが、他人の担当顧客のデータを見ることができないことを確認。
        """
        self.client.force_login(self.other_user) # 他のユーザーとしてログイン

        response = self.client.get(reverse('customer_list'))

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "自分の担当顧客") 
        self.assertContains(response, "他人の担当顧客")