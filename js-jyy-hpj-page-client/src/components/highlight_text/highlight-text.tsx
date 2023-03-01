/*
 * @Describe: 高亮文字组件
 * @Author: kexu9
 * @Date: 2021-04-01 18:02:19
 * @Last Modified by: kexu9
 * @Last Modified time: 2021-07-26 20:59:18
 */
import React, { CSSProperties } from 'react';
import { generate as sid } from 'shortid';

interface Props {
  style?: CSSProperties;
  className?: string;
  content: string;
  contentStyle?: CSSProperties;
  keyword: string | any;
  keywordStyle?: CSSProperties;
  isSingleRow?: boolean;
}

const HighlightText: React.FC<Props> = (props: Props) => {
  const {
    style,
    className,
    keyword,
    keywordStyle = { color: '#6680FF' },
    content = '',
    contentStyle,
    isSingleRow,
  } = props;
  /* 统一关键词 */
  const keywordList = React.useMemo(() => {
    if (Array.isArray(keyword)) {
      const lowerKeyWord = keyword.map((word) => word.toLowerCase());
      const uniqueKeyWord = [...Array.from(new Set(lowerKeyWord))];
      return uniqueKeyWord;
    }
    return [(keyword || '').toLowerCase()];
  }, [content, keyword]);

  /* list内容 */
  const list = React.useMemo(() => {
    const reg = new RegExp(keywordList.join('|'), 'gi');
    const matchList = (content || '').match(reg);
    const splitList = (content || '').split(reg);
    const l = splitList.reduce((p, c, i) => {
      if (matchList && matchList[i]) {
        return [...p, c, matchList[i]];
      }
      return [...p, c];
    }, []);

    return l;
  }, [keywordList, content]);
  const keys = React.useMemo(() => list.map(() => sid()), [list]);
  const finalStyle = isSingleRow
    ? {
        textOverflow: 'ellipsis',
        whiteSpace: 'nowrap',
        overflow: 'hidden',
        ...style,
      }
    : style;

  if (!keyword) {
    return (
      <p className={className} style={finalStyle as CSSProperties}>
        {content}
      </p>
    );
  }

  return (
    <p className={className} style={finalStyle as CSSProperties}>
      {list.map((word, i) => {
        const lowercaseWord = word.toLowerCase();
        const textStyle = keywordList.includes(lowercaseWord) ? keywordStyle : contentStyle;
        return (
          <span key={keys[i]}>
            <span style={textStyle}>{word}</span>
          </span>
        );
      })}
    </p>
  );
};

HighlightText.defaultProps = {
  style: null,
  keywordStyle: undefined,
  className: null,
  contentStyle: null,
  isSingleRow: true,
};

export default HighlightText;
