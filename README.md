# hc-consul-lab

## one consul client, three services

### Deployment

```sh
> git clone 
> cd consul-servers
> docker compose up -d
> cd ../consul-clients
> docker compose up -d
> cd ../app
> docker compose up -d
> export CONSUL_HTTP_ADDR=http://127.0.0.1:8501
```

### Features

 - App available at http://localhost
 - Consul configuration files
   - Cluster config at `consul-servers/config` folder
   - Client config at`consul-clients/config/clients` folder
   - Services config at `consul-clients/config/services` folder
   - Queries config at`consul-client/config/queries` folder

### Datacenter layout

```sh
> consul members
Node           Address            Status  Type    Build   Protocol  DC         Partition  Segment
consul-srv-1   10.100.0.11:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-2   10.100.0.12:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-3   10.100.0.13:8301   alive   server  1.21.0  2         dc-docker  default    <all>
web-server-01  10.100.0.2:8301    alive   client  1.21.0  2         dc-docker  default    <default>

> consul operator raft list-peers                             
Node          ID                                    Address           State     Voter  RaftProtocol  Commit Index  Trails Leader By
consul-srv-1  c1412020-583a-90e5-eaf1-dccac8b1aa1a  10.100.0.11:8300  leader    true   3             41            -
consul-srv-3  3a79f99a-1f86-33de-841d-b56b9e404e06  10.100.0.13:8300  follower  true   3             41            0 commits
consul-srv-2  86a03bf8-9249-f979-9967-b6fe727a661b  10.100.0.12:8300  follower  true   3             41            0 commits

```

## one consul client per service


### Deployment

```sh
> git clone
> cd consul-servers
> docker compose up -d
> cd ../app/db
> docker compose up -d
> cd ../api
> docker compose up -d
> cd ../frontend
> docker compose up -d
> export CONSUL_HTTP_ADDR=http://127.0.0.1:8501
```

### Features

 - App available at http://localhost
 - Consul configuration files
   - Cluster config at `consul-servers/config` folder
   - App database config at`app/db/consul` folder
   - App API config at `app/api/consul` folder
   - Frontend config at`app/frontend/consul` folder

### Datacenter layout

```sh
> consul members          
Node           Address            Status  Type    Build   Protocol  DC         Partition  Segment
consul-srv-1   10.100.0.11:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-2   10.100.0.12:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-3   10.100.0.13:8301   alive   server  1.21.0  2         dc-docker  default    <all>
api-server-01  10.100.10.20:8301  alive   client  1.21.0  2         dc-docker  default    <default>
db-server-01   10.100.10.30:8301  alive   client  1.21.0  2         dc-docker  default    <default>
web-server-01  10.100.10.40:8301  alive   client  1.21.0  2         dc-docker  default    <default>

> consul operator raft list-peers
Node          ID                                    Address           State     Voter  RaftProtocol  Commit Index  Trails Leader By
consul-srv-3  01a3912b-b121-abc2-8bf2-f11e99d9c9e4  10.100.0.13:8300  leader    true   3             84            -
consul-srv-2  00c79e24-f9fb-1c56-83b7-6e633a0d06f4  10.100.0.12:8300  follower  true   3             84            0 commits
consul-srv-1  4a8f510b-95d2-b9fa-f428-d803e41dfbba  10.100.0.11:8300  follower  true   3             84            0 commits
```

