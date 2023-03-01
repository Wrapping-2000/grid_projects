import React from 'react';
import { Select } from 'antd';
import withProps from '../../util/width-props';

type SelectProps = React.ComponentProps<typeof Select>;

const SimpleSelect = withProps<SelectProps>(Select, {
  style: { width: 224, height: 32 },
});

export default SimpleSelect;
