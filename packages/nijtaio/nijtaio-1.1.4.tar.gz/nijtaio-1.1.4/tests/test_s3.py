
import nijtaio
import os

from dotenv import load_dotenv
load_dotenv()

NIJTA_API_URL = 'https://api.nijta.com'
NIJTA_TOKEN = os.getenv('NIJTA_TOKEN')

NIJTA_DEMO_ACCESS_KEY_ID = os.getenv('NIJTA_DEMO_ACCESS_KEY_ID')
NIJTA_DEMO_SECRET_ACCESS_KEY = os.getenv('NIJTA_DEMO_SECRET_ACCESS_KEY')


def test_s3_support_one_file():
    storage_options = {
        "key": NIJTA_DEMO_ACCESS_KEY_ID,
        "secret": NIJTA_DEMO_SECRET_ACCESS_KEY,
    }
    headers = {"Content-Type": "application/json; charset=utf-8", "TOKEN": NIJTA_TOKEN}
    params = {
        'language': 'english_16',
    }

    session_id = nijtaio.session(NIJTA_TOKEN)
    response = nijtaio.send_request(
        's3://nijta-demo/recorded_20231025144932.wav',
        params,
        session_id,
        headers=headers,
        api_url=NIJTA_API_URL,
        storage_options=storage_options,
    )
    assert response.status_code == 202

def test_s3_support_bucket():
    # here we use the credentials stored in ~/.aws/credentials to connect to the genesys bucket
    headers = {"Content-Type": "application/json; charset=utf-8", "TOKEN": NIJTA_TOKEN}
    params = {
        'language': 'english_16',
    }

    session_id = nijtaio.session(NIJTA_TOKEN)
    response = nijtaio.send_request(
        's3://nijta-genesys/',
        params,
        session_id,
        headers=headers,
        api_url=NIJTA_API_URL,

    )
    assert response.status_code == 202
