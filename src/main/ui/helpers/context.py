from playwright.sync_api import BrowserContext

def add_item_to_local_storage(context: BrowserContext, item_key: str, item_value: str):
    script = f"window.localStorage.setItem('{item_key}', '{item_value}');"
    context.add_init_script(script)
