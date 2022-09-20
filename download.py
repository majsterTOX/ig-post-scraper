from requests_html import HTMLSession
import pathlib
import json
import os

session = HTMLSession()

class Hamster:

    def importData(self, datafile) -> 'str':
        with open(file=datafile, mode="r", encoding='utf-8') as file:
            content = file.read()
        data = json.loads(content)
        self.images = data["media"]["images"]
        self.videos = data["media"]["videos"]

    def createSubCatalog(self, new_catalog) -> 'str':
        current_path = os.getcwd()
        catalog_path = f"{current_path}\{new_catalog}"

        def exist():
            isExist = os.path.exists(catalog_path)
            return isExist

        if exist() == False:
            os.mkdir(new_catalog)
        else:
            pass
        os.chdir(catalog_path)

        self.path = os.getcwd()

    def download(self):
        path = self.path
        id = 1
        for image_url in self.images:
            content = session.get(image_url).content
            name = f"image-{id}.jpg"
            try: 
                with open(file=name, mode="wb") as img:
                    img.write(content)
                    id = id + 1
                    print(f"[+] Download {name} in {path}")
            except:
                    print(f"[*] Failed {name} in {path}")
                    exit()
        id = 1
        for video_url in self.videos:
            content = session.get(video_url).content
            name = f"video-{id}.mp4"
            try: 
                with open(file=name, mode="wb") as img:
                    img.write(content)
                    id = id + 1
                    print(f"[+] Download {name} in {path}")
            except:
                    print(f"[*] Failed {name} in {path}")
                    exit()