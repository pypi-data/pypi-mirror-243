import requests


class errors():    
    class PromptError(Exception):
        def __init__(self) -> None:
            self.error = 'prompt must be non empty string and bigger than 0 and smaller than 257'
        
        def __str__(self) -> str:
            return self.error
    
    class ServerError(Exception):
        def __init__(self) -> None:
            self.error = "API server is unreachable. Maybe you using bad URL or used method, that doesn't exist"
        
        def __str__(self) -> str:
            return self.error
    
    class GenresError(Exception):
        def __init__(self) -> None:
            self.error = "Wrong count of genres, it must be bigger than 0 and smaller than 35. Try again"
        
        def __str__(self) -> str:
            return self.error
    
    class TempertureError(Exception):
        def __init__(self) -> None:
            self.error = "temperture must be bigger than 0 and smaller than 41"
        
        def __str__(self) -> str:
            return self.error

    class TextLengthError(Exception):
        def __init__(self) -> None:
            self.error = "text_len must be bigger than 15 and smaller than 4096"
        
        def __str__(self) -> str:
            return self.error





class PomidorAPI():
    '''main class of SDK
params:
    
    url - actial pomidor project url. You can found it on https://api.pomidorproject.ru
'''
    def __init__(self, url: str = 'https://api.pomidorproject.ru') -> None:
        self.url = url
    
    def __str__(self) -> str:
        return '''PomidorAPI SDK
version - 1.5.0
methods - TETA, BRSC, AUM, DostGeneration'''


    def TETA(self, prompt: str = 'neutral sentense that dont contain any bad words') -> dict:
        '''Function that analyzes text for toxicity level

params: 

    prompt - string
    
return:

    response - dict'''
        if prompt != '':
            res = requests.post(f'{self.url}/TETA', params={'prompt': prompt})
            jn = res.json()
            if res.status_code != 200:
                raise errors.ServerError
            if 'error' in jn:
                raise errors.PromptError
            return jn
        else:   
            raise errors.PromptError
    

    def UAM(self, prompt: str = 'anime description', genres_count: int = 3) -> dict:
        '''Function that predict anime genre 

params: 

    prompt - description of anime
    genres_count - count of returned genres (1 - 34)

return:

    response - dict'''
        if not 1<=genres_count<=34:
            raise errors.GenresError
        if prompt != '':
            res = requests.post(f'{self.url}/UAM', params={'prompt': prompt, 'genres_count': genres_count})
            jn = res.json()
            if res.status_code != 200:
                raise errors.ServerError
            if 'error' in jn:
                raise errors.PromptError
            return jn
        else:
            raise errors.PromptError
    

    def TDM(self, prompt: str = 'Lorem ipsum dolor sit amet', text_length: int = 100, temperture: float = 0.5) -> dict:
        '''Function that generate text, based on Crime And Punishment Dostoevsky

params: 

    prompt - The sentence with which generation will begin
    text_length - count of symbols, that will generated
    temperture - Model creativity (the more the more creative) is not less than zero
    
return:

    response - dict'''
        if prompt != '':
            res = requests.post(f'{self.url}/TDM', params={'prompt': prompt, 'text_length': text_length, 'temperture': temperture})
            jn = res.json()
            if res.status_code != 200:
                raise errors.ServerError
            if 'error' in jn:
                if 'prompt' in jn['error']:
                    raise errors.PromptError
                elif 'temperture' in jn['error']:
                    raise errors.TempertureError
                elif 'text_len' in jn['error']:
                    raise errors.TextLengthError
            return jn
        else:
            raise errors.PromptError
        
    def BRSC(self, prompt: str = 'Lorem ipsum dolor sit amet', text_length: int = 100, seed: int = 42, out_lang: str = 'en') -> dict:
        '''Function that generate fake researches

params:

    prompt - The sentence with which generation will begin
    text_length - count of symbols, that will generated
    seed - randomizer of text
    out_lang - Language into which the result will be translated ("ru" | "en")
    
return:

    response - dict'''
        if prompt != '':
            res = requests.post(f'{self.url}/BRSC', params={'prompt': prompt, 'seed': seed, 'text_length': text_length, 'out_lang': out_lang})
            jn = res.json()
            if res.status_code != 200:
                raise errors.ServerError
            if 'error' in jn:
                if 'prompt' in jn['error']:
                    raise errors.PromptError
                elif 'text_len' in jn['error']:
                    raise errors.TextLengthError
            return jn
        else:   
            raise errors.PromptError


        

if __name__ == '__main__':
    Pomidor = PomidorAPI('http://172.20.10.9:80')
    research = Pomidor.BRSC("", 250, 234, 'ru')
    print(research['response'])