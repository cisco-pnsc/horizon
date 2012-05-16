import logging

from horizon import views

from .tables import ApplicationsTable

LOG = logging.getLogger(__name__)

apps = [
    {'id': '1',
    'name': 'MySQL',
    'description': 'MySQL is the world\'s most popular open source database software, with over 100 million copies of its software downloaded or distributed throughout it\'s history. With its superior speed, reliability, and ease of use, MySQL has become the preferred choice for Web, Web 2.0, SaaS, ISV, Telecom companies and forward-thinking corporate IT Managers because it eliminates the major problems associated with downtime, maintenance and administration for modern, online applications.',
    'image': 'mysql.png',
    'm_types': ['m1.small','m1.medium','m1.large','m1.xlarge'],},
    {'id': '2',
    'name': 'Wordpress',
    'description': 'WordPress started in 2003 with a single bit of code to enhance the typography of everyday writing and with fewer users than you can count on your fingers and toes. Since then it has grown to be the largest self-hosted blogging tool in the world, used on millions of sites and seen by tens of millions of people every day.',
    'image': 'wordpress.png',
    'm_types':  ['m1.small','m1.medium','m1.large','m1.xlarge'],},
    {'id': '3',
    'name': 'PhpMyAdmin',
    'description': 'RDBMS management',
    'image': 'phpmyadmin.png',
    'm_types':  ['m1.small','m1.medium','m1.large','m1.xlarge'],},
    {'id': '4',
    'name': 'NGINX',
    'description': 'Reverse proxy',
    'image': 'nginx.png',
    'm_types':  ['m1.small','m1.medium','m1.large','m1.xlarge'],},
    {'id': '5',
    'name': 'Webex',
    'description': 'Collaboration',
    'image': 'webex.png',
    'm_types':  ['m1.medium','m1.large','m1.xlarge'],},
]

class IndexView(views.APIView):
    # A very simple class-based view...
    template_name = 'marketplace/applications/index.html'

    def get_data(self, request, context, *args, **kwargs):
       context['apps'] = apps
       return context

class DetailView(views.APIView):
    template_name = 'marketplace/applications/details.html'

    def get_data(self, request, context, *args, **kwargs):
        for app in apps:
            if app['id'] == kwargs['app_id']:
                context['app'] = app
                break
        return context
