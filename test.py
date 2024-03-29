import util


def parse(url):
    util.execute('INSERT INTO url_podcasts (url_podcast, status_podcast) VALUES (%(p)s, %(p)s)', url, 1,
                 commit=True)  # ставим подкасту 0, что мы его уже скачали
#
# def parse(url):
#     util.execute('UPDATE url_podcasts SET status_podcast = 1 WHERE url_podcast = %(p)s', url,
#                  commit=True)  # ставим подкасту 0, что мы его уже скачали


if __name__ == '__main__':
    util.execute('TRUNCATE categorys', commit=True)
    util.execute('TRUNCATE items', commit=True)
    util.execute('TRUNCATE items_with_keywords', commit=True)
    util.execute('TRUNCATE keywords', commit=True)
    util.execute('TRUNCATE keywords_items', commit=True)
    util.execute('TRUNCATE podcasts', commit=True)
    util.execute('TRUNCATE podcasts_with_categorys', commit=True)
    util.execute('TRUNCATE podcasts_with_keywords', commit=True)
    util.execute('TRUNCATE podcast_with_subcat', commit=True)
    util.execute('TRUNCATE subcat_item', commit=True)
    util.execute('TRUNCATE subcat_podcast', commit=True)
    util.execute('TRUNCATE error_links', commit=True)
    util.execute('TRUNCATE cat_item', commit=True)
    util.execute('TRUNCATE url_podcasts', commit=True)
    util.execute('TRUNCATE temp_table', commit=True)
    # parse('https://mojomedia.ru/feed-podcasts/rebyata-my-potrahalis')
    parse('https://feeds.podcastmirror.com/zavtracast')
    # with open('parse_link.txt', 'r') as f:
    #     for i in enumerate(f.readlines()):
            # if i[0] < 100:
            # parse(i[1])
            # else:
            #     break
    # parse('https://podcasts.apple.com/ru/podcast/radio2-in-the-mix/id494551291')
    # parse('http://aboutsf.podomatic.com/rss2.xml')
    # parse('http://feeds.soundcloud.com/users/soundcloud:users:700171334/sounds.rss')
    # parse('https://meduza.io/rss/podcasts/sperva-rodi')
    # parse('http://feeds.soundcloud.com/users/soundcloud:users:700171334/sounds.rss')
    # parse('https://vk.com/podcasts-152712748.rss')
    # parse('https://feeds.podcastmirror.com/zavtracast')
    # parse('https://radiomayak.ru/podcasts/rss/podcast/2441')
    # parse('https://radiomayak.ru/podcasts/rss/podcast/2441')
    # parse('https://vk.com/podcasts-64599002.rss')