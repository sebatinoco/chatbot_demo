import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level
import pandas as pd
from datetime import datetime
import locale 
#from scrapper.parse_args import parse_args
from parse_args import parse_args

async def main():
    
    args = parse_args()
    
    search = f'"{args.search}"' if args.search else args.search
    lang = f'lang:{args.lang}' if args.lang else ''
    since = f'since:{args.since}' if args.since else ''
    until = f'until:{args.until}' if args.until else ''
    
    if not search:
        raise ValueError('you must specify a search prompt to scrape')

    # Validar que la fecha de 'since' sea menor o igual a 'until'
    if args.since and args.until:
        since_date = datetime.strptime(args.since, '%Y-%m-%d')
        until_date = datetime.strptime(args.until, '%Y-%m-%d')
        if since_date > until_date:
            raise ValueError('The "since" date must be less than or equal to the "until" date.')
    
    api = API()
    
    q = ' '.join([search, lang, since, until])
    print(q)
    
    data = []
    async for tweet in api.search(q, limit = args.limit):
        data.append([
            tweet.id, tweet.date, tweet.rawContent, tweet.user.username, 
            tweet.user.location, tweet.lang, tweet.hashtags, 
            tweet.likeCount, tweet.replyCount, tweet.retweetCount, 
            ])

    data = pd.DataFrame(data, columns = [
        'id', 'date', 'tweet', 'username', 
        'user_location', 'language', 'hashtags', 
        'likeCount', 'replyCount', 'retweetCount'
        ])
    
    data.to_csv(f'data/{to_camel_case(args.search)}.csv', encoding = 'utf-8-sig', index = False)

def format_date(fecha_str):
    
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    
    # Analizar la fecha en el formato dado
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S+00:00")

    # Crear una cadena en el formato deseado
    #fecha_formateada = fecha.strftime("%d de %B de %Y")
    fecha_formateada = fecha.date()

    return fecha_formateada

def to_camel_case(text):
    # Divide el texto en palabras separadas por espacios
    words = text.split()
    
    # Capitaliza la primera letra de cada palabra (excepto la primera palabra)
    camel_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    
    # Une las palabras para formar el Camel Case
    camel_case = ''.join(camel_words)
    
    return camel_case

def export_tweets():
    
    args = parse_args()
    
    df = pd.read_csv(f'data/{to_camel_case(args.search)}.csv')
    df['prefix'] = [f'Tweet {tweet}: ' for tweet in range(df.shape[0])]

    df['tweet'] = df['tweet'].apply(lambda x: ' '.join(x.split()) + '. ')

    df['user_location'] = df['user_location'].fillna('')
    df['user_location'] = df['user_location'].apply(lambda x: f'Ubicación: {x}. ')

    df['date'] = df['date'].apply(lambda x: f'Fecha: {format_date(x)}. ')
    df['tweet'] = df['prefix'] + df['tweet'] + df['date'] + df['user_location']

    megadoc = '\n'.join(df['tweet'])
    with open(f'documents/{to_camel_case(args.search)}_corpus.txt', 'w') as file:
        file.write(megadoc)

if __name__ == "__main__":
    # scrape tweets
    asyncio.run(main())
    
    # export tweets to .txt
    export_tweets()
    
    # montar aplicacion con gradio para buscar tweets + QA con LLM?