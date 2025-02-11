import time
import random
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def google_search(api_key, search_engine_id, keyword, target_url):
    """Tìm kiếm từ khóa trên Google Custom Search API"""
    search_url = f"https://www.googleapis.com/customsearch/v1?q={quote(keyword)}&key={api_key}&cx={search_engine_id}"
    headers = {"User-Agent": UserAgent().random}

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[ERROR] Không thể truy cập API (Status Code: {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Lỗi kết nối API: {e}")
        return None

    data = response.json()
    results = data.get("items", [])

    for index, result in enumerate(results, start=1):
        real_url = result.get("link", "")
        print(f"[INFO] Rank {index}: {real_url}")
        if target_url in real_url:
            print(f"[SUCCESS] Tìm thấy {target_url} ở vị trí {index}, đang truy cập...")
            return real_url

    print(f"[FAIL] Không tìm thấy {target_url} trong kết quả.")
    return None

def simulate_user_behavior(url):
    """Giả lập hành vi người dùng khi truy cập trang web"""
    print(f"[INFO] Đang truy cập: {url}")

    # Giả lập thời gian ở lại trang (15 - 20 giây)
    stay_time = random.randint(15, 20)
    for i in range(stay_time, 0, -1):
        print(f"[INFO] Đang ở lại trang... {i}s", end="\r")
        time.sleep(1)
    print("\n[INFO] Đã hoàn thành thời gian ở lại trang.")

    # Giả lập cuộn trang
    print("[INFO] Giả lập cuộn trang xuống cuối...")
    time.sleep(random.randint(5, 15))

    # Giả lập click vào link ngẫu nhiên trên trang
    try:
        headers = {"User-Agent": UserAgent().random}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True) if "http" in a["href"]]

        if links:
            random_link = random.choice(links)
            print(f"[INFO] Click vào link ngẫu nhiên: {random_link}")
            time.sleep(random.randint(10, 16))
        else:
            print("[INFO] Không tìm thấy link nào trên trang.")
    except Exception as e:
        print(f"[ERROR] Lỗi khi quét link trên trang: {e}")

def main():
    """Chạy vòng lặp tìm kiếm và thực hiện hành động"""
    api_key = input("Nhập API Key của Google Custom Search: ").strip()
    search_engine_id = input("Nhập Search Engine ID: ").strip()
    keywords = input("Nhập danh sách từ khóa (cách nhau bằng dấu phẩy): ").split(",")
    target_url = input("Nhập URL mục tiêu: ").strip()

    while True:
        for keyword in keywords:
            keyword = keyword.strip()
            print(f"\n[INFO] Đang tìm kiếm từ khóa: {keyword}")
            found_url = google_search(api_key, search_engine_id, keyword, target_url)

            if found_url:
                simulate_user_behavior(found_url)

            print("[INFO] Chờ 15s trước lần tìm kiếm tiếp theo...\n")
            time.sleep(15)  # Delay 1 phút

        print("[INFO] Hoàn thành một vòng lặp, tiếp tục vòng lặp mới...\n")

if __name__ == "__main__":
    main()
