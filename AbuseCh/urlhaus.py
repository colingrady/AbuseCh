import re
import csv
from io import BytesIO
from zipfile import ZipFile

import requests

from ._version import __version__


URLHAUS_API_URL = 'https://urlhaus.abuse.ch/downloads/'

REGEX_CSV_HEADER = re.compile(r'^#\s((?:[a-z_]+,)+(?:[a-z_]+))\r', re.MULTILINE)
REGEX_HOSTFILE_DOMAIN = re.compile(r'^127\.0\.0\.1\t(.+)\r', re.MULTILINE)


class URLhaus(object):

    def __init__(self, api_url=URLHAUS_API_URL):
        '''
        Prepare the URLhaus API
        '''

        # Save the API URL
        self._api_url = api_url

        # Get and prepare the session that will be used for all API calls
        self._session = requests.session()
        self._session.headers.update({
            'User-Agent': f'abuse_ch-urlhaus-api/{__version__}',
        })

    def _request(self, path, **kwargs):
        '''
        Internal method to handle API requests. Raises for errors and
        parses CSV or returns raw data as requested
        '''

        # Compose the full request URL
        req_url = f'{self._api_url}{path}'

        # Make the request
        resp = self._session.get(req_url, **kwargs)
        resp.raise_for_status()

        # Determine what to do based on response content-type
        content_type = resp.headers.get('content-type', None)

        # Is it a zip?
        if content_type == 'application/zip':

            # Attempt to open the response as a zip file
            sample_zip = ZipFile(BytesIO(resp.content))

            # Get the file list and ensure it's just a single file
            file_list = sample_zip.infolist()
            assert len(file_list) == 1

            # Extract the one file
            resp = sample_zip.read(file_list[0].filename)

        # Otherwise we're dealing with the raw content
        else:
            resp = resp.content

        # Return the result
        return resp.decode()

    def _parse_csv(self, content):

        # Attempt to find the CSV header
        csv_header = REGEX_CSV_HEADER.search(content)

        # We found the header
        if csv_header is not None:

            # Get the CSV columns
            csv_columns = tuple(csv_header[1].split(','))

            # Get the CSV data (minus comment lines)
            csv_data = [row for row in content.splitlines() if not row.startswith('#')]

            # Convert the CSV column names and data into a list of dicts
            content = list(csv.DictReader(csv_data, fieldnames=csv_columns))

        # Return the result
        return content

    def get_csv_urls_all(self, raw=False):

        # Make the request
        resp = self._request('csv/')

        # Not returning a raw result? Parse it
        if not raw:
            resp = self._parse_csv(resp)

        # Return the result
        return resp

    def get_csv_urls_recent(self, raw=False):

        # Make the request
        resp = self._request('csv_recent/')

        # Not returning a raw result? Parse it
        if not raw:
            resp = self._parse_csv(resp)

        # Return the result
        return resp

    def get_csv_urls_online(self, raw=False):

        # Make the request
        resp = self._request('csv_online/')

        # Not returning a raw result? Parse it
        if not raw:
            resp = self._parse_csv(resp)

        # Return the result
        return resp

    def get_text_urls_all(self):

        # Make the request and return the result
        resp = self._request('text/')
        return resp

    def get_text_urls_recent(self):

        # Make the request and return the result
        resp = self._request('text_recent/')
        return resp

    def get_text_urls_online(self):

        # Make the request and return the result
        resp = self._request('text_online/')
        return resp

    def get_hostfile(self):

        # Make the request and return the result
        resp = self._request('hostfile/')
        return resp

    def get_domains(self):

        # Get the hostfile
        hostfile = self.get_hostfile()

        # Get the domains from the hostfile
        domains = REGEX_HOSTFILE_DOMAIN.findall(hostfile)

        # Return the result
        return domains

    def get_payloads(self, raw=False):

        # Make the request and return the result
        resp = self._request('payloads/')
        return resp
