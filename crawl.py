import requests
from bs4 import BeautifulSoup

zastavky = set()
with open('linky.txt', 'w') as file:
    for i in range(193):
        print(f'linka {i}\n')
        text = requests.get(f'https://imhd.sk/ba/linka/{i}/').text
        parsed = BeautifulSoup(text, 'html.parser')
        tables = parsed.select('table')
        if len(tables) == 2:
            tables = tables[:1]
        else:
            tables = tables[:2]
        for table in tables:
            # Find td elements with class 'w-100' within each table
            td_elements = table.select('td.w-100')
            
            # Do something with the td elements
            file.write(f'{i}:  ')
            for td in td_elements:
                zastavky.add(td.text)
                file.write(f'{td.text};')
            file.write('\n')
               
