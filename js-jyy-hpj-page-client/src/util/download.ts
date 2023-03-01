export default (objectUrl: string, name: string): void => {
  const link = document.createElement('a');
  link.href = objectUrl;
  link.setAttribute('download', name);
  document.body.appendChild(link);
  link.click();
  // safari 同步revoke会报错
  setTimeout(() => {
    window.URL.revokeObjectURL(link.href);
  }, 100);
};
