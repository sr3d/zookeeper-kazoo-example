This is a test playground to explore ZooKeeper using Kazoo python client.

To start:

0.  run `pip3 install kazoo`
1.  run `docker-compose up`
2.  run `python3 server.py` in one terminal

```
± |master S:2 ?:1 ✗| → python3 server.py
State change CONNECTED
registering...
CONNECTED
join_as_master
watching /price_service/online
Children are now: []
Any key to exit
```

3.  run `python3 server.py` in another terminal

```
± |master S:2 ?:1 ✗| → python3 server.py
State change CONNECTED
registering...
CONNECTED
join_as_slave
/price_service/online/slave0000000012
on_master_update
Version: 0, data: {"master": true}
Any key to exit
```

4.  Use the Zoonavigator at http://localhost:9000 with `zookeeper:2181` as the connection to update the master node and the slave will get the update from the master.

5.  Killing the slave will result in the master getting a new list of children after a few seconds of missing heartbeat.