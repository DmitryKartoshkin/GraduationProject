import pytest

from ProductOrderingService.models import Shop, Category, Product, User, Contact


@pytest.mark.django_db
def test_get_one_shop(client, data_factory):
    """Проверка получения одного магазина"""
    # Arrange
    shops = data_factory('Shop', _quantity=5)
    # Act
    shop = Shop.objects.all()
    response = client.get(f'/api/v1/shop/{shop[3].id}/')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['name'] == shop[3].name
    assert len(data['name']) <= 50


@pytest.mark.django_db
def test_get_many_shop(client, data_factory):
    """Проверка получения списка магазина"""
    # Arrange
    shops = data_factory('Shop', _quantity=10)
    # Act
    response = client.get(f'/api/v1/shop/')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert len(data) == len(shops)

    # for i, s in enumerate(data):
    #     assert shop['name'] == shops[i].name


@pytest.mark.django_db
def test_get_one_category(client, data_factory):
    """Проверка получения одной категории товара"""
    # Arrange
    categoryes = data_factory('Category', _quantity=5)
    # Act
    category = Category.objects.all()
    response = client.get(f'/api/v1/category/{category[1].id}/')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['name'] == category[1].name
    assert len(data['name']) <= 40


@pytest.mark.django_db
def test_get_many_category(client, data_factory):
    """Проверка получения списка категорий товара"""
    # Arrange
    categoryes = data_factory('Category', _quantity=5)
    # Act
    response = client.get(f'/api/v1/category/')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert len(data) == len(categoryes)


@pytest.mark.django_db
def test_get_one_product(client, data_factory):
    """Проверка получения одного товара"""
    # Arrange
    categoryes = data_factory('Category', _quantity=5)
    products = data_factory('Product', _quantity=5, category_id=3)
    # Act
    product = Product.objects.all()
    response = client.get(f'/api/v1/products/{product[1].id}/')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['name'] == product[1].name
    assert len(data['name']) <= 80


@pytest.mark.django_db
def test_get_many_category(client, data_factory):
    """Проверка получения списка товаров"""
    # Arrange
    categoryes = data_factory('Category', _quantity=5)
    products = data_factory('Product', _quantity=5, category_id=3)
    # Act
    response = client.get(f'/api/v1/products/')
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert len(data) == len(products)

@pytest.mark.django_db
def test_get_contact_not_authenticate(client, data_factory):
    """Проверка получения списка товаров"""
    # Arrange
    users = data_factory('ProductOrderingService.User', _quantity=5)
    contacts = data_factory('Contact', _quantity=5, user_id=2)
    # Act
    response = client.get(f'/api/v1/contacts/')
    # Assert
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_contact_many_authenticate(client, data_factory):
    """Проверка получения списка товаров"""
    # Arrange
    users = data_factory('ProductOrderingService.User', _quantity=5)
    contacts = data_factory('Contact', _quantity=5, user_id=2)
    # Act
    user = User.objects.get(email=users[1])
    client.force_authenticate(user=user)

    response = client.get(f'/api/v1/contacts/')
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) == len(contacts)

@pytest.mark.django_db
def test_get_contact_many_authorization(client, data_factory):
    """Проверка получения списка товаров"""
    # Arrange
    users = data_factory('ProductOrderingService.User', _quantity=5)
    contacts = data_factory('Contact', _quantity=5, user_id=2)
    # Act
    user = User.objects.get(email=users[2])
    client.force_authenticate(user=user)

    response = client.get(f'/api/v1/contacts/')
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert len(data) != len(contacts)



@pytest.mark.django_db
def test_get_contact_one(client, data_factory):
    """Проверка получения списка товаров"""
    # Arrange
    users = data_factory('ProductOrderingService.User', _quantity=5)
    contacts = data_factory('Contact', _quantity=5, user_id=2)
    # Act
    user = User.objects.get(email=users[1])
    client.force_authenticate(user=user)
    contact = Contact.objects.all()
    response = client.get(f'/api/v1/contacts/{contact[1].id}/')
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data['city'] == contact[1].city
    assert len(data['city']) <= 50
    assert data['street'] == contact[1].street
    assert len(data['street']) <= 100
    assert data['phone'] == contact[1].phone
    assert len(data['phone']) <= 16



