import argparse
from datetime import datetime

# Configurar el parser
parser = argparse.ArgumentParser()
parser.add_argument('--search', default = None, help = 'search prompt')
parser.add_argument('--lang', default = None, help = 'specified language')
parser.add_argument('--since', default = None, help = 'start date to scrape') # YYYY-MM-DD
parser.add_argument('--until', default = None, help = 'final date to scrape') # YYYY-MM-DD
parser.add_argument('--limit', type = int, default = 10, help = 'max number of tweets')

# Analizar los argumentos
args = parser.parse_args()
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

q = ' '.join([search, lang, since, until])
print(q)
