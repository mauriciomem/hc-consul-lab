# hc-consul-lab

## one consul client, three services


```sh
> consul members
Node           Address            Status  Type    Build   Protocol  DC         Partition  Segment
consul-srv-1   10.100.0.11:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-2   10.100.0.12:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-3   10.100.0.13:8301   alive   server  1.21.0  2         dc-docker  default    <all>
web-server-01  10.100.0.2:8301    alive   client  1.21.0  2         dc-docker  default    <default>
```

## one consul client per service

```sh
> consul members          
Node           Address            Status  Type    Build   Protocol  DC         Partition  Segment
consul-srv-1   10.100.0.11:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-2   10.100.0.12:8301   alive   server  1.21.0  2         dc-docker  default    <all>
consul-srv-3   10.100.0.13:8301   alive   server  1.21.0  2         dc-docker  default    <all>
api-server-01  10.100.10.20:8301  alive   client  1.21.0  2         dc-docker  default    <default>
db-server-01   10.100.10.30:8301  alive   client  1.21.0  2         dc-docker  default    <default>
web-server-01  10.100.10.40:8301  alive   client  1.21.0  2         dc-docker  default    <default>
```