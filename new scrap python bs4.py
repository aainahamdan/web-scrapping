from bs4 import BeautifulSoup
import requests, openpyxl
import pandas as pd 

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'scrap_halal.gov'
sheet_header = ['Company Name', 'Company Address', 'Date Expired']

try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    # BG=Barang Gunaan, FM=Farmaseutikal, KO=Kosmetik, OEM=Pengilangan Kontrak / Original, PE=Premis, PL=Logistik, PR=Produk Makanan / Minuman, PS=Rumah Sembelihan
    # 01=jb, 02=kedah, 03=kelantan, 04=melaka, 05=n9, 06=pahang, 07=pp, 08=perak, 09=perlis, 10=selangor, 11=trengganu, 12=sabah, 13=srwk, 14=kl, 15= labuan, 16=putrajaya
    source = requests.get('https://www.halal.gov.my/v4/index.php?data=ZGlyZWN0b3J5L2luZGV4X2RpcmVjdG9yeTs7Ozs=&negeri=01&category=PR&page=&cari=','PR', headers=headers)
    source.raise_for_status()
    # print(source) #to check if the url right can be access
    soup = BeautifulSoup(source.text, 'html.parser')
    # print(soup) #to check the soup can be used or not

    # halalgov = soup.find('div', class_='content-wrap main-content-wrap')
    # print(halalgov)


    company_name = [item.text.strip() for item in soup.select('span.company-name')]
    df_name = pd.DataFrame(company_name)
    # print(df_name)
    company_address = [item.text.strip() for item in soup.select('span.company-address')]
    df_address = pd.DataFrame(company_address)
    # print(df_address)
    date_expired = [item.text.rstrip(".") for item in soup.select('div.search-date-expired')[1:]]
    df_date = pd.DataFrame(date_expired)
    # print(df_date)

    # df_name.rename(columns= {'0':"Company Name"})
    # df_address.rename(columns= {'0':"Company Address"})
    # df_date.rename(columns= {'0':"Certification Expired Date"})

except Exception as e:
    print(e)

with pd.ExcelWriter("Bismillah.xlsx", engine="openpyxl") as writer:
    df_name.to_excel(writer, sheet_name='Sheet_1', header=False, index=False)
    df_address.to_excel(writer, sheet_name='Sheet_1', startcol=1, header=False, index=False)
    df_date.to_excel(writer, sheet_name='Sheet_1', startcol=2, header=False, index=False)

print('Fin')