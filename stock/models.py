from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    # PK(기본키)인 user_id는 장고가 알아서 'id'라는 이름으로 만들어주므로 안 적어도 됩니다!
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True) # 이메일 형식 확인 및 중복 방지
    nickname = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True) # 데이터가 생성될 때 현재 시간 자동 저장

    def __str__(self):
        return self.nickname # Admin 페이지에서 글자 대신 닉네임이 예쁘게 보이게 해줍니다.

# 2. 주식 종목 (Stocks) 테이블
class Stock(models.Model):
    # 종목코드는 장고가 자동 생성하는 id 대신, 우리가 직접 PK로 지정합니다. (primary_key=True)
    stock_code = models.CharField(max_length=20, primary_key=True) 
    company_name = models.CharField(max_length=100)
    market_type = models.CharField(max_length=20)
    current_price = models.DecimalField(max_digits=10, decimal_places=4)
    updated_at = models.DateTimeField(auto_now=True) # 데이터가 수정될 때마다 시간 자동 갱신

    def __str__(self):
        return self.company_name
    
# 3. AI 추천 레포트 (Recommendations) 테이블
class Recommendation(models.Model):
    # stock_code(FK): 어떤 주식에 대한 레포트인지 연결합니다. (주식이 지워지면 레포트도 같이 삭제: CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='recommendations') 
    title = models.CharField(max_length=255)
    summary = models.TextField() # 글자 수가 많은 긴 글은 TextField를 씁니다.
    ai_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 4. 추천 상세 근거 (Reasons) 테이블
class Reason(models.Model):
    # report_id(FK): 어떤 레포트에 속한 근거인지 연결합니다. (레포트가 지워지면 근거도 같이 삭제: CASCADE)
    report = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='reasons')
    sequence = models.IntegerField() # 카드 순서 (1, 2, 3...)
    category = models.CharField(max_length=50) # 재무, 뉴스, 선례 등
    content = models.TextField()
    visual_url = models.URLField(max_length=255, blank=True, null=True) # 이미지가 없을 수도 있으니 빈칸 허용

    def __str__(self):
        return f"{self.report.title} - 근거 {self.sequence}"

# 5. 북마크 (Bookmarks) 테이블
class Bookmark(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookmarks') # 누가 북마크 했는지 연결
    report = models.ForeignKey(Recommendation, on_delete=models.CASCADE, related_name='bookmarks') # 어떤 레포트를 북마크 했는지 연결
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname}님의 북마크: {self.report.title}"