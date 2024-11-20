import re

def extract_hashtags(content):
    return list(set(re.findall(r'#(\w+)', content)))