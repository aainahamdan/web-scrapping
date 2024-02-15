from typing import TextIO

import requests
import lxml.html as html
import csv

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://www.halal.gov.my',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36 Edg/90.0.818.46',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.halal.gov.my/v4/index.php?data=ZGlyZWN0b3J5L2luZGV4X2RpcmVjdG9yeTs7Ozs=',
    'Accept-Language': 'en-US,en;q=0.9,ms;q=0.8,id;q=0.7',
}

header = ["Company Name","Kitchen", "Company Address", "Expired Date (Halal)", "Phone No.", "Email"]
g = open("food premises.csv", "w", newline='', encoding="utf-8")
row_writer = csv.writer(g)
row_writer.writerow(header)

current_page = 1
all_company_name = []
all_company_kitchen = []
all_company_address = []
all_company_date = []
base_url = " https://www.halal.gov.my/v4/"
for current_page in range(1,3):
    url = f"https://www.halal.gov.my/v4/index.php?data=ZGlyZWN0b3J5L2luZGV4X2RpcmVjdG9yeTs7Ozs=&negeri=&category=PE&page={current_page}&cari="
    # BG=Barang Gunaan, FM=Farmaseutikal, KO=Kosmetik, OEM=Pengilangan Kontrak / Original, PE=Premis, PL=Logistik, PR=Produk Makanan / Minuman, PS=Rumah Sembelihan
    # 01=jb, 02=kedah, 03=kelantan, 04=melaka, 05=n9, 06=pahang, 07=pp, 08=perak, 09=perlis, 10=selangor, 11=trengganu, 12=sabah, 13=srwk, 14=kl, 15= labuan, 16=putrajaya
    response = requests.get(url, headers=headers)
    doc = html.fromstring(response.text)
    query = doc.xpath("//li[@class='clearfix search-result-data']")
    print(query)
    print(current_page)
    for i in query:
        # # ni nk dapatkan nama
        name = i.xpath("./div[@class='search-details']/span[@class='company-name']/text()")[0]
        # nak dapatkan nama kitchen hotel
        kitchen=""
        kitchenraw = i.xpath("./div[@class='search-details']/span[@class='company-brand']/text()")
        if len(kitchenraw)>0:
            kitchen = kitchenraw[0]
        # ni nk dapatkan alamat
        address = i.xpath("./div[@class='search-details']/span[@class='company-address']/text()")
        # ni nk dapatkan tarikh
        date = i.xpath("./div[@class='search-date-expired']/text()")[0]
        modal = i.xpath("substring-before(substring-after((./div[@class='search-company']/img/@onclick),\"openModal('\"),\"'\")")
        url2 = f"{base_url}{modal}"
        response2 = requests.get(url2, headers=headers)
        doc2 = html.fromstring(response2.text)
        queryphoneno = doc2.xpath("//table/tr[5]/td[2][@bgcolor]/text()")[0]
        # [0]=array & tak ade [0]=collect semua dan tanda ['']
        queryemail = " "
        queryemailraw = doc2.xpath("//table/tr[7]/td[2][@bgcolor]/text()")
        if len(queryemailraw) > 0:
            queryemail = queryemailraw[0]
        #queryemail = doc2.xpath("//table/tr[7]/td[2][@bgcolor]/text()")
        new_address = ''.join(address)
        row_writer.writerow([name,kitchen, new_address, date, queryphoneno, queryemail])
        all_company_name.append(name)
        all_company_kitchen.append(kitchen)
        all_company_address.append(new_address)
        all_company_date.append(date)