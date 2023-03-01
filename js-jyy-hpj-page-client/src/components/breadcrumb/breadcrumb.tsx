import React from 'react';
import { Breadcrumb } from 'antd';
import { generate } from 'shortid';
import cls from 'classnames';
import { useHistory } from 'react-router-dom';
import Path from '../../assets/icon-path.svg';
import RoutePatterns from '../../service/route_paths';
import './breadcrumb.scss';

export interface BreadcrumbItem {
  name: string; // 显示名称
  path?: string; // 路径
  state?: any; // 参数
  onClick?: (path: string) => undefined; // 自定义点击事件
}

export type BreadcrumbList = BreadcrumbItem[];

export interface BreadcrumbsProps {
  data: BreadcrumbList;
  style?: React.CSSProperties;
  state?: any;
}

function Breadcrumbs(props: BreadcrumbsProps): JSX.Element {
  const history = useHistory();

  const { data, style, state } = props;

  /* 面包屑点击事件 */
  const onItemClick = (e, item) => {
    if (item.onClick) {
      item.onClick();
      return;
    }
    if (item.path) {
      history.push(item.path);
    }
    if (item.path === RoutePatterns.ROUTE_ANALYSE_PROFESSIONAL_RESULT) {
      history.replace({
        pathname: item.path,
        state,
      });
    }
    if (item.path === RoutePatterns.ROUTE_ANALYSE_PROFESSIONAL_DATA) {
      history.replace({
        pathname: item.path,
        state,
      });
    }
    if (item.path === RoutePatterns.ROUTE_ANALYSE_DATA_MANAGE_NAME) {
      history.replace({
        pathname: item.path,
        state,
      });
    }
    if (item.path === RoutePatterns.ROUTE_ANALYSE_DATA_MANAGE_CONDITION) {
      history.replace({
        pathname: item.path,
        state,
      });
    }
  };
  /* 为data加上key */
  const dataWithKey = React.useMemo(
    () => data.map((d) => ({ ...d, key: d.path || generate() })),
    [data],
  );
  return (
    <Breadcrumb separator="" className="breadcrumb-container" style={style}>
      <Breadcrumb.Item>
        <Path
          className="icon-back"
          onClick={() => {
            if (history.location.pathname === '/analyse/professional-data/result') {
              history.replace({
                pathname: RoutePatterns.ROUTE_ANALYSE_PROFESSIONAL_DATA,
              });
            } else {
              history.goBack();
            }
          }}
        />
      </Breadcrumb.Item>
      {dataWithKey.map((item, index) => (
        <React.Fragment key={item.key}>
          <Breadcrumb.Item onClick={(e) => onItemClick(e, item)}>
            <span className={cls({ link: index !== dataWithKey.length - 1 })}>{item.name}</span>
          </Breadcrumb.Item>
          {index !== dataWithKey.length - 1 ? <Breadcrumb.Separator /> : null}
        </React.Fragment>
      ))}
    </Breadcrumb>
  );
}

export default Breadcrumbs;
