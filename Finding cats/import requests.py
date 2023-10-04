import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Функция для поиска всех фотографий котиков на странице и следовании по ссылкам на другие страницы
def find_cat_photos_recursive(url, visited_urls, cat_image_urls, max_cat_photos=100):
    try:
        # Отправляем GET-запрос к указанному URL
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            # Используем BeautifulSoup для парсинга HTML-кода страницы
            soup = BeautifulSoup(response.content, 'html.parser')

            # Находим все изображения на текущей странице
            images = soup.find_all('img')

            # Перебираем найденные изображения и проверяем, содержат ли атрибут alt ключевое слово "cat" (независимо от регистра)
            for image in images:
                alt_text = image.get('alt', '')
                if 'cat' in alt_text.lower():
                    cat_image_urls.append(image['src'])

                    # Если достигнуто максимальное количество фотографий, завершаем поиск
                    if len(cat_image_urls) >= max_cat_photos:
                        return

            # Добавляем текущий URL в список посещенных страниц
            visited_urls.add(url)

            # Находим все ссылки на другие страницы на текущей странице
            links = soup.find_all('a', href=True)

            # Перебираем найденные ссылки
            for link in links:
                href = link.get('href', '')

                # Преобразуем относительные ссылки в абсолютные
                absolute_url = urljoin(url, href)

                # Проверяем, что ссылка ведет на сайт Википедии и не была посещена ранее
                if absolute_url.startswith('https://en.wikipedia.org') and absolute_url not in visited_urls:
                    # Рекурсивно вызываем функцию для следующей страницы
                    find_cat_photos_recursive(absolute_url, visited_urls, cat_image_urls, max_cat_photos)

    except Exception as e:
        print(f'Произошла ошибка: {str(e)}')

# Начальный URL Википедии о котиках (на английском языке)
start_url = 'https://en.wikipedia.org/wiki/Cat'

# Создаем множество для отслеживания посещенных URL
visited_urls = set()

# Создаем список для хранения URL фотографий котиков
cat_image_urls = []

# Максимальное количество фотографий, которое нужно найти
max_cat_photos = 10

# Вызываем функцию для поиска фотографий котиков с ограничением
find_cat_photos_recursive(start_url, visited_urls, cat_image_urls, max_cat_photos)

# Создаем и открываем текстовый файл для записи URL фотографий
with open('cat_photos.txt', 'w', encoding='utf-8') as file:
    # Записываем найденные фотографии в файл
    for i, photo_url in enumerate(cat_image_urls, 1):
        file.write(f'Фото котика {i}: {photo_url}\n')

print(f'Ссылки на первые {max_cat_photos} фотографий котиков сохранены в файл cat_photos.txt')
