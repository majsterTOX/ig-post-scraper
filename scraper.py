from codecs import open
from fileinput import filename
from requests_html import HTMLSession
import json
from download import Hamster


class Scraper():
    def __init__(self, _username):
        self.url = f"https://i.instagram.com/api/v1/users/web_profile_info?username={_username}"
        self.headers = {"x-ig-app-id": "936619743392459"}
        self.username = _username

    def loadData(self):
        self.session = HTMLSession()
        try:
            response = self.session.get(url=self.url, headers=self.headers)
            print(
                f"[+] Establish connection host {self.url} [{response.status_code}]")
        except:
            print(
                f"[*] Failed connection host {self.url} with {response.status_code} ")
            exit()
        self.data = json.loads(response.text)

    def extractData(self):
        try:
            data = self.data
        except:
            print(f"No posts on @{self.username} or account is private!")
            exit()

        post = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]
        post_id = post["id"]
        post_short_code = post["shortcode"]
        description = post["edge_media_to_caption"]["edges"][0]["node"]["text"]

        def getValue(key_name):
            attributes = description.split("\n")
            for attr in attributes:
                attr = attr.split(": ")
                key_string = attr[0]
                if key_name == key_string:
                    value = attr[1]
                    value = value[1:]
                    value = value[:-1]
                    return value

        def getMediaLinks():
            media = {}
            videos = []
            images = []
            media_list = data["data"]["user"]["edge_owner_to_timeline_media"][
                "edges"][0]["node"]["edge_sidecar_to_children"]["edges"]
            count = len(media_list)

            for i in range(count):
                media_object = data["data"]["user"]["edge_owner_to_timeline_media"][
                    "edges"][0]["node"]["edge_sidecar_to_children"]["edges"][i]["node"]
                media_type = media_object["__typename"]

                if media_type == 'GraphImage':
                    url = media_object["display_url"]
                    images.append(url)
                elif media_type == 'GraphVideo':
                    url = media_object["video_url"]
                    videos.append(url)
                else:
                    print("[+] Error! Neither image nor video!")
                    exit()
            media = {
                'images': images,
                'videos': videos
            }
            return media

        self.payload = {
            'post': {
                'id': post_id,
                'shortcode': post_short_code
            },
            'item': {
                'title': getValue('title'),
                'description': getValue('description'),
                'price': getValue('price')
            },
            'media': getMediaLinks()
        }

    def saveDataFile(self):
        self.datafile = 'post.json'
        filename = self.datafile
        try:
            with open(filename=filename, mode="w", encoding='utf-8') as out_file:
                json.dump(self.payload, out_file, indent=6, ensure_ascii=False)
                print(f'[+] Succes! File {filename} saved!')
        except:
            print(f'[*] Error! File {filename} not saved correctly!')
            exit()
    
    def DownloadMediaFiles(self):
        hamster = Hamster()
        hamster.importData(self.datafile)
        hamster.createSubCatalog(self.username)
        hamster.download()

def main():
    account = str(input("Account: "))
    instagram = Scraper(account)
    instagram.loadData()
    instagram.extractData()
    instagram.saveDataFile()
    instagram.DownloadMediaFiles()

if __name__ == "__main__":
    main()