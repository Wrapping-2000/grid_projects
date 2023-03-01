const getHighlight = (content) => {
  if (!content) {
    return [];
  }
  return [...Array.from(new Set([...Array.from(Array.from(content.matchAll(/&_(.*?)_&/g), (m: any) => m[1]) || [])]))];
};
export default getHighlight;
