import sys
import time

import requests

ATTEMPTS = 10


def measure(url: str, attempts: int = ATTEMPTS) -> None:
    """
    Качает url несколько раз подряд и считает среднюю скорость.
    """

    total_bytes = 0
    total_time = 0.0

    for i in range(1, attempts + 1):
        # добавляем мусорный параметр, чтобы CDN/прокси
        # не отдавал файл из кеша и мы мерили реальную сеть, а не кеш.
        sep = "&" if "?" in url else "?"
        bust_url = f"{url}{sep}_={time.time()}"

        start = time.perf_counter()
        response = requests.get(bust_url, timeout=30)
        response.raise_for_status()

        # скачиваем всё тело
        data = response.content
        elapsed = time.perf_counter() - start

        size = len(data)
        total_bytes += size
        total_time += elapsed

        print(
            f"[{i:2}] время: {elapsed:6.3f} c  |  размер: {size / 1024 / 1024:6.2f} МБ"
        )

    avg_time = total_time / attempts
    total_mb = total_bytes / 1024 / 1024
    speed_mb = total_mb / total_time
    speed_mbit = speed_mb * 8

    print("-" * 48)
    print(f"Среднее время запроса : {avg_time:.3f} c")
    print(f"Скачано всего         : {total_mb:.2f} МБ")
    print(f"Скорость              : {speed_mb:.2f} МБ/с  ({speed_mbit:.2f} Мбит/с)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python main.py <url>")
        print(
            "Пример: python main.py https://i.pinimg.com/736x/d6/c1/26/d6c126c73600d4a81caaddbbcb6086f6.jpg"
        )
        sys.exit(1)

    measure(sys.argv[1])
