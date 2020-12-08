from kazoo.client import KazooClient, KazooState
import json
import signal
import sys
import time

zk = KazooClient(hosts='127.0.0.1:2181')

is_master = False

def join_as_master():
    global is_master

    is_master = True
    print("join_as_master")
    zk.ensure_path("/price_service")

    node = None
    node = zk.create("/price_service/master", str.encode(json.dumps({"master": True})), ephemeral=True)

    zk.ensure_path("/price_service/online")
    watch_node("/price_service/online")


def watch_node(node):
    print("watching " + str(node))

    def callback(children):
        # print(event)
        print("Children are now: %s" % children)
    children = zk.ChildrenWatch(node, callback)


def join_as_slave():
    print("join_as_slave")

    zk.ensure_path("/price_service/online")
    node = zk.create("/price_service/online/slave", str.encode(json.dumps({"slave": True})), sequence=True, ephemeral=True)
    print(node)

    zk.DataWatch("/price_service/master", on_master_update)


def on_master_update(data, stat):
    print("on_master_update")
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))


@zk.add_listener
def my_listener(state):
    print(f"State change {state}")
    if state == KazooState.LOST:
        print("lost connection")
        # Register somewhere that the session was lost
        pass
    elif state == KazooState.SUSPENDED:
        print("suspended")
        # Handle being disconnected from Zookeeper
        pass
    elif state == KazooState.CONNECTED:
        print(zk.client_state)


zk.start()



def register():
    print("registering...")
    master_node = zk.exists("/price_service/master")
    if master_node is not None:
        join_as_slave()
    else:
        join_as_master()

register()

input("Any key to exit\n")

gracefully_exit()

zk.stop()



def gracefully_exit(*args):
    print('You pressed Ctrl+C!')
    try:
        if is_master:
            zk.delete('/price_service/master')
    except Exception as e:
        print(e)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')

# # k = input("any button to exit")
# while True:
#     time.sleep(0.1)