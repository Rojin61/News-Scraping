from bs4 import BeautifulSoup
import requests
import json

def main():
    keyword = input("Enter a keyword to search: ")
    kathmandu_post_scrape(keyword)
    onlinekhabar_scrape(keyword)
    setopati_scrape(keyword)
    print(f"Searching {keyword}...\n")
    print("-" * 130)

    with open("kathmandu_post_articles.json", "r") as f:
        articles = json.load(f)
        if articles:
            if keyword == "@all":
                print("All articles found in Kathmandu Post:")                
            else:
                print(f"Articles related to '{keyword}' found in Kathmandu Post:")
            print("-" * 130)
            for article in articles:
                print("Title:", article['title'])
                print("Author:", article['author'])
                print(f"Link: {article['link']}\n")
        else:
            if keyword == "@all":
                print("No articles found in Kathmandu Post.")
            else:
                print(f"No articles found with the keyword '{keyword}' in Kathmandu Post.")
    print("-" * 130)

    with open("onlinekhabar_articles.json", "r") as f:
        articles = json.load(f)
        if articles:
            if keyword == "@all":
                print("All articles found in Online Khabar:")
            else:
                print(f"Articles related to '{keyword}' found in Online Khabar:")
            print("-" * 130)
            for article in articles:
                print("Title:", article['title'])
                print("Time:", article['time'])
                print(f"Link: {article['link']}\n")
        else:
            if keyword == "@all":
                print("No articles found in Online Khabar.")
            else:
                print(f"No articles found with the keyword '{keyword}' in Online Khabar.")
    print("-" * 130)

    with open("setopati_articles.json", "r") as f:
        articles = json.load(f)
        if articles:
            if keyword == "@all":
                print("All articles found in Setopati:")
            else:
                print(f"Articles related to '{keyword}' found in Setopati:")
            print("-" * 130)
            for article in articles:
                print("Title:", article['title'])
                print("Time:", article['time'])
                print(f"Link: {article['link']}\n")
        else:
            if keyword == "@all":
                print("No articles found in Setopati.")
            else:
                print(f"No articles found with the keyword '{keyword}' in Setopati.")
    print("-" * 130)

def kathmandu_post_scrape(keyword):
    kathmandu_post_articles = []

    html = requests.get("https://kathmandupost.com/politics").text
    soup = BeautifulSoup(html, "html.parser")
    block = soup.find('div', class_='block--morenews')
    articles = block.find_all('article', class_='article-image')
    
    for article in articles[:10]:
        title_tag = article.find('h3')
        title = title_tag.text if title_tag else "No title found"
        author_tag = article.find('span', class_='article-author')
        author = author_tag.text if author_tag else "No author found"
        link = article.a['href']

        with open("kathmandu_post_articles.json", "w") as f:
                json.dump(kathmandu_post_articles, f, indent=4)
        if keyword == "@all" or keyword.lower() in title.lower():
            kathmandu_post_articles.append({
                "title": title.strip(),
                "author": author.strip(),
                "link": f"https://kathmandupost.com{link}"
            })
    return kathmandu_post_articles
        
def onlinekhabar_scrape(keyword):
    onlinekhabar_articles = []

    html = requests.get("https://english.onlinekhabar.com/category/political").text
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all('div', class_ = 'ok-post-contents')

    for article in articles[:10]:
        title_tag = article.find('h2')
        title = title_tag.text if title_tag else "No title found"
        time_tag = article.find('span',class_ = 'ok-post-hours')
        time = time_tag.find('span').text if time_tag else "No time found"
        link = article.a['href']
        
        with open("onlinekhabar_articles.json", "w") as f:
            json.dump(onlinekhabar_articles, f, indent=4)
        if keyword == "@all" or keyword.lower() in title.lower():
            onlinekhabar_articles.append({
                "title": title.strip(),
                "time": time.strip(),
                "link": link
            })
    return onlinekhabar_articles

def setopati_scrape(keyword):
    setopati_articles = []

    html = requests.get("https://en.setopati.com/political").text
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find_all('div', class_='items col-md-4')

    for article in article[:10]:
        title_tag = article.find('span', class_='main-title')
        title = title_tag.text if title_tag else "No title found"
        time_tag = article.find('span', class_='time-stamp')
        time = time_tag.text if time_tag else "No time found"
        link = article.a['href']

        with open("setopati_articles.json", "w") as f:
            json.dump(setopati_articles, f, indent=4)
        
        if keyword == "@all" or keyword.lower() in title.lower():
            setopati_articles.append({
                "title": title.strip(),
                "time": time.strip(),
                "link": link
        })
    return setopati_articles

if __name__ == "__main__":
        main()