import os
from google.cloud import translate_v2 as translate

class GcpTranslate:
    """
    Instantiate a GCP Translate object.

    Args:
        credential_file (str): Credential json file
        proxy (str): Proxy address
    """
    def __init__(self, credential_file, proxy=''):
        self.credential_file = credential_file
        self.proxy = proxy
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_file
        if proxy != '':
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy

    # Translate text from one language to another language
    def translate_text(self, text, target_language='en'):
        """
        Translate text from one language to another language.

        Args:
            text (str): Text to be translated
            target_language (str): Target language. Default: 'en'

        Returns:
            result (str): Translated text
        """
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=target_language)
        return result['translatedText']
    