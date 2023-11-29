import re

from django.contrib.contenttypes.models import ContentType

from igraph import Graph
from nautobot.dcim.choices import CableTypeChoices
from nautobot.dcim.models import RearPort, Cable, Rack


def get_weight_for_frontport_name(fp_name):
    if "/" in fp_name:
        [part_1, part_2] = fp_name.split("/")
        part_1_match = re.search(r'\d+', part_1)
        part_2_match = re.search(r'\d+', part_2)

        part_1_num = int(part_1_match.group(0)) if part_1_match else 0
        part_2_num = int(part_2_match.group(0)) if part_2_match else 0
        return 1000000 + (part_1_num * 1000) + part_2_num

    else:
        part_1_match = re.search(r'\d+', fp_name)
        part_1_num = int(part_1_match.group(0)) if part_1_match else 0
        return 1000000 + part_1_num


class CablePathExistingMember:
    cable: Cable = None
    is_swapped: bool = False

    def __init__(self, cable_list_raw_entry):
        # cable_list_raw_entry might me something like r_UUID or n_UUID, which means the cable with the UUID in normal
        # or reversed orientation.

        cable_match_regex = re.match(
            r'^([0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12})_([rn])$',
            cable_list_raw_entry)

        self.cable = Cable.objects.get(pk=cable_match_regex.group(1))
        self.is_swapped = cable_match_regex.group(2) == "r"

        # TODO: Add assertions about connected terminations on cable.

    """
    frontport is an abstraction about the Netbox data model.
    Cables added to CablePathExistingMember are connected to two rear ports.
    Those rear ports should only have one front port.
    """

    @property
    def frontport_a(self):
        return self.cable.termination_b.frontports.first() if self.is_swapped else \
            self.cable.termination_a.frontports.first()

    @property
    def frontport_b(self):
        return self.cable.termination_a.frontports.first() if self.is_swapped else \
            self.cable.termination_b.frontports.first()

    @property
    def rearport_a(self):
        return self.cable.termination_b if self.is_swapped else self.cable.termination_a

    @property
    def rearport_b(self):
        return self.cable.termination_a if self.is_swapped else self.cable.termination_b


class CablePathNewMember:
    # termination_a and termination_b are swapped correctly beforehand.
    # There is no way that those need to be swapped at any point.
    termination_a = None
    termination_b = None

    def __init__(self, termination_a, termination_b):
        self.termination_a = termination_a
        self.termination_b = termination_b

    @property
    def needed_cable(self):
        return {
            "termination_a_type": ContentType.objects.get_for_model(self.termination_a),
            "termination_a_id": self.termination_a.id,
            "termination_a": self.termination_a,
            "termination_b_type": ContentType.objects.get_for_model(self.termination_b),
            "termination_b_id": self.termination_b.id,
            "termination_b": self.termination_b
        }


class CablePath:
    def __init__(self, termination_a, termination_a_type, termination_b, termination_b_type, cable_list_raw):
        self.termination_a = termination_a
        self.termination_b = termination_b
        self.termination_a_type = termination_a_type
        self.termination_b_type = termination_b_type

        cp_existing_members = list()
        for clre in cable_list_raw:
            cp_existing_members.append(
                CablePathExistingMember(clre)
            )

        self.cp_existing_members = cp_existing_members
        self.cp_members = list()

        open_elem = self.termination_a

        for existing_member in self.cp_existing_members:

            # open_elem might be the same as frontport_a, if we started our search from a front_port and this
            # is the first cable. Thus, we do not need a cable.
            if open_elem != existing_member.frontport_a:
                self.cp_members.append(
                    CablePathNewMember(
                        open_elem,
                        existing_member.frontport_a
                    )
                )

            open_elem = existing_member.frontport_b
            self.cp_members.append(existing_member)

        if open_elem and open_elem != self.termination_b:
            self.cp_members.append(
                CablePathNewMember(
                    open_elem,
                    self.termination_b
                )
            )

    @property
    def needed_cables(self):
        return list(
            map(lambda x: x.needed_cable, filter(lambda x: isinstance(x, CablePathNewMember), self.cp_members)))

    def get_renderable_path(self):

        # needed_cables and self.cable_list are sorted and only needs to be zipped for a complete cable trace.
        # Furthermore, we only need to add interfaces and devices for a neat trace.

        intermediate_elements = list()

        open_element = {
            "device": self.termination_a.device,
        }

        for cpm in self.cp_members:
            if isinstance(cpm, CablePathNewMember):
                intermediate_elements.append({
                    **open_element,
                    "attachment_b": cpm.termination_a
                })
                intermediate_elements.append({
                    "needed_cable": cpm.needed_cable
                })
                open_element = {
                    "attachment_a": cpm.termination_b,
                    "device": cpm.termination_b.device
                }
            elif isinstance(cpm, CablePathExistingMember):
                intermediate_elements.append({
                    **open_element,
                    "attachment_b": cpm.rearport_a
                })
                intermediate_elements.append({
                    "cable": cpm.cable
                })
                open_element = {
                    "attachment_a": cpm.rearport_b,
                    "device": cpm.rearport_b.device
                }

        intermediate_elements.append(open_element)

        return intermediate_elements


