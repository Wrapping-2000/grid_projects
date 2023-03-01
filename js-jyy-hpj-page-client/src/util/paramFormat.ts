import isNil from 'lodash/isNil';

export default (options: any) => {
  if (!options || !options.params) return options;
  const {params} = options;
  const {
    current,
    pageSize,
  } = params;

  const formattedParams = isNil(current) ? params : {
    ...options.params,
    skip: (current -1) * pageSize,
    limit: pageSize,
  };

  const formattedOptions: Partial<typeof options> = {
    ...options,
    params: formattedParams
  }
  delete formattedOptions.params.pageSize;
  delete formattedOptions.params.current;
  return formattedOptions;
}
