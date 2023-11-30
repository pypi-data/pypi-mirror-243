import json
import os


def get_marketing_cloud_credentials():
    credentials = None
    try:
        credentials = json.loads(os.getenv('mc_info', '{}'))
    except Exception:
        pass

    if not credentials:
        try:
            credentials = json.loads(os.environ.get('mc_info', {}))
            if not credentials:
                print('###### Credenciais inválidas ou não informadas.')
                raise Exception('Credenciais inválidas ou não informadas.')

        except Exception:
            print('###### Credenciais inválidas ou não informadas.')
            raise Exception('Credenciais inválidas ou não informadas.')

    return credentials
