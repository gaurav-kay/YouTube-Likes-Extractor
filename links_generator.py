from bs4 import BeautifulSoup

with open('raw_html_utf-8.txt', 'r', encoding='utf-8') as f:
    file_soup = BeautifulSoup(f.read(), 'lxml')

links = file_soup.select('a.pl-video-title-link.yt-uix-tile-link.yt-uix-sessionlink.spf-link ')

print(len(links))
