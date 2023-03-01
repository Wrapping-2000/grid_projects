import React from 'react';
import { Select, DatePicker } from 'antd';
import useSelectors from './useSelectors';
import type { SelectProps, DatePickerProps } from 'antd';
import withProps from '@/util/withProps';

const StyledSelect = withProps<SelectProps<any>>(
  Select,
  {
    style: {width: 200, marginRight: 18, marginLeft: 8},
    labelInValue: true,
    optionLabelProp: 'label'
  }
);

const StyledDatePicker = withProps<DatePickerProps>(
  // @ts-ignore
  DatePicker,
  {
    style: {width: 200, marginRight: 18, marginLeft: 8},
    picker: 'year'
    // labelInValue: true,
    // optionLabelProp: 'label'
  }
);

function Selectors(props: {
  currentTab: HPJ.ProjectEvaluateType,
  handleChange: (type: string) => (v: any) => void;
  options: Record<string, any[]>;
  values?: Record<string, any>;
}) {
  const {currentTab, handleChange, options, values} = props;

  const renders = React.useMemo(() => {
    const getName = (type: string) => `${currentTab}_${type}`

    const getProps = (type: string) => {
      const n = getName(type);
      return {
        value: values?.[n],
        options: options?.[n],
        onChange: handleChange(n),
      }
    }

    const getPickerProps = (type: string) => {
      const n = getName(type);
      return {
        // value: values?.[n],
        // options: options?.[n],
        onChange: handleChange(n),
      }
    }

    if (currentTab === 'construction_process') {
      return (
        <>
          <span>对比均值</span><StyledSelect {...getProps('average')} /> {/* 建设过程-对比均值  */}
        </>
      )
    }

    if (currentTab === 'operation_effect') {
      return (
        <>
          <span>指标类型</span><StyledSelect {...getProps('type')} /> {/* 运营效果-指标类型 */}
          {/* <span>年份</span><StyledSelect {...getProps('year')} /> 运营效果-年份 */}
          <span>年份</span><StyledDatePicker {...getPickerProps('year')} /> {/* 运营效果-年份 */}
          <span>对比均值</span><StyledSelect {...getProps('average')} /> {/* 运营效果-对比均值 */}
        </>
      )
    }

    return (
      <>
        {/* <span>年份</span><StyledSelect {...getProps('year')} /> 投资管控-年份 */}
        <span>年份</span><StyledDatePicker {...getPickerProps('year')} /> {/* 运营效果-年份 */}
        <span>对比均值</span><StyledSelect {...getProps('average')} /> {/* 投资管控-对比均值 */}
      </>
    )
  }, [currentTab, values, options])

  return (
    <div style={{margin: '16px 24px'}}>
      {renders}
    </div>
  );
}

export default Selectors;

export { useSelectors };
