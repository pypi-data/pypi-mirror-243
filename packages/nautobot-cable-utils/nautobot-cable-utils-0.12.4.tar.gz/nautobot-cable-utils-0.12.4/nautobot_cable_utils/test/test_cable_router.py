from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from nautobot.dcim.choices import CableTypeChoices, InterfaceTypeChoices
from nautobot.dcim.models import Site, Manufacturer, DeviceType, DeviceRole, Device, Rack, RearPortTemplate, Cable, \
    RearPort, Region, InterfaceTemplate, FrontPortTemplate
from nautobot_cable_utils.cable_router import CableRouter


class CableRouterTest(TestCase):

    @classmethod
    def _populate_sites(cls):

        region = Region.objects.first()
        site = Site.objects.create(name="1519 - RZGö", region=region)
        manufacturer = Manufacturer.objects.create(name="Manufacturer 1", slug="manufacturer-1")
        dt_pp = DeviceType.objects.create(manufacturer=manufacturer, model="Patch Panel")

        rpt = RearPortTemplate.objects.create(
            device_type=dt_pp,
            name="1/1"
        )

        FrontPortTemplate.objects.create(
            device_type=dt_pp,
            name="1/1",
            rear_port=rpt,
        )

        dt_d = DeviceType.objects.create(manufacturer=manufacturer, model="Device")

        InterfaceTemplate.objects.create(
            device_type=dt_d,
            name="swp1",
            type=InterfaceTypeChoices.TYPE_100GE_QSFP28,
        )
        device_role = DeviceRole.objects.create(name="Device Role 1", slug="device-role-1")

        return site, manufacturer, dt_pp, dt_d, device_role

    @classmethod
    def _populate_edges(cls, site, dt_pp, dt_d, device_role, edges, device_locations, cable_type_choice):

        rack_names = set([x for e in edges for x in e])

        for rack_name in rack_names:
            Rack.objects.create(
                name=rack_name,
                site=site
            )

        patched_cables = list()

        for edge in edges:
            (rack_a, rack_b) = edge

            device_a = Device.objects.create(
                device_role=device_role,
                device_type=dt_pp,
                site=site,
                rack=Rack.objects.get(site=site, name=rack_a)
            )

            device_b = Device.objects.create(
                device_role=device_role,
                device_type=dt_pp,
                site=site,
                rack=Rack.objects.get(site=site, name=rack_b)
            )

            c = Cable.objects.create(
                termination_a=RearPort.objects.get(device=device_a),
                termination_b=RearPort.objects.get(device=device_b),
                type=cable_type_choice,
            )

            patched_cables.append(c)

        start_dev = Device.objects.create(
            device_role=device_role,
            device_type=dt_d,
            site=site,
            rack=Rack.objects.get(site=site, name=device_locations[0])
        )

        end_dev = Device.objects.create(
            device_role=device_role,
            device_type=dt_d,
            site=site,
            rack=Rack.objects.get(site=site, name=device_locations[1])
        )

        return patched_cables, start_dev, end_dev

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        site, manufacturer, dt_pp, dt_d, device_role = cls._populate_sites()
        cls.simple_patch_cables, cls.simple_patch_start, cls.simple_patch_end = cls._populate_edges(
            site, dt_pp, dt_d, device_role,
            [
                ("1519-B-1009", "1519-B-1010"),
                ("1519-B-1011", "1519-B-1012"),
                ("1519-B-1010", "1519-B-1011"),
            ],
            [
                "1519-B-1009",
                "1519-B-1012",
            ],
            CableTypeChoices.TYPE_SMF
        )

        cls.rack_hop_cables, cls.rack_hop_start, cls.rack_hop_end = cls._populate_edges(
            site, dt_pp, dt_d, device_role,
            [
                ("1519-C-1009", "1519-C-1010"),
                ("1519-C-1011", "1519-C-1012"),
            ],
            [
                "1519-C-1009",
                "1519-C-1012",
            ],
            CableTypeChoices.TYPE_SMF
        )

    def test_dummy(self):

        content_type = ContentType.objects.get(app_label="dcim", model="interface")
        cr = CableRouter(self.simple_patch_start.interfaces.first(), content_type, self.simple_patch_end.interfaces.first(), content_type, "fiber_sm")
        cr_reverse = CableRouter(self.simple_patch_end.interfaces.first(), content_type, self.simple_patch_start.interfaces.first(), content_type, "fiber_sm")
        cr_simple_hop = CableRouter(self.simple_patch_end.interfaces.first(), content_type, self.simple_patch_start.interfaces.first(), content_type, "fiber_sm", enable_next_rack_hops=True)
        path = cr.get_path()
        path_reverse = cr_reverse.get_path()
        path_simple_hop = cr_simple_hop.get_path()

        self.assertEqual(len(path), 3)
        self.assertEqual(len(path_reverse), 3)
        self.assertEqual(len(path_simple_hop), 1)
        self.assertEqual(sorted(path), sorted(map(lambda c: c.id, self.simple_patch_cables)))
        self.assertEqual(sorted(path_reverse), sorted(map(lambda c: c.id, self.simple_patch_cables)))

    def test_rack_hop_disabled(self):
        content_type = ContentType.objects.get(app_label="dcim", model="interface")
        cr = CableRouter(self.rack_hop_start.interfaces.first(), content_type, self.rack_hop_end.interfaces.first(), content_type, "fiber_sm")
        cr_easy_hop = CableRouter(self.rack_hop_start.interfaces.first(), content_type, self.rack_hop_end.interfaces.first(), content_type, "fiber_sm", enable_next_rack_hops=True)
        path = cr.get_path()
        cr_easy_hop_path = cr_easy_hop.get_path()
        self.assertEqual(path, None)
        self.assertEqual(len(cr_easy_hop_path), 2)
