import pandas as pd
from requests_html import HTMLSession
import random

def get_info(s, user_agents, url, posts, comments_list):
    # --- HEADERS --- 
    random_user_agent = random.choice(user_agents)
    headers = {
    'User-Agent': random_user_agent
    }
    
    try:
        # --- SENDING REQUEST ---
        r = s.get(url, headers=headers)
        r.html.render(timeout=320)
        if int(url[-1])%2==0:
            print(url)
        else:
            pass
        
        # --- POST ---
        title = r.html.xpath('//*[@id="container"]/section/article[2]/div[1]/header/div/h3/span[2]', first=True).text
        upvote = r.html.xpath('//*[@id="container"]/section/article[2]/div[1]/div/div[3]/div[1]/div[1]/div', first=True).text.split('\n')[0]
        downvote = r.html.xpath('//*[@id="container"]/section/article[2]/div[1]/div/div[3]/div[1]/div[2]/div', first=True).text

        info = r.html.xpath('//*[@id="container"]/section/article[2]/div[1]/header/div', first=True)
        creator_name = info.find('span.nickname', first=True).text        
        creation_date = info.find('span.gall_date', first=True).text.split(' ')[0].replace('.', '-')
        try:
            creator_ip = info.find('span.ip', first=True).text.strip('()')
        except:
            creator_ip = 'hidden'

        try:
            content = r.html.find('div.write_div', first=True).text.replace('\n', ' ').replace('\xa0', ' ')
        except:
            content = 'no content'
        
        posts.append([title, creator_name, creator_ip, content, upvote, downvote, creation_date])
        
        # --- COMMENTS ---
        all_comments = r.html.find('ul.cmt_list', first=True)
        if all_comments:
            comments = all_comments.find('li.ub-content')
            for comment in comments:
                
                # find comm info
                comm_info = comment.find('span.nickname', first=True)
                if comm_info:
                    comm_name = comm_info.find('em', first=True).text
                    try:    
                        comm_ip = comm_info.find('span.ip', first=True).text.strip('()') 
                    except:
                        comm_ip = 'hidden'
                else:
                    comm_info = None
                
                # find comm content  
                try:
                    comm_content = comment.find('p[class*="usertxt ub-word"]', first=True).text.replace('\n', ' ')
                except:
                    comm_content = None
                
                # find comm creation date
                try:
                    comm_date = comment.find('span.date_time', first=True).text.split(' ')[0].replace('.', '-')
                    if len(comm_date) >= 5:
                        comm_date = '2023-' + comm_date
                    else:
                        pass
                except:
                    comm_date = None

                # --- MAKING A LIST ---                
                if comm_info == comm_content == comm_date or comm_info.text == '댓글돌이':
                    comm_info, comm_content, comm_date, comm_name, comm_ip = None, None, None, None, None
                    pass
                else:
                    comments_list.append([title, comm_name, comm_ip, comm_content, comm_date])
                    comm_info, comm_content, comm_date, comm_name, comm_ip = None, None, None, None, None
        else:
            comm_content, comm_date, comm_name, comm_ip = 'no_comments', 'no_comments', 'no_comments', 'no_comments'
            comments_list.append([title, comm_name, comm_ip, comm_content, comm_date])

    except Exception as e:
        print(str(e), '\n', url)
        pass

def get_last(s):
    url = 'https://gall.dcinside.com/board/lists/?id=bitcoins_new1&page=1&list_num=100'
    r = s.get(url)
    last = r.html.xpath('//*[@id="container"]/section[1]/article[2]/div[4]/div[1]/a[16]', first=True).attrs['href']
    return int(last.split('=')[2].split('&')[0])

def get_hrefs(s, user_agents, url, urls):
    random_user_agent = random.choice(user_agents)
    headers = {
    'User-Agent': random_user_agent
    }
    try:
        # --- SENDIND REQUEST ---
        r = s.get(url, headers=headers)
        if int(url.split('=')[-2].split('&')[0])%1000 == 0:
                print(url)
        else:
            pass
        
        # --- COLLECTING URLS --- 
        posts = r.html.find('tr[class*="ub-content us-post"]')
        if posts:
            for post in posts:
                href = post.find('a', first=True).attrs['href']
                urls.append('https://gall.dcinside.com/' + href)
        else:
            pass
    except Exception as e:
        print(str(e), '\n', url)
        pass

def get_urls(s, user_agents):
    # last = get_last(s)
    pages = [f'https://gall.dcinside.com/board/lists/?id=bitcoins_new1&page={num}&list_num=100' for num in range(1, 2)]
    urls = []
    [get_hrefs(s, user_agents, page, urls) for page in pages]
    return urls

if __name__ == '__main__':
    s = HTMLSession()
    posts = [] 
    comments = []  
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.5563.65 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'
    ]
    
    urls = get_urls(s, user_agents)
    for url in urls:
        get_info(s, user_agents, url, posts, comments)
    # --- CONVERTING INTO CSV ---
    posts_df = pd.DataFrame(posts, columns=['Title', "Creator's name", "Creator's IP", "Post's content", 'Upvotes', 'Downvotes', 'Creation date'])
    posts_df.to_csv('bitcoins_new.csv', index=False)
    
    comments_df = pd.DataFrame(comments, columns=['Title', "Commentator's name", "Commentator's IP", "Comment's content", "Comment's creation date"])
    comments_df.to_csv('comments of bicoins_new.csv', index=False)