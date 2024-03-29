import re


def check_on_shit(string):      # чистим полученные строки от говна, типа сидата или спецсимволы хтмл
    if string.find('&#') > -1:
        string = encode_from_html(string)
    if string.find('<![CDATA[') > -1:   # чистим строку от cdata
        string = string[string.find('<![CDATA[') + 9: string.find(']]>')]
    string = clear_from_tags(string)
    return string


def encode_from_html(string):   # перекодировка из html символов в обычные, бекап в коммитах
    if re.search(r'&#x[\d\w]{1,4};', string) is not None:   # если вдруг попалась 16-ичная система
        for word in re.findall(r'&#x[\d\w]{1,4};', string):
            string = re.sub(word, chr(int(word[word.rfind('x') + 1:-1], 16)), string)

    if re.search(r'&#\d{1,4};', string) is not None:
        for word in re.findall(r'&#\d{1,4};', string):
            string = re.sub(word, chr(int(word[word.rfind('#') + 1:-1], 10)), string)

    if re.search(r'&lt;|&gt;|quot;|&amp;', string):
        string = string.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')

    if re.search(r'&[^;]{1,8};', string) is not None:  # чистим от кода на буквах (&amp;)
        for word in re.findall(r'&[^;]{1,8};', string):
            string = re.sub(word, '', string)

    return string


def clear_from_tags(string):
    if re.search(r'&lt;|&gt;|quot;|&amp;', string):
        string = string.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')
    string = re.sub(r"</?(hr|br|p|li)[^>]*>", '\n', string)
    for i in re.findall(r"<a[^<]*</a>", string):  # достаем ссылку, без тега
        isurl = re.search(r'href=\"[^\"]*', i, flags=re.IGNORECASE)
        if isurl is not None:
            url = isurl.group()[isurl.group().find('"') + 1:]   # тупо ссылка которая в href
        else:
            url = ''
        content = re.search(r">[^<]*<", i).group()[1:-1]    # контент котоорый в теле тега <a>
        if content == url:
            string = string.replace(i, ' ' + url + ' ')
        else:
            string = string.replace(i, content + ' - ' + url + ' ')
    string = re.sub("<[^>]*>", '', string)  # удаление вообще всех тегов
    return string


def convert_time(time):      # конвертация времени из секунд в часы
    return ('0' * (2 - len(str(time // 3600))) + str(time // 3600)) + ':' + ('0' * (2 - len(str(time // 60 % 60))) + str(time // 60 % 60)) + ':' + ('0' * (2 - len(str(time % 60))) + str(time % 60))


def parse_category(html):   # парсим категории
    categorys, subcategorys = str(), str()
    while html.find('category ') > -1:  # считываем все категории
        if html.find('category text="') == -1:
            break
        html = html[html.find('category text="') + 15:]
        if html.find('>') < html.find('/>'):  # если у категории есть подкатегории
            categorys += html[: html.find('"')].replace('/', 'or') + ', '
            subcategorys_field = html[html.find('>') + 1: html.find('</itunes:category>')]
            while subcategorys_field.find('category text="') > -1:
                subcategorys += subcategorys_field[subcategorys_field.find('category text="') + 15: subcategorys_field.rfind('"')].replace('/', 'or') + ', '
                subcategorys_field = subcategorys_field[subcategorys_field.find('/>') + 2:]
            html = html[html.find('</itunes:category>') + 18:]  # срезаем подкатегории
        else:
            categorys += html[: html.find('"')] + ', '
    if categorys:
        categorys = check_on_shit(categorys)
        if subcategorys:
            subcategorys = check_on_shit(subcategorys)
    return categorys.split(', '), subcategorys.split(', ')


def parse_keywords(html):
    temp_html = html[html.find('keywords>') + 9:]  # временная срезка, для нахождения ключ. слов
    return check_on_shit(temp_html[: temp_html.find('</')]).replace(' ', '').split(',')


def parse_description(html):
    if html.find('description>') == -1:
        return None
    temp_code = html[html.find('description>') + 12:]
    return check_on_shit(temp_code[:temp_code.find(re.search(r"</(desc|itun)", temp_code).group())])


def clear_pubdata(string):
    dict_day = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                   'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    try:
        if string[1] == ' ':    # для нормального времени (2 -> 02)
            string = '0' + string[0] + ' ' + string[2:]
    except Exception as e:
        return None
    month = re.search(r'\w\w\w', string)
    month = month.group() if month else None
    if dict_day.get(month) is None:
        return None
    string = re.sub(month, dict_day.get(month), string)  # запуливаем вместо названия месяца номер месяца
    string = re.sub(r'[ :]', '', string)    # вместо пробела и двоиточия ничего, в инт бахаем
    return string[4:8] + string[2:4] + string[:2]   # подводим под шаблон бд