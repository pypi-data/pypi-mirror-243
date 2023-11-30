



import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import logging
import pkg_resources

# logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

assets_dir = './assets/'

resource_package = __name__
resource_path = 'assets.json'
assets_path = pkg_resources.resource_filename(resource_package, resource_path)


with open(assets_path, 'r') as file:
    data = json.load(file)
    hashmap_ext = data['extension_to_folder']


class AssetHandler(FileSystemEventHandler):
    def on_created(self, event):
        
        _, ext = os.path.splitext(event.src_path)
        ext = ext[1:]

        if ext in hashmap_ext:
            target_dir = os.path.join(assets_dir +  hashmap_ext[ext])
        
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            try:
                shutil.move(event.src_path, assets_dir + hashmap_ext[ext])
                logger.info(f" \"{os.path.basename(event.src_path)}\" was moved to \"{hashmap_ext[ext]}\"")
                
            except Exception as e:
                logger.error(f" coulnd't move \"{os.path.basename(event.src_path)}\" to Target Path because of {e}")
                
        else:
            logger.warning(f" No specified folder for the .{ext} filetype")



def main():
    
    observer = Observer()
    observer.schedule(AssetHandler(), path=".", recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
if __name__ == "__main__":
    main()
    