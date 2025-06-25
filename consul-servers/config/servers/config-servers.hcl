log_level  = "INFO"
server     = true
datacenter = "dc-docker"

ui_config {
  enabled = true
}

acl {
  enabled       = false
  # enabled        = true
  # default_policy = "deny"
  # down_policy    = "extend-cache"
  # enable_token_persistence = true
  # enable_token_replication = true
  # tokens = {
  #   default            = "b479bcd9-1c18-4356-94fe-7c523fcef19d"
  #   initial_management = "db3e1362-1c65-4ae2-b56a-b2be3aa76c7a"
  # }
}

performance = {
    raft_multiplier = 1
}

limits {
  rpc_max_conns_per_client  = 100
  http_max_conns_per_client = 200
}

encrypt = "pCOEKgL2SYHmDoFJqnolFUTJi7Vy+Qwyry04WIZUupc="

leave_on_terminate = true
data_dir           = "/opt/consul/data"

bootstrap_expect = 3
retry_join = ["consul-srv-1:8301", "consul-srv-2:8301", "consul-srv-3:8301"]

client_addr    = "0.0.0.0"
advertise_addr = "{{GetPrivateIP}}"
bind_addr = "{{GetPrivateIP}}"
