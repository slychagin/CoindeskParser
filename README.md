# CoindeskParser
![made by](https://img.shields.io/badge/made_by-slychagin-green)
![python](https://img.shields.io/badge/python-v3.10.5-blue)
![aiohttp](https://img.shields.io/badge/aiohttp-v3.8.4-red)

News parser from coindesk.com
#
Быстрый парсер на основе библиотеки aiohttp.

Необходимо было спарсить новости с сайта https://www.coindesk.com
по запросу в поиске https://www.coindesk.com/search?s=bitcoin.

Но по данному запросу получить данные не получалось (парсер просто не видел их), так как запрос типа "/search?s=" запрещен.
Пробовал bs4, Selenium и Scrapy - безрезультатно.

Нашел другой способ.
На нужной странице сайта открываем инструменты разработчика (F12) -> Networks -> Fetch/XHR -> обновляем страницу ->
находим нужный нам запрос -> щелкаем ПКМ -> Copy -> Copy link address.
Получаем такой адрес:
https://www.coindesk.com/pf/api/v3/content/fetch/search?query=%7B%22search_query%22%3A%22bitcoin%22%2C%22sort%22%3A0%2C%22page%22%3A0%2C%22filter_url%22%3A%22%22%7D

И уже данный адрес используем для парсинга (необходимо просто менять значение page, по умолчанию равно 0).
Доступ по нему получилось получить через Selenium, urllib и aiohttp.
Selenium очень медленный в данном случае, urllib намного шустрее, но aiohttp намного быстрее, поэтому выбор пал на него.

### Вы можете запустить этот проект локально просто сделав следующее:
- `git clone https://github.com/slychagin/CoindeskParser.git`;
- у вас должен быть установлен Python;
- установите все зависимости из файла requirements.txt.
