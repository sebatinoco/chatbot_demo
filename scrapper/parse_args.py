import argparse

def parse_args():
    
    parser = argparse.ArgumentParser()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', default = None, help = 'search prompt')
    parser.add_argument('--lang', default = None, help = 'specified language')
    parser.add_argument('--since', default = None, help = 'start date to scrape') # YYYY-MM-DD
    parser.add_argument('--until', default = None, help = 'final date to scrape') # YYYY-MM-DD
    parser.add_argument('--limit', type = int, default = 10, help = 'max number of tweets')
    
    # consolidate args
    args = parser.parse_args()
    #args = vars(args)
    
    return args
    