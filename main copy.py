import concurrent.futures
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from fake_useragent import UserAgent
import pandas as pd
import datetime
import bs4
import os

csvFile = "products.csv"

urls = [
    "https://www.amazon.com.br/Inteligente-AGL-Wi-Fi-metros-Compat%C3%ADvel/dp/B08VLFBX6C/?_encoding=UTF8&pd_rd_w=YVIrN&content-id=amzn1.sym.07271deb-23ee-498c-8f97-f25954bcc083&pf_rd_p=07271deb-23ee-498c-8f97-f25954bcc083&pf_rd_r=H8TETVHT3MH9RTPYYJQC&pd_rd_wg=9Fe9y&pd_rd_r=f83163c2-65a6-432d-8de5-e21b1fd03941&ref_=pd_gw_ci_mcx_mr_hp_atf_m",
    "https://www.amazon.com.br/Inteligente-AGL-metros-Compat%C3%ADvel-Branco/dp/B08VL94QQT/?_encoding=UTF8&pd_rd_w=YVIrN&content-id=amzn1.sym.07271deb-23ee-498c-8f97-f25954bcc083&pf_rd_p=07271deb-23ee-498c-8f97-f25954bcc083&pf_rd_r=H8TETVHT3MH9RTPYYJQC&pd_rd_wg=9Fe9y&pd_rd_r=f83163c2-65a6-432d-8de5-e21b1fd03941&ref_=pd_gw_ci_mcx_mr_hp_atf_m",
]

nomeProdutos = []
precoProdutos = []
dataProdutos = []

def initDrivers():
    options = Options()
    options.headless = True

    global driver
    driver = webdriver.Firefox(options=options)

def scraper():	
    for i in range(len(urls)):
        driver.get(urls[i])

        content = driver.page_source
        soup = bs4.BeautifulSoup(content, "html.parser")
        items = soup.find_all("div", {"class": "home_improvement pt_BR"})

        for product in items:
            
            tempNome = (product.find("span", {"class": "a-size-large product-title-word-break"}).text).strip()
            tempPreco = product.find("span", {"class": "a-offscreen"}).text
            dataAtual = datetime.datetime.now()
            dataAtual = dataAtual.strftime("%x") + " " + dataAtual.strftime("%X")
            
            
            nomeProdutos.append(tempNome)
            precoProdutos.append(tempPreco)
            dataProdutos.append(dataAtual)
            # gpus.append({
            #     "Produto": (product.find("span", {"class": "a-size-large product-title-word-break"}).text).strip(),
            #     "Preco": product.find("span", {"class": "a-offscreen"}).text,
            #     # "change": 0
            # })
    
def saveDataFrame():
    df = pd.DataFrame({'Data': dataProdutos, 'Nome': nomeProdutos, 'Preco': precoProdutos})    
    df.to_csv(csvFile, mode="a", index=False, encoding='utf-8', header=False)

# def openDataFrameHistory():
#     df = pd.read_csv(csvFile)

    # idx = df.groupby(['Nome', 'Preco'])["Data"].idxmin()

    # print(df.loc[idx])

    # tempDifferentNames = [{}]

if __name__ == "__main__":
    print(os.path.dirname(__file__))
    initDrivers()
    scraper()
    saveDataFrame()

    # openDataFrameHistory()