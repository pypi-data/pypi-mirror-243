from distutils.core import setup

setup(
    name = 'it4u_web_crawler',
    packages = ['it4u_web_crawler'],
    version = 'v1.0.13',
    description = 'WebCrawler will fetch all requests parallel',
    author = 'Louis',
    author_email = 'thonh.it@gmail.com',
    url = 'https://github.com/louis-it4u/web-crawler',
    download_url = 'https://github.com/louis-it4u/web-crawler/archive/refs/tags/v1.0.13.tar.gz',
    keywords = ['requests', 'crawler'],
    classifiers = [],
    install_requires=[
        'requests',
        'reactivex',
        'tqdm',
        'it4u_http_request==1.0.17'
    ]
)