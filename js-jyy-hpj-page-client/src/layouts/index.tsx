import React from 'react';
import { Badge, DatePicker, Select } from 'antd';
import type { IRouteComponentProps } from 'umi';
import cls from 'classnames';
import ProProvider from '@ant-design/pro-provider';//加@表示引入的该包是范围包
import styles from './style.less';

export default function Layout({ children }: IRouteComponentProps) {
  const values = React.useContext(ProProvider);
  return (
    <ProProvider.Provider
      value={{
        ...values,
        valueTypeMap: {
          statusIndicator: {
            render: (value) => {
              if (!value?.status_msg) return <span>-</span>;
              const success = value?.status === 'green';
              return (
                <span>
                  <Badge
                    className={cls([styles['status-indicator']], success && styles.success)}
                    status={success ? 'success' : 'error'}
                    text={value.status_msg}
                  />
                </span>
              )
            },
            renderFormItem: (text, props) => {
              const options = Object.keys(props?.valueEnum||{}).map(value => ({value, name: value}));
              if (props.fieldProps?.valuePropName) {
                props.fieldProps.valuePropName = 'status';
              }
              return <Select {...props.fieldProps} options={options} allowClear placeholder="请选择" />
            }
          },
          customDateYear: {
            render: (text) => {
              return text
            },
            renderFormItem: (text, props) => {
              // 这里服务端接口不要时间戳，需要年份字符串比如`2019`, 但这里onchange经过内部组件是还需要是个Moment，所以在接口请求处处理
              return <DatePicker picker="year" {...props.fieldProps} />
            }
          },
        },
      }}
    >
      {children}
    </ProProvider.Provider>
  );
}
