import concurrent.futures
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from fake_useragent import UserAgent
import pandas as pd
import datetime
import bs4
import matplotlib.pyplot as plt
import numpy as np

csvFile = "products.csv"

possibleChoices = ["S", "s", "N", "n"]

urls = [
    "https://www.amazon.com.br/Inteligente-AGL-Wi-Fi-metros-Compat%C3%ADvel/dp/B08VLFBX6C/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=YZLACH9O04UI&keywords=fita+led+agl&qid=1669857602&qu=eyJxc2MiOiIyLjQzIiwicXNhIjoiMS42OSIsInFzcCI6IjEuODIifQ%3D%3D&sprefix=fita+led+ag%2Caps%2C213&sr=8-1&ufe=app_do%3Aamzn1.fos.6121c6c4-c969-43ae-92f7-cc248fc6181d",
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
        items = soup.find_all("div", {"class": "pt_BR"})

        for product in items:
            
            tempNome = (product.find("span", {"class": "a-size-large product-title-word-break"}).text).strip()
            tempPreco = product.find("span", {"class": "a-offscreen"}).text[2:].replace(",", ".")
            dataAtual = datetime.datetime.now()
            dataAtual = dataAtual.strftime("%x") + " " + dataAtual.strftime("%X")
            

            nomeProdutos.append(tempNome)
            precoProdutos.append(tempPreco)
            dataProdutos.append(dataAtual)


    df = pd.DataFrame({'Data': dataProdutos, 'Nome': nomeProdutos, 'Preco': precoProdutos})    
    df.to_csv(csvFile, mode="a", index=False, encoding='utf-8', header=False)
        # df.to_csv(csvFile + "-" + str(i) + ".csv", mode="a", index=False, encoding='utf-8', header=False)
            
            # gpus.append({
            #     "Produto": (product.find("span", {"class": "a-size-large product-title-word-break"}).text).strip(),
            #     "Preco": product.find("span", {"class": "a-offscreen"}).text,
            #     # "change": 0
            # })
    
# def saveDataFrame():

def openDataFrameHistory():
    
    # for i in range(len(urls)):
    global df
    df = pd.read_csv(csvFile, usecols=["Data", "Nome", "Preco"])

    print("Preços registrados: ")
    result = df.groupby(["Nome"]).agg({'Preco': ['min', 'max']})
    # result = df.groupby(["Nome"]).agg({'Preco': ['min', 'idxmin', 'max', 'idxmax']})
    print(result)

    print("Menores preços registrados em: ")
    print(df.loc[df.groupby('Nome')['Preco'].idxmin()])
    print("Maiores preços registrados em: ")
    print(df.loc[df.groupby('Nome')['Preco'].idxmax()])

    print("\nPreco Atual:")

    print(df.tail(len(urls)))

    # grouped = df.groupby("Nome")

    # nColunas = len(urls)
    # nLinhas = int(np.ceil(grouped.ngroups/nColunas))

    # fig, axes = plt.subplots(nrows=nLinhas, ncols=nColunas, figsize=(12,4), sharey=True)

    # for (key, ax) in zip(grouped.groups.keys(), axes.flatten()):
    #     grouped.get_group(key).plot(ax=ax)
    
    # ax.legend()

def plotGraph():
    df.set_index('Data', inplace=True)
    df.groupby('Nome')['Preco'].plot(legend=True)

    plt.title("Variação Preços")

    plt.show()

if __name__ == "__main__":
    # print(os.path.dirname(__file__))
    print("Iniciando Driver")
    initDrivers()
    print("Buscando Preços...")
    scraper()
    # saveDataFrame()

    openDataFrameHistory()
    while True:
        choose = input("Deseja mostrar gráfico com variação dos preços? (S/N) ")
        if choose not in possibleChoices:
            print("Escolha inválida")
        
        if choose == "S" or choose == "s":
            plotGraph()
            break
        else:
            break
