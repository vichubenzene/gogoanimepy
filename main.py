from bs4 import BeautifulSoup
import requests
import lxml
class anime:
    def _init_(self, name,episode_num):
        self.name = name
        self.episode_num = episode_num



    def search(name):
        try:
            url1 = f"https://gogoanime.pe/search.html?keyword={name}"
            response = requests.get(url1)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            result = []
            for anime in animes:
                title = anime.a["title"]
                url = anime.a["href"]
                year = str(anime.find("p", class_="released").text.strip())
                year = year.replace(" ", "")
                id = url.split('/')
                result.append({"name": f"{title}", "animeid": f"{id[2]}", "year": year})
            if result == []:
                return({"status": "204", "reason": "No search results found for the query"})
            else:
                return (result)
        except requests.exceptions.ConnectionError:
            return ({"status": "404", "reason": "Check the host's network Connection"})

    def watch(name, episode_num):
        try:
            a_id=anime.search(name)
            a_id=a_id[0]["animeid"]
            print(a_id)
            response = requests.get(f'https://gogoanime.pe/{a_id}-episode-{episode_num}')
            soup = BeautifulSoup(response.content, 'lxml')
            aki = soup.find('div', class_="anime_muti_link")
            aku = aki.findAll('a')
            result = []
            for i in aku:
                link_url = i["data-video"]
                if not link_url.startswith("https:"):
                    link_url = "https:" + link_url
                check = requests.get(link_url)
                case = {'status': check.status_code, 'Domain': (i.text.strip().replace("Choose this server", "")),
                        'url': link_url}
                result.append(case)
            results=[{"gogoanime" : {'name':a_id , 'ep':episode_num, 'url':response.url},"other_domains":result}]
            return results
        except AttributeError:
            return {"status": "400", "reason": "Invalid animeid or episode_num"}
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}


    def download(name, episode_num ):
        try:
            a_id = anime.search(name)
            a_id = a_id[0]["animeid"]
            response = requests.get(f'https://gogoanime.pe/{a_id}-episode-{episode_num}')
            soup = BeautifulSoup(response.content, 'lxml')
            aki = soup.find("li", class_="dowloads")
            links = aki.find_all("a")
            download_url ={'name':a_id , 'ep':episode_num, 'link':links[0]["href"]}
            return download_url
        except AttributeError:
            return {"status": "400", "reason": "Invalid animeid or episode_num"}
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}

    def anime_info(name) :
            try:
                animelink = 'https://gogoanime.pe/category/{}'.format(name)

                response = requests.get(animelink)
                plainText = response.text
                soup = BeautifulSoup(plainText, "lxml")
                source_url = soup.find("div", {"class": "anime_info_body_bg"}).img
                imgg = source_url.get('src')
                tit_url = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
                lis = soup.find_all('p', {"class": "type"})
                plot_sum = lis[1]
                pl = plot_sum.get_text().split(':')
                pl.remove(pl[0])
                sum = ""
                plot_summary = sum.join(pl)
                type_of_show = lis[0].a['title']
                ai = lis[2].find_all('a')  # .find_all('title')
                genres = []
                for link in ai:
                    genres.append(link.get('title'))
                year1 = lis[3].get_text()
                year2 = year1.split(" ")
                year = year2[1]
                status = lis[4].a.get_text()
                oth_names = lis[5].get_text()
                lnk = soup.find(id="episode_page")
                ep_str = str(lnk.contents[-2])
                a_tag = ep_str.split("\n")[-2]
                a_tag_sliced = a_tag[:-4].split(">")
                last_ep_range = a_tag_sliced[-1]
                y = last_ep_range.split("-")
                ep_num = y[-1]
                res_detail_search = {"title":f"{tit_url}", "year":f"{year}", "other_names":f"{oth_names}", "type":f"{type_of_show}", "status":f"{status}", "genre":f"{genres}", "episodes":f"{ep_num}", "image_url":f"{imgg}","plot_summary":f"{plot_summary}"}
                return res_detail_search
            except AttributeError:
                return {"status":"400", "reason":"Invalid animeid"}
            except requests.exceptions.ConnectionError:
                return {"status":"404", "reason":"Check the host's network Connection"}
