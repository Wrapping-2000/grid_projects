from test.test_basics import BasicsTestCase
from app.grid_evaluation.manager.install_capacity_manager import InstallCapacityManager


class InstallManager(BasicsTestCase):

    def test_install_capacity_manager(self):
        params =[
            {'water_install': '水电装机容量'},
            {'wind_install': '风电装机容量'},
            {'sun_install': '太阳能装机容量'},
            {'biomass_install': '生物质能装机容量'},
            {'social_install': '并网发电装机容量'}
        ]
        # print(InstallCapacityManager.get_install_capacity_object_sum_detail(params))


