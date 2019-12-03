from PIL import Image #imaging library (handle image files)
from twython import Twython #twitter api library
import requests
import bs4
import time


# initialize image URL variable
image_url = ""
# initialize image date variable
image_date = ""

# initialize twitter api keys and oauth tokens
APP_KEY = ""
APP_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# open url in beautifulsoup
# soup is the entire html text for the webpage
url = 'https://dilbert.com/'
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'html.parser')

# parses through the html for the first <img> tag with these specific classes
# saves the url of the image to image_url
image = soup.find("img", class_="img-responsive img-comic")
image_url = "https:" + image['src']

# saves date of image to image_date
image_date = soup.find("date", class_="comic-title-date")
image_date = image_date.contents[1]
image_date = image_date.next

# saves comic title to comic_title
comic_title = soup.find("span", class_="comic-title-name")
comic_title = comic_title.contents[0]

# remove comma at the end of image_date and replace whitespace with underscores
image_date = image_date.replace(",", "")
image_date_underscores = image_date.replace(" ", "_")

def saveImg():
    # opens img with pillow (PIL) and saves it as .png with date as the filename
    img = Image.open(requests.get(image_url, stream = True).raw)
    img.save(f'/Users/arnavsurve/Documents/compsci/Python/dilbert-bot/images/{image_date_underscores}.png')

def uploadImage():
    # check if able to verify credentials, then upload image to twitter
    if twitter.verify_credentials():
        photo = open(f'/Users/arnavsurve/Documents/compsci/Python/dilbert-bot/images/{image_date_underscores}.png', 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=f'[{image_date}]\n{comic_title}\ndilbert.com', media_ids=[response['media_id']])
        print(f"Media for {image_date} has been successfully uploaded with title {comic_title}.")
    else:
        print("Unable to verify credentials.")

saveImg()
uploadImage()
prev_image_url = image_url


# main loop
while True:
    # wait 15 seconds before checking for changes in page
    time.sleep(15)

    # refresh page
    response = requests.get(url)

    # parses through the html for the first <img> tag with these specific classes
    # saves the url of the image to image_url
    image = soup.find("img", class_="img-responsive img-comic")
    image_url = "https:" + image['src']

    # if previous image is different than the current image, save current image as a new entry in images folder
    if image_url != prev_image_url:
        # saves date of image to image_date
        image_info = soup.find("date", class_="comic-title-date")
        image_date = image_info.contents[1]
        image_date = image_date.next

        # remove comma at the end of image_date and replace whitespace with underscores
        image_date = image_date.replace(",", "")
        image_date_undercores = image_date.replace(" ", "_")
        print(f"updated comic // url: {image_url}, date: {image_date}")

        saveImg();
        uploadImage();
        prev_image_url = image_url
    else:
        print("no changes")
