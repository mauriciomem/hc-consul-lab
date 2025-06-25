FROM python:3.12-slim

ARG HASHI_PRODUCT=consul
ARG HASHI_VERSION=1.20.4

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install consul and curl for health checks
RUN apt update && apt install gpg unzip grep wget curl -y && \
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
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]