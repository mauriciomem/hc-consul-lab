FROM nginx:alpine

ARG API_BASE_URL='http://localhost:8000'
ENV API_BASE_URL=${API_BASE_URL}

# install consul
ARG HASHI_PRODUCT 
ARG HASHI_VERSION 

RUN apk add --update --virtual .deps --no-cache gnupg && \
  cd /tmp && \
  wget https://releases.hashicorp.com/${HASHI_PRODUCT}/${HASHI_VERSION}/${HASHI_PRODUCT}_${HASHI_VERSION}_linux_amd64.zip && \
  wget https://releases.hashicorp.com/${HASHI_PRODUCT}/${HASHI_VERSION}/${HASHI_PRODUCT}_${HASHI_VERSION}_SHA256SUMS && \
  wget https://releases.hashicorp.com/${HASHI_PRODUCT}/${HASHI_VERSION}/${HASHI_PRODUCT}_${HASHI_VERSION}_SHA256SUMS.sig && \
  wget -qO- https://www.hashicorp.com/.well-known/pgp-key.txt | gpg --import && \
  gpg --verify ${HASHI_PRODUCT}_${HASHI_VERSION}_SHA256SUMS.sig ${HASHI_PRODUCT}_${HASHI_VERSION}_SHA256SUMS && \
  grep ${HASHI_PRODUCT}_${HASHI_VERSION}_linux_amd64.zip ${HASHI_PRODUCT}_${HASHI_VERSION}_SHA256SUMS | sha256sum -c && \
  unzip /tmp/${HASHI_PRODUCT}_${HASHI_VERSION}_linux_amd64.zip -d /tmp && \
  mv /tmp/${HASHI_PRODUCT} /usr/local/bin/${HASHI_PRODUCT} && \
  rm -f /tmp/${HASHI_PRODUCT}_${HASHI_VERSION}_linux_amd64.zip ${HASHI_PRODUCT}_${HASHI_VERSION}_SHA256SUMS ${HASHI_VERSION}/${HASHI_PRODUCT}_${HASHI_VERSION}_SHA256SUMS.sig && \
  apk del .deps

RUN rm -rf /usr/share/nginx/html/*

COPY contents/ /usr/share/nginx/html/
COPY entrypoint.sh /

EXPOSE 80

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]