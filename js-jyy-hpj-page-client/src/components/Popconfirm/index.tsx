import React from 'react';
import { Popconfirm, PopconfirmProps } from 'antd';

function CustomPopconfirm(props: PopconfirmProps & {
  desc?: string
}) {
  return (
    <Popconfirm
      {...props}
      title={(
        <div>
          {props?.title ? <p>{props.title}</p> : null}
          {props?.desc ? <p>{props.desc}</p> : null}
        </div>
      )}
    />
  );
}

export default CustomPopconfirm;
