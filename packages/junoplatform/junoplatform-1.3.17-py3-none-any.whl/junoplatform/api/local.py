import requests
import logging

# CARBON
def write(data:list[dict], batch:bool = True):
    """
    data: list[dict], example:
          [{'PLC_TAG1': 2.2}, {'PLC_TAG2': 1.2}]
    """
    api='http://jp-connector/api/write'
    try:
        newdata = {
            "bacth": batch,
            "data": data
        }
        
        r = requests.post(api, json=newdata, timeout=5)
        if r.status_code != 200:
            logging.error(r.text)
            return r.text
        
        logging.info(f"write opc success: {data}")
        return ""
    except Exception as e:
        logging.error(str(e))
        raise e