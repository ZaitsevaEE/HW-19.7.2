from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data_without_photo(name='Коржик', animal_type='Дворянин',
                                     age='14'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными с фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_photo_pet_with_valid_data(pet_id='62eb7493-f31d-4fc2-a646-8a01016e0db4', pet_photo='images/CatNew.jpg'):
    """Проверяем что можно добавить питомца с корректными данными с добавлением фото питомца, у которого его не было"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_photo_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

 # негативные тесты:
  #1
def test_get_auth_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
        """Проверяем запрос с невалидным паролем и с валидным емейлом.
        Проверяем нет ли ключа в ответе"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'key' not in result
        print(result)

  #2
def test_get_auth_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
        """Проверяем запрос с невалидным паролем и с валидным емейлом.
        Проверяем нет ли ключа в ответе"""

        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
        status, result = pf.get_api_key(email, password)

        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'key' not in result
        print(result)

  #3
def test_get_auth_key_for_empty_reg_fields(email='', password=''):
    '''Доступ к веб приложению без ввода адреса электронной почты и пароля.
     Запрос API на возврат статуса 403 в связи с отсутствием в запросе данных пользователя'''

    # Отправляем запрос и сохраняем ответ с кодом статуса в status, а текст в result
    status, result = pf.get_api_key(email, password)

    # Сверяем ожидаемый и фактический результат
    assert status == 403
    print(result)

  #4
def test_get_auth_key_with_invalid_key(filter="my_pets"):
    """ Проверяем, что запрос "моих питомцев" при запросе с неверно указанным ключом ничего не возвращает """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets({'key': '111222333555666'}, filter)
    assert status == 403
    print(result)

  #5
def test_get_all_pets_with_wrong_filter(filter='mymy_pets'):
    """ Проверяем запрос всех питомцев с ошибкой в параметре filter - задвоение "mymy".
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список пустой."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
    assert 'pets' not in result
    print(result)

  #6
def test_add_new_pet_invalid_age(name='Снежный Барс', animal_type='дикая кошка', age='99999999999999'):
    '''Проверка добавления нового питомца без фото с некорректными данными возраста:
    слишком большое число.'''

    #Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    #Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['age'] !=0
    print(result)
    #баг - животное не должно добавляться нереального возраста.

  #7
def test_add_new_pet_negative_age(name='Рваное Ухо', animal_type='собака', age='-100'):
    '''Проверка добавления нового питомца без фото с некорректными данными вораста:
    отрицательное число.'''

    #Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    #Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['age'] !=0
    print(result)
    #баг - животное не должно добавляться нереального возраста.

 #8
def test_add_new_pet_without_name(name='', animal_type='двортерьер', age='13'):
    """Проверяем что можно добавить питомца c пустым полем Имя"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом. Ожидаем, что питомца без обязательного поля создать невозможно
    assert status == 200
    assert result['name'] == ''
    print(result)
    # баг - животное не должно добавляться ,без обязательного поля

 #9
def test_add_new_empty_pet(name='', animal_type='', age=''):
    '''Проверка добавления нового питомца без данных.'''

    # Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    print(result)
    # баг - животное не должно добавляться без обязательных полей для заполнения

 #10
def test_add_new_pet_with_long_name(name='Очень длинное имечко у меняяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяя',
                                    animal_type='сибирская',
                                    age='1'):
    """Проверка, что нельзя добавить питомца с именем длиннее 50 символов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age,)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['name']) > 50

    print(result)
    print(len(result['name']))
 #'Баг - сайт позволяет добавить питомца с именем длиннее 50 символов'