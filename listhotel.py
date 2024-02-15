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

header = ["Company Name", "Address", "Phone No.", "Email"]
g = open("listhotel.csv", "w", newline='', encoding="utf-8")
row_writer = csv.writer(g)
row_writer.writerow(header)

current_page = 1
all_company_name = []
all_company_address = []
base_url = " https://www.halal.gov.my/v4/"
for current_page in range(1,20):
    # 145, 160 prob sebab emailnya = null
    url = f"https://www.halal.gov.my/v4/index.php?data=ZGlyZWN0b3J5L2luZGV4X2RpcmVjdG9yeTs7Ozs=&negeri=&category=PE&page={current_page}&cari=hotel"
    # BG=Barang Gunaan, FM=Farmaseutikal, KO=Kosmetik, OEM=Pengilangan Kontrak / Original, PE=Premis, PL=Logistik, PR=Produk Makanan / Minuman, PS=Rumah Sembelihan
    response = requests.get(url, headers=headers)
    doc = html.fromstring(response.text)
    query = doc.xpath("//li[@class='clearfix search-result-data']")
    print(doc)
    print(query)

    for i in query:
        # # ni nk dapatkan nama
        name = i.xpath("./div[@class='search-details']/span[@class='company-name']/text()")[0]
        # ni nk dapatkan alamat
        address = i.xpath("./div[@class='search-details']/span[@class='company-address']/text()")
        modal = i.xpath("substring-before(substring-after((./div[@class='search-company']/img/@onclick),\"openModal('\"),\"'\")")
        url2 = f"{base_url}{modal}"
        response2 = requests.get(url2, headers=headers)
        doc2 = html.fromstring(response2.text)
        queryphoneno = doc2.xpath("//table/tr[5]/td[2][@bgcolor]/text()")
        # [0]=array & tak ade [0]=collect semua dan tanda ['']
        queryemail = doc2.xpath("//table/tr[7]/td[2][@bgcolor]/text()")
        new_address = ''.join(address)
        row_writer.writerow([name, new_address, queryphoneno, queryemail])
        all_company_name.append(name)
        all_company_address.append(new_address)
