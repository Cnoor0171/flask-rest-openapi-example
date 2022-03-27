"""Gunicorn configuration"""
# pylint: disable=invalid-name
wsgi_app = "app:create_application()"
bind = "0.0.0.0:9050"
workers = 3
proc_name = "example_server"
keyfile = "certs/private-key.pem"
certfile = "certs/certificate.pem"
ssl_version = "TLS"
accesslog = "-"
raw_env = [
    "LOG_FILE_BASE_NAME=logs/sample_app",
]
