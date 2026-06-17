import time
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
plt.rcParams["font.family"] = "Microsoft JhengHei"

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.ptt.cc"

def get_latest_page():
    url = f"{base_url}/bbs/MobilePay/index.html"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    prev_href = soup.find("a", string="‹ 上頁")["href"]
    return int(prev_href.split("index")[1].split(".html")[0]) + 1

def crawl_ptt_pay(pages):
    latest = get_latest_page()
    titles = [] 
    print(f"最新頁碼是 {latest}，開始往前抓 {pages} 頁...")

    for i in range(pages):
        target_page = latest - i
        url = f"{base_url}/bbs/MobilePay/index{target_page}.html"
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        for div in soup.find_all("div", class_="title"):
                a = div.find("a")
                if a: 
                    titles.append(a.text.strip())
        print(f"正在讀取第 {target_page} 頁...")
        time.sleep(0.5)
        
    return titles

def analyze_and_plot(titles):
    df = pd.DataFrame(titles, columns=["title"])   
    jk = df["title"].str.contains("街口").sum()
    line = df["title"].str.contains("line", case=False).sum()
    ipass = df["title"].str.contains("ipass|一卡通", case=False).sum()
    print(f" [統計結果] 街口: {jk} 篇 | LINE Pay: {line} 篇 | 一卡通: {ipass} 篇")

    labels = ["街口支付", "LINE Pay", "iPASS 一卡通"]
    values = [jk, line, ipass]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.bar(labels, values, color=["#ff7f7f", "#7fbfff", "#7fff7f"])
    ax2.pie(values, labels=labels, autopct="%1.1f%%")   
    plt.show() 

if __name__ == "__main__":
    page_count = int(input("請輸入想抓取頁數:"))  
    data = crawl_ptt_pay(page_count)      
    analyze_and_plot(data)