class CableRouter:

    def __init__(self, termination_a, termination_a_type, termination_b, termination_b_type, media_type,
                 enable_next_rack_hops=False):
        self.termination_a = termination_a
        self.termination_b = termination_b

        self.allowed_cable_types = None
        if media_type == "fiber_sm":
            self.allowed_cable_types = [
                CableTypeChoices.TYPE_SMF,
                CableTypeChoices.TYPE_SMF_OS1,
                CableTypeChoices.TYPE_SMF_OS2,
            ]
        elif media_type == "fiber_mm":
            self.allowed_cable_types = [
                CableTypeChoices.TYPE_MMF,
                CableTypeChoices.TYPE_MMF_OM1,
                CableTypeChoices.TYPE_MMF_OM2,
                CableTypeChoices.TYPE_MMF_OM3,
                CableTypeChoices.TYPE_MMF_OM4,
            ]
        elif media_type == "copper":
            self.allowed_cable_types = [
                CableTypeChoices.TYPE_CAT3,
                CableTypeChoices.TYPE_CAT5,
                CableTypeChoices.TYPE_CAT5E,
                CableTypeChoices.TYPE_CAT6,
                CableTypeChoices.TYPE_CAT6A,
                CableTypeChoices.TYPE_CAT7,
                CableTypeChoices.TYPE_CAT7A,
                CableTypeChoices.TYPE_CAT8,
            ]

        excluded_cable_ids = list()
        if termination_a_type.app_label == "dcim" and termination_a_type.model == "frontport":
            rps_to_exclude = RearPort.objects.filter(device=self.termination_a.device)
            for rp in rps_to_exclude:
                if termination_a.rear_port != rp and rp.cable:
                    excluded_cable_ids.append(rp.cable.id)

        if termination_b_type.app_label == "dcim" and termination_b_type.model == "frontport":
            rps_to_exclude = RearPort.objects.filter(device=self.termination_b.device)
            for rp in rps_to_exclude:
                if termination_b.rear_port != rp and rp.cable:
                    excluded_cable_ids.append(rp.cable.id)

        rack_connection_cables = Cable.objects.raw(
            '''
                SELECT
                    c.*, d_a.rack_id as termination_a_rack_id, d_b.rack_id as termination_b_rack_id,
                    fp_a.name as termination_a_name, fp_b.name as termination_b_name
                FROM dcim_cable c
                LEFT JOIN django_content_type ct_a ON ct_a.id = termination_a_type_id
                LEFT JOIN django_content_type ct_b ON ct_b.id = termination_b_type_id
                LEFT JOIN dcim_rearport rp_a ON rp_a.id = termination_a_id
                LEFT JOIN dcim_rearport rp_b ON rp_b.id = termination_b_id
                INNER JOIN dcim_frontport fp_a ON fp_a.rear_port_id = rp_a.id AND fp_a.cable_id IS NULL
                INNER JOIN dcim_frontport fp_b ON fp_b.rear_port_id = rp_b.id AND fp_b.cable_id IS NULL
                LEFT JOIN dcim_device d_a ON rp_a.device_id = d_a.id
                LEFT JOIN dcim_device d_b ON rp_b.device_id = d_b.id
                WHERE (
                    c.type = ANY(%s) AND
                    NOT c.id = ANY(%s) AND
                    ct_a.app_label = 'dcim' AND ct_a.model = 'rearport' AND
                    ct_b.app_label = 'dcim' AND ct_b.model = 'rearport' AND
                    fp_a.cable_id IS NULL and fp_b.cable_id IS NULL
                )
            ''',
            [self.allowed_cable_types, excluded_cable_ids]
        )

        """
        We have two different types of rack interconnection, which have some constraints to them:
        1. Neighbor-Connections, which can only be used once in a row, therefore you cannot hop from rack to rack.
        2. Rack-Connections, which can be used unlimited times and have no further restrictions, but should
        be avoided, if there is a Neighbor Connection available.

        Therefore, we need to use a DAG.
        Each rack has two nodes, one node named X_Incoming and one node named X_Outgoing.
        Each connection with two plugs, e.g. an same rack or inter rack connection, goes from X_Incoming to Y_Outgoing.
        Each connection between two ports, e.g. a fiber connection through the data center, goes from X_Outgoing to Y_Incoming.
        Note: Each connection adds two edges to the graph, X_Outgoing to Y_Incoming and Y_Outgoing to X_Incoming.
        """

        self.graph = Graph(directed=True)

        self.resolvable_edges = dict()

        racks = Rack.objects.all()

        for rack in racks:
            incoming_vertex_id = f'incoming_{rack.id}'
            outgoing_vertex_id = f'outgoing_{rack.id}'

            self.graph.add_vertex(incoming_vertex_id, human_name=rack.name)
            self.graph.add_vertex(outgoing_vertex_id, human_name=rack.name)
            self.graph.add_edge(incoming_vertex_id, outgoing_vertex_id, weight=0)

        if enable_next_rack_hops:
            rack_tuples = Rack.objects.raw(
                '''SELECT 1 as id, racks1.id as rack1_id, racks2.id as rack2_id FROM dcim_rack as racks1, dcim_rack as racks2 WHERE racks1.site_id=racks2.site_id and is_neighbor(racks1.name, racks2.name)'''
            )
            for rack_tuple in rack_tuples:
                self.graph.add_edge(f"incoming_{rack_tuple.rack1_id}", f"outgoing_{rack_tuple.rack2_id}", weight=1500000)

        for edge in rack_connection_cables:
            fp_a_weight = get_weight_for_frontport_name(edge.termination_a_name)
            fp_b_weight = get_weight_for_frontport_name(edge.termination_b_name)

            if not edge.termination_a_rack_id or not edge.termination_b_rack_id:
                continue

            termination_a_incoming_vertex_id = f'incoming_{edge.termination_a_rack_id}'
            termination_a_outgoing_vertex_id = f'outgoing_{edge.termination_a_rack_id}'
            termination_b_incoming_vertex_id = f'incoming_{edge.termination_b_rack_id}'
            termination_b_outgoing_vertex_id = f'outgoing_{edge.termination_b_rack_id}'

            e_to = self.graph.add_edge(
                termination_a_outgoing_vertex_id,
                termination_b_incoming_vertex_id,
                weight=fp_a_weight,
            )
            self.resolvable_edges[e_to.index] = {
                "cable_id": edge.id,
                "is_reversed": False,
            }
            e_from = self.graph.add_edge(
                termination_b_outgoing_vertex_id,
                termination_a_incoming_vertex_id,
                weight=fp_b_weight,
            )
            self.resolvable_edges[e_from.index] = {
                "cable_id": edge.id,
                "is_reversed": True,
            }

    def get_path(self):

        # Technically, this could also end on incoming_, but there is a zero cost edge in place.
        shortest_path = self.graph.get_shortest_paths(
            f'incoming_{self.termination_a.device.rack.id}',
            f'outgoing_{self.termination_b.device.rack.id}',
            weights="weight",
            output="epath",
        )

        # shortest_path could contain more than one element, if the function is called in a different way.
        # Therefore, we can unpack this.

        if len(shortest_path) < 1:
            return None

        # If res now contains no elements, this is a direct connection, which can be done without any "real" edges.
        res = [self.resolvable_edges[x] for x in shortest_path[0] if x in self.resolvable_edges]
        return res
