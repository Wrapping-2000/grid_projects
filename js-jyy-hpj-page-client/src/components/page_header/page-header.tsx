import React from 'react';
import { Typography } from 'antd';
import Breadcrumb, { BreadcrumbList } from '../breadcrumb';

interface PageHeaderProps {
  breadcrumbs?: BreadcrumbList;
  title?: string | any;
  state?: any;
}

function PageHeader(props: PageHeaderProps): JSX.Element {
  const { breadcrumbs, title, state } = props;
  return (
    <>
      {breadcrumbs ? (
        <Breadcrumb data={breadcrumbs} state={state} style={{ marginTop: 20 }} />
      ) : null}
      {title ? (
        <Typography.Title level={3} style={{ margin: '18px 0' }}>
          {title}
        </Typography.Title>
      ) : null}
    </>
  );
}

PageHeader.defaultProps = {
  breadcrumbs: undefined,
  title: undefined,
  state: undefined,
};

export default PageHeader;
