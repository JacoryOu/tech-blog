/**
 * 开发服务器 - 带热重载
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

console.log('🚀 启动开发服务器...\n');

// 首次构建
console.log('📦 执行初始构建...');
require('./build.js');

console.log('\n📝 启动文件监视...');
console.log('   监控目录: content/posts/\n');

// 使用 chokidar 监视文件变化
try {
  const chokidar = require('chokidar');
  
  const watcher = chokidar.watch(path.join(__dirname, '../content/posts'), {
    ignored: /(^|[\/\\])\../,
    persistent: true
  });
  
  let buildTimeout;
  
  watcher.on('change', filePath => {
    console.log(`📝 文件变化: ${path.basename(filePath)}`);
    clearTimeout(buildTimeout);
    buildTimeout = setTimeout(() => {
      console.log('🔄 重新构建...\n');
      require('./build.js');
      console.log('\n✅ 构建完成，刷新浏览器查看更新\n');
    }, 500);
  });
  
  watcher.on('add', filePath => {
    console.log(`➕ 新文章: ${path.basename(filePath)}`);
    clearTimeout(buildTimeout);
    buildTimeout = setTimeout(() => {
      console.log('🔄 重新构建...\n');
      require('./build.js');
      console.log('\n✅ 构建完成\n');
    }, 500);
  });
  
} catch (err) {
  console.log('⚠️ 未安装 chokidar，热重载功能不可用');
  console.log('   运行: npm install\n');
}

// 启动 HTTP 服务器
console.log('🌐 启动 HTTP 服务器...');
console.log('   网站地址: http://localhost:8080');
console.log('   管理后台: http://localhost:8080/admin\n');

const server = exec('python3 -m http.server 8080', {
  cwd: path.join(__dirname, '..')
});

server.stdout.on('data', data => {
  // 静默处理
});

server.stderr.on('data', data => {
  // 静默处理
});

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n👋 停止服务器...');
  server.kill();
  process.exit(0);
});

console.log('💡 提示: 按 Ctrl+C 停止服务器\n');
