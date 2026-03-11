import requests
import string
import time

BASE_URL = "https://api-sambungkata.vercel.app/api/search"
OUTPUT_FILE = "hasil.txt"

letters = list(string.ascii_lowercase)
hasil = set()

for awalan in letters:
    for akhiran in letters:
        url = f"{BASE_URL}?awalan={awalan}&akhiran={akhiran}&sort=sort_abjad"

        try:
            r = requests.get(url, timeout=10)

            if r.status_code == 200:
                data = r.json()

                # ambil kata dari berbagai kemungkinan format response
                if isinstance(data, list):
                    for item in data:
                        hasil.add(str(item))

                elif isinstance(data, dict):
                    for v in data.values():
                        if isinstance(v, list):
                            for item in v:
                                hasil.add(str(item))

            print(f"✔ {awalan}-{akhiran} | total: {len(hasil)}")

        except Exception as e:
            print(f"✖ error {awalan}-{akhiran}: {e}")

        time.sleep(0.15)  # delay supaya tidak spam API

# simpan ke file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for kata in sorted(hasil):
        f.write(kata + "\n")

print("\nSelesai!")
print(f"Total kata: {len(hasil)}")
print(f"Tersimpan di: {OUTPUT_FILE}")
