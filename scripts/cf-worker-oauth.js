/**
 * Decap CMS OAuth Proxy for Cloudflare Workers
 * 处理 GitHub OAuth 登录流程
 */

// 配置
const CONFIG = {
  // 你的 GitHub OAuth App 信息
  githubClientId: 'YOUR_GITHUB_CLIENT_ID',
  githubClientSecret: 'YOUR_GITHUB_CLIENT_SECRET',
  
  // 允许的域名
  allowedOrigins: [
    'https://your-blog.pages.dev',
    'http://localhost:8080',
    'http://127.0.0.1:8080'
  ]
};

// CORS 头
function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin || '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400'
  };
}

// 处理请求
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin');
    
    // 检查来源
    const allowedOrigin = CONFIG.allowedOrigins.find(o => origin?.startsWith(o)) || '*';
    
    // 处理 CORS 预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(allowedOrigin)
      });
    }
    
    try {
      // 路由
      switch (url.pathname) {
        case '/auth':
          return handleAuth(request, allowedOrigin);
        case '/callback':
          return handleCallback(request, allowedOrigin);
        case '/success':
          return handleSuccess(request);
        default:
          return new Response('Not Found', { status: 404 });
      }
    } catch (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: {
          ...corsHeaders(allowedOrigin),
          'Content-Type': 'application/json'
        }
      });
    }
  }
};

// 处理授权请求
async function handleAuth(request, allowedOrigin) {
  const url = new URL(request.url);
  const provider = url.searchParams.get('provider');
  
  if (provider !== 'github') {
    return new Response('Unsupported provider', { 
      status: 400,
      headers: corsHeaders(allowedOrigin)
    });
  }
  
  // 构建 GitHub OAuth URL
  const githubAuthUrl = new URL('https://github.com/login/oauth/authorize');
  githubAuthUrl.searchParams.set('client_id', CONFIG.githubClientId);
  githubAuthUrl.searchParams.set('scope', 'repo');
  githubAuthUrl.searchParams.set('state', generateState());
  
  return Response.redirect(githubAuthUrl.toString(), 302);
}

// 处理 OAuth 回调
async function handleCallback(request, allowedOrigin) {
  const url = new URL(request.url);
  const code = url.searchParams.get('code');
  
  if (!code) {
    return new Response('Missing authorization code', { status: 400 });
  }
  
  // 用 code 换 access_token
  const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      client_id: CONFIG.githubClientId,
      client_secret: CONFIG.githubClientSecret,
      code: code
    })
  });
  
  const tokenData = await tokenResponse.json();
  
  if (tokenData.error) {
    return new Response(JSON.stringify(tokenData), { 
      status: 400,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
  
  // 返回 success 页面，带 token
  const successHtml = generateSuccessHtml(tokenData.access_token);
  
  return new Response(successHtml, {
    headers: {
      ...corsHeaders(allowedOrigin),
      'Content-Type': 'text/html'
    }
  });
}

// 生成随机 state
function generateState() {
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15);
}

// 生成成功页面 HTML
function generateSuccessHtml(token) {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>授权成功</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      background: #f5f5f5;
    }
    .container {
      text-align: center;
      padding: 2rem;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      max-width: 400px;
    }
    .success-icon {
      font-size: 64px;
      color: #22c55e;
      margin-bottom: 1rem;
    }
    h1 {
      margin: 0 0 1rem;
      color: #333;
    }
    p {
      color: #666;
      margin-bottom: 1.5rem;
    }
    .loading {
      display: inline-block;
      width: 24px;
      height: 24px;
      border: 3px solid #f3f3f3;
      border-top: 3px solid #3498db;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="success-icon">✓</div>
    <h1>授权成功</h1>
    <p>正在跳转回管理后台...</p>
    <div class="loading"></div>
  </div>
  
  <script>
    // 将 token 传回父窗口
    if (window.opener) {
      window.opener.postMessage({
        type: 'authorization:github:success',
        token: '${token}'
      }, '*');
      setTimeout(() => window.close(), 1000);
    } else {
      // 保存到 localStorage 并跳转
      localStorage.setItem('decap-cms-token', '${token}');
      window.location.href = '/admin/';
    }
  </script>
</body>
</html>`;
}

// 处理 success 请求
async function handleSuccess(request) {
  return new Response('OK', { status: 200 });
}
