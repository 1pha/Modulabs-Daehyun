import argparse
import os
from newspaper import Article
import requests
import pandas as pd
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description='Semi-Automated News Crawler')

parser.add_argument('--page_num', '-p', type=int, default=100,
                    help='Number of pages to crawl')
parser.add_argument('--code', '-c', default=101,
                    help='Which code to take')
parser.add_argument('--date', '-d', type=int, default=20201119,
                    help='Format of YYYYMMDD 8-digit date. Default 20201119')
args = parser.parse_args()

def make_urllist(page_num, code, date): 
    urllist= []
    for i in range(1, page_num + 1):
        url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1='+str(code)+'&date='+str(date)+'&page='+str(i)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
        news = requests.get(url, headers=headers)

        # BeautifulSoup의 인스턴스 생성합니다. 파서는 html.parser를 사용합니다.
        soup = BeautifulSoup(news.content, 'html.parser')

        # CASE 1
        news_list = soup.select('.newsflash_body .type06_headline li dl')
        # CASE 2
        news_list.extend(soup.select('.newsflash_body .type06 li dl'))

        # 각 뉴스로부터 a 태그인 <a href ='주소'> 에서 '주소'만을 가져옵니다.
        for line in news_list:
            urllist.append(line.a.get('href'))
        
    return urllist


def make_data(urllist, code):
    text_list = []
    for url in urllist:
        article = Article(url, language='ko')
        article.download()
        article.parse()
        text_list.append(article.text)

    df = pd.DataFrame({'news': text_list})

    df['code'] = idx2word[str(code)]
    
    return df


def make_total_data(page_num, code_list, date):
    df = None

    for code in code_list:
        url_list = make_urllist(page_num, code, date)
        df_temp = make_data(url_list, code)
        print(str(code)+'번 코드에 대한 데이터를 만들었습니다.')

        if df is not None:
            df = pd.concat([df, df_temp])
        else:
            df = df_temp

    return df


def save_df(df, page_num, code, date):

    fname = f'{page_num}_{code}_{date}.csv'
    csv_path = './news_crawler/news_'+fname

    df.to_csv(csv_path, index=False)


if __name__=="__main__":


    code_list = [101, 102, 103, 105]
    idx2word = {
        '101' : '경제',
        '102' : '사회',
        '103' : '생활/문화',
        '105' : 'IT/과학'
    }

    code = list(map(int, args.code.split())) if len(args.code) >= 3 else code_list
    page_num, date = args.page_num, args.date

    df = make_total_data(page_num, code, date)
    save_df(df, page_num, code, date)