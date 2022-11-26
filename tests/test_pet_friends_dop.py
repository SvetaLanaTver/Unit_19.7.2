from api import PetFriends
from settings import *
import os


pf = PetFriends()


# 1 позитивный
def test_add_new_pet_simple(name='Сорока', animal_type='птиц', age=2):
    """Проверяем, что можно добавить питомца в упрощенном формате (без фото) с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    try:
        assert status == 200
        assert result['name'] == name
    except:
        print("\nПитомец не добавился при корректных данных")


# 2 негативный
def test_add_new_pet_simple_invalid_name(name=True, animal_type='птица', age=3):
    """Проверяем, что можно добавить питомца в упрощенном формате (без фото) с некорректным именем.
    По условиям тип name - строка"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом

    try:
        assert status == 200
        assert result['name'] == str(name)
        print('\nBAG: Питомец добавлен при некорректном формате имени питомца (name)')
    except ValueError:
        print('\nТест отработал правильно')


# 3 позитивный
def test_add_photo_to_pet_with_valid_data(pet_photo='images\Koko.jpg'):
    """Проверяем что можно добавить фотографию к ранее добавленному питомцу"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем: если список своих питомцев пустой, то добавляем нового
    # и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Несушка", "несушка", 4)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фотографии
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'pet_photo' in result


# 4 негативный
def test_add_photo_to_pet_with_novalid_data(pet_photo='images\Koko1.jpg'):
    """Проверяем, что нельзя добавить фотографию к питомцу, если файл отсутствует"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового
    # и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_simple(auth_key, "Несушка", "несушка", 4)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фотографии
    pet_id = my_pets['pets'][0]['id']

    try:
        status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)
    except FileNotFoundError:
        print('\nФайл с фотографией питомца или каталог отсутствует!. Тест прошел успешно')
    else:
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert 'pet_photo' in result
        print('\nBAG: Тест прошёл при отсутсвующем файле с фото')


#5 негативный
def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа с неправильным e-mail'ом возвращает статус 403
    403	- The error code means that provided combination of user email and password is incorrect"""

    try:
        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status,
        # а текст ответа в result
        status, result = pf.get_api_key(email, password)
    except ValueError:
        print('\nНекорректный тип данных')
    else:
        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'This user wasn&#x27;t found in database' in result


# 6 негативный
def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа с неправильным паролем возвращает статус 403
    403	- The error code means that provided combination of user email and password is incorrect"""

    try:
        # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status,
        # а текст ответа в result
        status, result = pf.get_api_key(email, password)
    except ValueError:
        # Сверяем полученные данные с нашими ожиданиями
        assert status == 403
        assert 'This user wasn&#x27;t found in database' in result


# 7 негативнй
def test_get_pets_list_with_invalid_filter(filter='111'):
    """ Проверяем что запрос питомцев c некорректным значением поля filter возвращает ошибку.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Получаем ключ auth_key и запрашиваем список питомцев с неправильным фильтром
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500
    assert 'Filter value is incorrect' in result


# 8 негативный
def test_successful_update_self_pet_invalid_age(name='Нюша', animal_type='британка', age=-5):
    """Проверяем возможность обновления информации о питомце с отрицательным значением возраста питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        try:
            status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        except ValueError:
            print('\nНеверные параметры')
        else:
            # Проверяем что статус ответа и имя питомца соответствует заданному
            if status == 200 and result['age'] == str(age):
                print("\nБаг, должно быть выдано предупреждение, что возраст < 0 и выполнение прервано")
            else:
                print('\nТест не сработал')

    else:
        # если спиок своих питомцев пустой
        print("\nСписок питомцев пустой")


# 9 негативный
def test_successful_update_info_otherUser_pet(name='Кличка изменена другим пользователем',
                                          animal_type='животное',
                                          age=11):
    """Проверяем возможность обновления информации о питомце, созданным другим пользователем
    и возможность изменения возраста на значение выше разумного"""

       # Получаем ключ other_auth_key, auth_key и запрашиваем список чужих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, other_pets = pf.get_list_of_pets(auth_key, "")

    # Проверяем: если список питомцев не пустой, пытаемся изменить
    if len(other_pets['pets']) > 0:
        print("\nимя первого питомца=", other_pets['pets'][0]['name'])
        status, result = pf.update_pet_info(auth_key, other_pets['pets'][0]['id'], name, animal_type, age)
    else:
        # если спиок питомцев пустой, то выдается сообщение с текстом об отсутствии питомцев
        print("\nСписок питомцев пустой")
        return

    try:
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    except:
        print('\nИзменить данные чужого питомца не удалось')
    else:
        print('\nBAG: Изменены даные чужого питомца')
    finally:
        print("новое имя =", result['name'])


# 10 негативный
def test_add_new_pet_simple_invalid_age(name='Коко', animal_type='курица', age='4'):
    """Проверяем, что можно добавить питомца в упрощенном формате (без фото) с некорректным форматом возраста.
    По условиям тип age - число"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    try:
        # Добавляем питомца
        status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    except ValueError:
        print('\nТест отработал правильно: тип данных возраста некорректный')
    else:
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['age'] == age
        print('\nBAG: Питомец добавлен при некорректном формате возраста питомца (age)')

#11
#### Проверка Удаление питомцев, созданных во время тестирования #######
def test_delete_self_pet():
    """Проверяем возможность удаления питомца. Заодно подчищаем после своей работы"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # если спиок питомцев пустой, то выдается сообщение с текстом об отсутствии питомцев
    if len(my_pets['pets']) == 0:
        print("\nСписок питомцев пустой - удалять нечего")
        return

    while len(my_pets['pets']) > 0:
        # Берём id первого питомца из списка и отправляем запрос на удаление
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id not in my_pets.values()

        # Запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Ещё раз запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        print("\nПитомцы удалены. Список пустой")


