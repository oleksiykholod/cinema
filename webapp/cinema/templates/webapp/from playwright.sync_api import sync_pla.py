import asyncio
from pyppeteer import launch

async def get_xhr_requests(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url,timeout=0)

    # Чекаємо 10 секунд перед тим, як збирати дані
    await page.waitFor(10000)

    # Отримуємо всі запити зі списку requests
    requests = await page.evaluate('() => performance.getEntriesByType("resource")')

    # Відбираємо XHR запити та зберігаємо дані з кожного
    xhr_requests = [request for request in requests if 'xmlhttprequest' in request['name']]
    data = [await page.evaluate(f'return (await fetch("{request["name"]}")).json()') for request in xhr_requests]

    await browser.close()
    return data

url = 'https://rezka.ag/series/adventures/53465-odni-iz-nas-2023.html'
data = asyncio.get_event_loop().run_until_complete(get_xhr_requests(url))
print(data)