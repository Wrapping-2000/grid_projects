/*
 * @Describe: 设置组件预定义props的方法
 * @Author: kexu9
 * @Date: 2021-04-27 10:08:49
 * @Last Modified by: kexu9
 * @Last Modified time: 2021-07-26 19:00:05
 */
import React from 'react';
import defaultsDeep from 'lodash/defaultsDeep';

function withProps<CP>(
  Component: React.FC<CP>,
  predefineProps: CP,
  options?: { mergeFunction?; debug? },
) {
  return function component(props: CP): JSX.Element {
    const { mergeFunction, debug } = options || {};

    /* 默认合并方法 */
    const defaultMerge = (preP, p) => {
      // 拼接合并className
      let className = '';
      if (preP?.className) {
        className += preP.className;
      }
      if (p?.className) {
        className = className ? `${className} ${p.className}` : p.className;
      }
      // deep合并其他属性
      const merged = defaultsDeep({ ...p }, preP);
      return { ...merged, className: className || merged.className };
    };

    /* 合并props */
    const mergeProps = (preP, p) =>
      mergeFunction ? mergeFunction(preP, p) : defaultMerge(preP, p);

    const finalProps = mergeProps(predefineProps, props);

    if (debug) {
      // eslint-disable-next-line no-console
      console.debug(finalProps, 'withProps_finallyProps');
    }
    return <Component {...finalProps} />;
  };
}

export default withProps;
