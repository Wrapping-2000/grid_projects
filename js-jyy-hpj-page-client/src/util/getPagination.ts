/* 获取tablepagination */
import React from 'react';
import type { PaginationProps } from 'antd';

const DEFAULT_PAGE_SIZE = 10;
export default (props?: PaginationProps) => {
  const [size, setSize] = React.useState<number>(props?.pageSize || DEFAULT_PAGE_SIZE);

  const defaultProps = {
    pageSize: DEFAULT_PAGE_SIZE,
    showQuickJumper: true,
    showTotal: (total: number, range: [number, number]) => {
      const pages = Math.ceil(total/size);
      const currentPage = Math.ceil(range[0]/size);
      return `共${total}条记录 第${currentPage}/${pages}页`;
    },
    onChange: (current: number, s: number) => {
      setSize(s);
    }
  }

  return props ? {...defaultProps, ...props} : defaultProps;
}
