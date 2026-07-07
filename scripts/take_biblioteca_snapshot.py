#!/usr/bin/env python3
import os
import requests

SNAPSHOT_PATH = os.environ.get('BIBLIOTECA_SNAPSHOT_FILE', '/home/azureuser/IlViale/biblioteca/biblioteca_iframe_snapshot.html')

def main():
    url = 'https://mailchi.mp/e4fc2f1a5400/ellida'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; SnapshotBot/1.0)'}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    content = r.text
    content = content.replace('og:', 'og_removed:')
    content = content.replace(
        'https://mcusercontent.com/ab5e8ed8c9b39209c68db19d5/images/4ebf9ea4-ee9d-71bb-bc9d-19e5ccd727f6.png',
        'https://vialeformica.org/static/images/LogoViale2019_plain.svg'
    )
    og_tags = """
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://vialeformica.org/static/images/logoassociazione1.jpg" />
    <meta property="og:image:type" content="image/jpeg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Nome associazione con stele di Castionetto" />
    """
    if '</head>' in content:
        content = content.replace('</head>', f'{og_tags}\n</head>')

    os.makedirs(os.path.dirname(SNAPSHOT_PATH), exist_ok=True)
    with open(SNAPSHOT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Snapshot saved to', SNAPSHOT_PATH)

if __name__ == '__main__':
    main()
