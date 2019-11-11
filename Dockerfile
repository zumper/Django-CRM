FROM python:3.6

WORKDIR /z_crm

# Intall dependencies
COPY . /z_crm/

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
  apt update && \
  apt install -y git ruby-dev nodejs postgresql-client redis-server wkhtmltopdf && \
  apt clean && \
  gem install compass sass && \
  npm -g install less && \
  pip install --no-cache-dir -r requirements.txt && \
  pip install --no-cache-dir redis

RUN chmod +x /z_crm/entrypoint.sh \
  /z_crm/wait-for-postgres.sh
ENTRYPOINT ["/z_crm/entrypoint.sh"]
