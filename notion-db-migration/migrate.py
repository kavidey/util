# %%
from pathlib import Path
from dotenv import load_dotenv

if not load_dotenv(Path.cwd()/'.env'):
    raise ValueError('dotenv not found')
# %%
import os
from notion_client import Client
from pprint import pprint
import pickle
from tqdm import tqdm
# %%
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["DATABASE_ID"]
# %%
items = []
next_cursor = None

while True:
    response = notion.databases.query(
        **{
            "database_id": database_id,
            "start_cursor": next_cursor,
        }
    )
    items.extend(response['results'])
    next_cursor = response.get('next_cursor')
    if not next_cursor:
        break
# %%
# with open('backup.pkl', 'wb') as f:
#     pickle.dump(items, f)
# %%
for item in tqdm(items):
    # print("start")
    # pprint(item['properties']['Start Date'])
    # print("\nend")
    # pprint(item['properties']['End Date'])

    if not item['properties']['Start Date']['date']['end']:
        notion.pages.update(
            **{
                "page_id": item['id'],
                "properties": {
                    "Start Date": {
                        "date": {
                            "start": item['properties']['Start Date']['date']['start'],
                            "end": item['properties']['End Date']['date']['start']
                        }
                    }
                }
            }
        )

# %%
