export const array2Map = (arr: string[] | undefined) => {
  if (!arr) return arr;
  return arr.reduce((prev: Record<string, string>, current: string) => {
    prev[current] = current;
    return prev
  }, {})
}
