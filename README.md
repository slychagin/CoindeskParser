# CoindeskParser
News parser from coindesk.com

Быстрый парсер на основе библиотеки aiohttp.
Необходимо было спарсить новости с сайта https://www.coindesk.com
по запросу в поиске https://www.coindesk.com/search?s=bitcoin.

Но по данному запросу получить данные не получалось (парсер просто не выдел их), так как запрос типа "/search?s=" запрещен.
Пробовал bs4, Selenium b Scrapy - безрезультатно.

Нашел другой способ.
На нужной странице сайта открываем инструменты разработчика (F12) -> Networks -> Fetch/XHR -> обновляем страницу ->
находим нужный нам запрос -> щелкаем ПКМ -> Copy -> Copy link address.
Получаем такой адрес:
https://www.coindesk.com/pf/api/v3/content/fetch/search?query=%7B%22search_query%22%3A%22bitcoin%22%2C%22sort%22%3A0%2C%22page%22%3A0%2C%22filter_url%22%3A%22%22%7D

И уже данный адрес используем для парсинга.
Опять таки доступ по нему получилось получить через Selenium, urllib и aiohttp.
Selenium очень медленный в данном случае, urllib намного шустрее, но aiohttp намного быстрее, поэтому выбор пал на него.

Для запуска парсера на своем компьютере выполните следующее
