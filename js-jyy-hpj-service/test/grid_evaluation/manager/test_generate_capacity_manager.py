from test.test_basics import BasicsTestCase
from app.grid_evaluation.manager.generate_capacity_manager import GenerateCapacityManager


class ManagerTest(BasicsTestCase):

    def test_generate_capacity(self):
        dict1 = {'water_power': '水电发电量',
                 'wind_power': '风力发电量',
                 'sun_power': '太阳能发电量',
                 'biomass_power': '生物质能发电量',
                 'social_power': '全社会用电量'
                 }
        print(GenerateCapacityManager.get_generate_power_object_biomass_detail(dict1))
        # print(GenerateCapacityManager.get_generate_power_object_sum_detail(dict1))