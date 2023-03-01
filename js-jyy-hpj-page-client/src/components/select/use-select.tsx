import React from 'react';
import { Select } from 'antd';

interface Options<VT> {
  dataSource?: VT;
  onChange?: (v: any) => void;
  defaultValue?: unknown;
}

function useSelect<VT>(options: Options<VT> = {}) {
  const [value, setValue] = React.useState(
    options.defaultValue !== undefined ? options.defaultValue : options?.dataSource?.[0],
  );

  return {
    Select: React.useMemo(() => Select, []),
    value,
    setValue,
  };
}

export default useSelect;
