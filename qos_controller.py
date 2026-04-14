from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}

# Table-miss rule (VERY IMPORTANT)
def _handle_ConnectionUp(event):
    msg = of.ofp_flow_mod()
    msg.priority = 0
    msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
    event.connection.send(msg)
    log.info("Table-miss installed")


def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.connection.dpid

    if not packet.parsed:
        return

    mac_to_port.setdefault(dpid, {})

    src = packet.src
    dst = packet.dst

    # MAC learning
    mac_to_port[dpid][src] = event.port

    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    ip = packet.find('ipv4')

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)

    # ---------------- QoS ----------------
    if ip:
        if ip.protocol == 6:
            msg.priority = 100
            log.info("TCP -> HIGH PRIORITY")
        elif ip.protocol == 1:
            msg.priority = 10
            log.info("ICMP -> LOW PRIORITY")
        else:
            msg.priority = 5
    else:
        msg.priority = 1

    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

    # immediate forwarding
    po = of.ofp_packet_out()
    po.data = event.ofp
    po.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(po)


def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("QoS Controller Running")
