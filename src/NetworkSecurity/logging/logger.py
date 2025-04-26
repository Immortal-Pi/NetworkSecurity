import logging
import os 
from datetime import datetime 

# LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
today=datetime.now().strftime('%m_%d_%Y')
log_folder=os.path.join(os.getcwd(),'logs',today)
os.makedirs(log_folder,exist_ok=True)

log_file=f'{today}.log'
log_file_path=os.path.join(log_folder,log_file)

# log_path=os.path.join(os.getcwd(),'logs',LOG_FILE)
# os.makedirs(log_path,exist_ok=True)

# LOG_FILE_PATH=os.path.join(log_path,LOG_FILE)


logging.basicConfig(
    filename=log_file_path,
    format='[%(asctime)s %(lineno)d %(name)s - %(levelname)s - %(message)s]',
    level=logging.INFO,

)

