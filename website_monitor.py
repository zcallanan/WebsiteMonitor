import asyncio
import functools
import requests
import sys
import time
import yaml
from http import HTTPStatus

with open('config.yml') as f:
    config_data = yaml.safe_load(f)

config_period = config_data['data']['period']
config_log_file = config_data['data']['log_file']
config_urls = config_data['data']['urls']
input_val = ''
input_quit = ''

def handle_standard_output(period):
    # Use config period
    if period == '':
        period = str(config_period)

    # Use input value if valid
    if period.isnumeric():
        period = float(period)
        print(f'Logging website progress check to {config_log_file} every {period} seconds')
    
    return period

while isinstance(input_val, str):
    input_val = input(f'Enter the period between website checks, or hit ENTER to use the default value {config_period}.\n>> ')

    input_val = handle_standard_output(input_val)

def make_periodic_http_requests(period):
    def loop_http_request_tasks(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            while True:
                task = asyncio.create_task(fn(*args, **kwargs))
                await asyncio.sleep(period)
                if task.result() == 1:
                    break
        return wrapper
    return loop_http_request_tasks

@make_periodic_http_requests(input_val)
async def http_get_request(url):
    try: 
        res = requests.get(url)

        # Append to log file
        with open(config_log_file, 'a', encoding='utf-8') as f:
            print(f'{time.asctime()}; {url}; {res.status_code} - '\
                f'{HTTPStatus(res.status_code).name}; {res.elapsed.total_seconds()}', file = f)

        await asyncio.sleep(1)
    except Exception as e:
        print(repr(e))
        return 1

async def main():
    tasks = [http_get_request(url) for url in config_urls]

    try: 
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(repr(e))
        sys.exit(1)
    
asyncio.run(main())
