/*
 * @Describe: 高亮文字组件
 * @Author: kexu9
 * @Date: 2021-04-01 18:02:19
 * @Last Modified by: kexu9
 * @Last Modified time: 2021-07-26 20:59:51
 */
import React, { CSSProperties } from 'react';
import { generate as sid } from 'shortid';

interface Props {
  style?: CSSProperties;
  className?: string;
  content: string;
  contentStyle?: CSSProperties;
  keyword: string;
  keywordStyle: CSSProperties;
}

const HighlightText: React.FC<Props> = (props: Props) => {
  const { style, className, keyword, keywordStyle, content = '', contentStyle } = props;
  const contentList = (content || '').replace(new RegExp('<br/>', 'gm'), '').split(keyword);
  const keys = React.useMemo(() => contentList.map(() => sid()), [contentList]);

  if (!keyword) {
    return (
      <p className={className} style={style}>
        {content}
      </p>
    );
  }

  return (
    <p className={className} style={style}>
      {contentList.length <= 1 ? (
        <span style={contentStyle}>{contentList[0]}</span> // 没有匹配
      ) : (
        contentList.map((c, i) => {
          // 至少一个匹配
          // 第一个是关键字
          if (c === '' && i === 0) {
            return (
              <span key={keys[i]} style={keywordStyle}>
                {keyword}
              </span>
            );
          }
          // 最后一个是关键字
          if (c === '' && i === contentList.length - 1) {
            return null;
          }
          // 最后一个不是关键字
          if (c !== '' && i === contentList.length - 1) {
            return (
              <span key={keys[i]} style={contentStyle}>
                {c}
              </span>
            );
          }
          return (
            <span key={keys[i]}>
              <span style={contentStyle}>{c}</span>
              <span style={keywordStyle}>{keyword}</span>
            </span>
          );
        })
      )}
    </p>
  );
};

HighlightText.defaultProps = {
  style: null,
  className: null,
  contentStyle: null,
};

export default HighlightText;
