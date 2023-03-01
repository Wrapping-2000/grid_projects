
input_name=$1
pkg_name=$(node -e "(function() { console.log(require('./package.json').name) })()")
app_name=${input_name:-$pkg_name}
version=${app_name}-${PROJECT_VERSION}.${BUILD_ID}
echo $version
source ~/.bashrc
nvm install 14.18.3
nvm use 14.18.3
npm  -v
npm install -g pnpm
rm -rf node-modules
# 使用yarn build的话需要安装devDeps中的cross-env
pnpm install
pnpm build zip=${version}
