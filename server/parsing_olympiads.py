import requests, re
from bs4 import BeautifulSoup

from models import Olympiads
from extensions import db

def parse_olympiads(start_limit, end_limit):
    output_olympiads = []
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    for activity_id in range(start_limit, end_limit+1):
        if not Olympiads.query.filter_by(id=activity_id).first():

            try:
                url = f"https://olimpiada.ru/activity/{activity_id}"
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=10
                )
                if response.status_code != 200:
                    print(f'{activity_id} error: { response.status_code }')
                    continue

                soup = BeautifulSoup(response.text, "html.parser")

                h1_tag = soup.find("h1")
                if not h1_tag:
                    continue

                olympiad_name = h1_tag.get_text(strip=True)
                subjects = []
                subject_block = soup.select_one('div.subject_tags_full')

                if subject_block:
                    subjects = subject_block.get_text(
                        separator='/',
                        strip=True
                    ).split('/')

                all_texts = [
                    link.get_text(strip=True)
                    for link in soup.select(
                        f'td a[href^="/activity/{activity_id}/events/"]'
                    )
                ]

                dates = []

                for i in range(0, len(all_texts), 2):
                    if i + 1 < len(all_texts):
                        dates.append({
                            "stage": all_texts[i],
                            "date": all_texts[i + 1]
                                .replace("...", "-")
                                .replace("\xa0", " ")
                        })


                olympiad_site = None

                for svg in soup.select("a svg"):
                    link = svg.parent
                    href = link.get("href")

                    if href and href.startswith("http"):
                        olympiad_site = href
                        break
                if not olympiad_site:
                    olympiad_site=''
                classes = ''
                if soup.find('span', class_='classes_types_a'):
                    classes = soup.find('span', class_='classes_types_a').text.split(' ')[0]
               

                level_perechnya = ""
                blocks = soup.find_all('div', class_='f_blocks')

                # Перебираем все блоки в поиске нужного текста
                for block in blocks:
                    text_perechnya = block.get_text()
                    
                    if "В Перечне Минобрнауки" in text_perechnya:
                        # Ищем слово "уровень" и цифру после него
                        match = re.search(r'уровень\s*(\d+)', text_perechnya)
                        if match:
                            level_perechnya = match.group(1) # Получит "2"
                            break # Выходим из цикла, если нашли


                olympiad = Olympiads(
                    id = activity_id,
                    title = olympiad_name,
                    subjects = subjects,
                    dates = dates,
                    classes = classes,
                    url = olympiad_site,
                    level_perechnya = level_perechnya
                )
                db.session.add(olympiad)
                db.session.commit()    
                this_olympiad = Olympiads.query.filter_by(id=activity_id).first()
                output_olympiads.append({
                    "id": this_olympiad.id,
                    "title": this_olympiad.title,
                    "subjects": this_olympiad.subjects,
                    "dates": this_olympiad.dates,
                    "classes": this_olympiad.classes,
                    "url": this_olympiad.url,
                    "level_perechnya": this_olympiad.level_perechnya
                })
                print(f'{ activity_id } parsed')

            except Exception as e:
                print(activity_id, e)
        else:
            print(f'{ activity_id } was not parsed')
            this_olympiad = Olympiads.query.filter_by(id=activity_id).first()
            output_olympiads.append({
                    "id": this_olympiad.id,
                    "title": this_olympiad.title,
                    "subjects": this_olympiad.subjects,
                    "dates": this_olympiad.dates,
                    "classes": this_olympiad.classes,
                    "url": this_olympiad.url,
                    "level_perechnya": this_olympiad.level_perechnya
                })
    return output_olympiads