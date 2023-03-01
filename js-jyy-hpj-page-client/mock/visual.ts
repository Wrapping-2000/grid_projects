import { Request, Response } from 'express';

const getVisual = (req: Request, res: Response) => {
  res.json({
    data: [
      {
        type: '可再生能源',
        indicators: [
          {
            indicator: '可再生能源发电量（10^18焦耳）',
            indicatorTranslation:
              'Renewables: Renewable power generation*(Exajoules (input-equivalent)*)',
          },
          {
            indicator: '可再生能源发电量（太瓦时）',
            indicatorTranslation: 'Renewables: Renewable power generation*(Terawatt-hours)',
          },
          {
            indicator: '可再生能源消费量（10^18焦耳）',
            indicatorTranslation: 'Renewables: Consumption*(Exajoules)',
          },
          {
            indicator: '地热能、生物质能和其他可再生能源消费量（10^18焦耳）',
            indicatorTranslation:
              'Renewables: Consumption - Geothermal, Biomass and Other*(Exajoules (input-equivalent))',
          },
          {
            indicator: '太阳能发电量（太瓦时）',
            indicatorTranslation: 'Renewables: Generation- Solar*(Terawatt-hours)',
          },
          {
            indicator: '太阳能消费量（10^18焦耳）',
            indicatorTranslation: 'Renewables: Consumption - Solar*(Exajoules (input-equivalent))',
          },
          {
            indicator: '风能发电量（太瓦时）',
            indicatorTranslation: 'Renewables: Generation- Wind*(Terawatt-hours)',
          },
          {
            indicator: '风能消费量（10^18焦耳）',
            indicatorTranslation: 'Renewables: Consumption - Wind*(Exajoules (input-equivalent))',
          },
          {
            indicator: '生物燃料产量（千桶油当量/日）',
            indicatorTranslation:
              'Renewable energy -  Biofuels production*(Thousand barrels of oil equivalent per day)',
          },
          {
            indicator: '生物燃料产量（10^15焦耳）',
            indicatorTranslation: 'Renewable energy -  Biofuels production*(Petajoules)',
          },
          {
            indicator: '生物燃料消费量（10^15焦耳）',
            indicatorTranslation: 'Renewable energy -  Biofuels consumption*(Petajoules)',
          },
          {
            indicator: '生物燃料消费量（千桶油当量/日）',
            indicatorTranslation:
              'Renewable energy -  Biofuels consumption*(Thousand barrels of oil equivalent per day)',
          },
          {
            indicator: '可再生能源和其他能源产量（万亿英热单位）',
            indicatorTranslation: 'Renewables and other (quad Btu)',
          },
          {
            indicator: '可再生能源和其他能源消费量（万亿英热单位）',
            indicatorTranslation: 'Renewables and other (quad Btu)',
          },
        ],
      },
      {
        type: '石油',
        indicators: [
          {
            indicator: '石油消费量(10^18焦耳)',
            indicatorTranslation: 'Oil: Consumption*(Exajoules)',
          },
          {
            indicator: '液体石油总消费量（千桶/日）',
            indicatorTranslation:
              'Oil: Total liquids consumption in thousands of barrels per day*(Thousand barrels daily)',
          },
          {
            indicator: '石油消费量（千桶/日）',
            indicatorTranslation: 'Oil: Consumption*(Thousand barrels daily)',
          },
          {
            indicator: '石油消费量（百万吨）',
            indicatorTranslation: 'Oil: Consumption*(Million tonnes)',
          },
          {
            indicator: '石油炼厂产能（千桶/日）',
            indicatorTranslation: 'Oil: Refining Capacity(Thousand barrels daily*)',
          },
          {
            indicator: '原油加工量（千桶/日）',
            indicatorTranslation: 'Oil: Refinery throughput(Thousand barrels daily*)',
          },
          {
            indicator: '石油产量（千桶/日）',
            indicatorTranslation: 'Oil: Production*(Thousand barrels daily)',
          },
          {
            indicator: '石油产量（百万吨）',
            indicatorTranslation: 'Oil: Production*(Million tonnes)',
          },
          {
            indicator: '石油探明储量（十亿桶）',
            indicatorTranslation:
              'Oil: Proved reserves in thousand million barrels(Thousand million barrels)',
          },
          {
            indicator: '石油和其他液体产量（万亿英热单位）',
            indicatorTranslation: 'Petroleum and other liquids (quad Btu)',
          },
          {
            indicator: '石油和其他液体消费量（万亿英热单位）',
            indicatorTranslation: 'Petroleum and other liquids (quad Btu)',
          },
          {
            indicator: '石油贸易出口（千桶/日）',
            indicatorTranslation: 'Oil: Trade movements exports(Thousand barrels daily)',
          },
          {
            indicator: '石油贸易进口（千桶/日）',
            indicatorTranslation: 'Oil: Trade movements imports(Thousand barrels daily)',
          },
        ],
      },
    ],
  });
};

export default {
  getVisual,
};
