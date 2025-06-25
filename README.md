# hc-consul-lab

### check cluster status

```
> consul members
Node           Address           Status  Type    Build   Protocol  DC         Partition  Segment
consul-srv-1   10.100.0.11:8301  alive   server  1.20.6  2         dc-docker  default    <all>
consul-srv-2   10.100.0.12:8301  alive   server  1.20.6  2         dc-docker  default    <all>
consul-srv-3   10.100.0.13:8301  alive   server  1.20.6  2         dc-docker  default    <all>
web-server-01  10.100.0.14:8301  alive   client  1.20.6  2         dc-docker  default    <default>

> consul operator raft list-peers
Node          ID                                    Address           State     Voter  RaftProtocol  Commit Index  Trails Leader By
consul-srv-2  61b6856f-0c39-bea7-28e3-cd68669a265e  10.100.0.12:8300  leader    true   3             68            -
consul-srv-3  40fe4082-bbef-9053-7bf7-324da0efe1e1  10.100.0.13:8300  follower  true   3             68            0 commits
consul-srv-1  bcdfaf70-9bb1-98f8-8589-ddf2ee308b6d  10.100.0.11:8300  follower  true   3             68            0 commits

> consul members                 
Node           Address           Status  Type    Build   Protocol  DC         Partition  Segment
consul-srv-1   10.100.0.11:8301  alive   server  1.20.6  2         dc-docker  default    <all>
consul-srv-2   10.100.0.12:8301  alive   server  1.20.6  2         dc-docker  default    <all>
consul-srv-3   10.100.0.13:8301  alive   server  1.20.6  2         dc-docker  default    <all>
web-server-01  10.100.0.14:8301  alive   client  1.20.6  2         dc-docker  default    <default>
```