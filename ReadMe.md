## Introduction

해외 기계식 키보드, 오디오 공동구매 스타트업 DROP 사이트 클론 코딩

- 기간 : 2022.06.20 ~ 2022.07.01
- 구성 : Front-end 3명, Back-end 1명
- [Back-end 깃헙 주소](https://github.com/wecode-bootcamp-korea/34-1st-HDPDB-backend)
- [Front-end 깃헙 주소](https://github.com/wecode-bootcamp-korea/34-1st-HDPDB-frontend)

## DB modeling

![HDPDB-DROP.png](https://user-images.githubusercontent.com/104124384/176837849-9250f078-fe2f-424c-bf95-5f36421a3869.png)

## Technologies

- Python
- Django Web Framework
- MySQL
- React

## Features

- products
    - 제품 상세 정보 불러오기
    - 제품 옵션 선택을 통한 최종 제품 필터링
    - 제품 목록 필터링을 통해 정렬(Featured, Category
- order
    - 장바구니 추가, 삭제, 수정
- users
    - 조건을 만족하는 데이터로 회원가입
    - 로그인시 인증토큰 전송
- core
    - 로그인이 필요한 기능 사용시 토큰검사 및 디코딩
    - 데이터베이스에 타임스탬프 찍는 모델
- etc
    - csv 데이터를 통해 데이터 일괄 등록 가능

## API

### Base Request

```python
통신 에러를 피하기 위해 모튼 요청은 api 로 전송 되어야함
(host)/api
```

### Cart Request

```python
모든 요청은 헤더에 Authorization Json Web Token이 존재해야함.

카트에 아이템 추가
POST (host)/api/cart
body = product_id, quantity)

카트 조회
GET (host)/api/cart

카트 갯수 수정
PATCH (host)/api/cart
body = cart_id, quantity

카트 삭제
DELETE (host)/api/cart
```

### Product Request

```python
특정 제품에 대한 상세 정보
GET (host)/api/product/(product_group_id)

제품 리스트 쿼리 요청
GET (host)/api/product_groups/(Query)
Query = category_id, featured_id
```

### User Request
```python
회원가입
POST (host)/api/user/signup
body = email, password

로그인
POST (host)/api/user/signin
body = email, password
```
