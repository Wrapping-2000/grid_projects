declare module 'slash2';
declare module '*.css';
declare module '*.less';
declare module '*.scss';
declare module '*.sass';
declare module '*.svg';
declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.gif';
declare module '*.bmp';
declare module '*.tiff';
declare module 'omit.js';
declare module 'numeral';
declare module '@antv/data-set';
declare module 'mockjs';
declare module 'react-fittext';
declare module 'bizcharts-plugin-slider';

// preview.pro.ant.design only do not use in your production ;
// preview.pro.ant.design Dedicated environment variable, please do not use it in your project.
declare let ANT_DESIGN_PRO_ONLY_DO_NOT_USE_IN_YOUR_PRODUCTION: 'site' | undefined;

declare const REACT_APP_ENV: 'test' | 'dev' | 'pre' | false;
declare const SERVER_URL: string|undefined;
declare const IS_DEV: boolean;

declare namespace HPJ {
  // 项目评价维度
  type ProjectEvaluateType =
    'construction_process'| // 建设过程
    'operation_effect'| // 运行效果
    'financial_benefits' // 投资管控

  // 对比均值
  type AverageClassification =
    'classification'| // 同类均值
    'voltage_level'| // 同电压等级均值
    'company'| // 同公司均值
    'operation_year' // 同投运年份均值

  // 汇总评价展示类型
  type SummaryChartType = 'bar'|'line'|'pie'

  type SummaryChartList = SummaryChartType[];

  // 汇总指标
  type SummaryEvaluateType =
    'construction_control'| // 建设过程
    'operation_effect'| // 运行效果
    'investment_control' // 投资管控
}

