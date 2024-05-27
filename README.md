# zhouyi-fontend

## 部署说明

创建者本机的node和npm版本为：Node.js v16.18.1.npm@9.3.1

如果不一样的话应该没大问题。

创建时配置如下：

```bash
Vue CLI v5.0.8
? Please pick a preset: Manually select features
? Check the features needed for your project: Babel, PWA, Router, Vuex, CSS Pre-processors, Linter, Unit
? Choose a version of Vue.js that you want to start the project with 3.x
? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
? Pick a CSS pre-processor (PostCSS, Autoprefixer and CSS Modules are supported by default): Sass/SCSS (with dart-sass)
? Pick a linter / formatter config: Basic
? Pick additional lint features: Lint on save
? Pick a unit testing solution: Jest
? Where do you prefer placing config for Babel, ESLint, etc.? In dedicated config files
? Save this as a preset for future projects? No
```

首先进行：

```
npm install
```

开发时运行：

```
npm run serve
```

配置到服务器上时运行：

```
npm run build
```

运行测试unit tests

```
npm run test:unit
```

修复文件

```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
