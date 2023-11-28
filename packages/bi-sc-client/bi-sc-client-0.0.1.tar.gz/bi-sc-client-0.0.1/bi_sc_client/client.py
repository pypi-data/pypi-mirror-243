import os
import urllib

import requests

from bi_sc_client.errors import ErrorApiResponse


class BISomConnexioClient:
    def __init__(self):
        user = os.getenv("BI_USER")
        password = os.getenv("BI_PASSWORD")
        self.auth = (user, password)
        self.url = os.getenv("BI_URL")

    def start_billing_run_invoicing(self, billing_run_number):
        body = {"billing_run_uuid": billing_run_number}
        self._send_request("POST", "/apidata/invoices_oc/", body)

    def notify_invoice_number(self, invoice_number):
        params = {"invoice": invoice_number}
        self._send_request("GET", "/apidata/invoices_oc_pdf/", params)

    def _send_request(self, method, path, content):
        headers = {"accept": "application/json"}
        url = urllib.parse.urljoin(self.url, path)
        if method == "GET":
            response = requests.get(
                url=url, params=content, headers=headers, auth=self.auth
            )
        elif method == "POST":
            headers.update(
                {
                    "Content-Type": "application/json",
                }
            )
            response = requests.post(
                url=url, body=content, headers=headers, auth=self.auth
            )
        if not response.ok or response.status_code != 200:
            raise ErrorApiResponse(response.text)
