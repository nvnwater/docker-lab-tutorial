#!/usr/bin/python

# Copyright 2017 - Adriano Pezzuto
# https://github.com/kalise

# Usage: <command> -h host -p port -t
# -h, --host host to connect
# -p, --port port to connect, default is 2375
# -t, --tls use TLS on port 2376

import sys, getopt, os
import docker
import json

def main(argv):
  host = "localhost"
  port = "2375"
  server_timeout = 10
  api_version = 'auto'
  cert_path = os.environ["HOME"] + "/.docker/"
  client_cert = (cert_path + "cert.pem", cert_path + "key.pem")
  ca_cert = cert_path + "ca.pem"
  tls_config = ''
  options, remaining = getopt.getopt(sys.argv[1:], 'h:p:t', ['host=','port=','tls'])
  print "ARGV      :", sys.argv
  print "OPTIONS   :", options
  print "REMAINING :", remaining
  for opt, arg in options:
      if opt in ('-h','--host'):
          host = arg
      elif opt in ('-p','--port'):
          port = arg
      elif opt in ('-t','--tls'):
          tls_config = docker.tls.TLSConfig(client_cert,ca_cert,True)

  base_url = "tcp://" + host + ":" + port
  print "HOST      :", base_url
  client = docker.DockerClient(base_url,api_version,server_timeout,tls_config)
  version = client.version()
  print "VERSION   :", version["Version"]
  print "NODES     :"
  template = "{0:16}{1:16}{2:16}{3:16}{4:16}{5:16}"
  print template.format("ID","STATUS","NAME","ADDRESS","ROLE","AVAILABILITY")
  for node in client.nodes.list():
    id = node.short_id
    status = node.attrs["Status"]["State"]
    address = node.attrs["Status"]["Addr"]
    name = node.attrs["Description"]["Hostname"]
    role = node.attrs["Spec"]["Role"]
    availability = node.attrs["Spec"]["Availability"]
    print template.format(id,status,name,address,role,availability)

    #print json.dumps(node.attrs,sort_keys=True,indent=4)

if __name__ == "__main__":
  main(sys.argv[1:])
