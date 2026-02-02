/**
 * TechBlog - 主脚本文件
 * 包含主题切换、移动端菜单、滚动动画等功能
 */

// ================================
// 主题切换
// ================================
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle?.querySelector('i');

// 检查本地存储的主题或系统偏好
function getInitialTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        return savedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// 应用主题
function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (themeIcon) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// 初始化主题
const currentTheme = getInitialTheme();
applyTheme(currentTheme);

// 主题切换事件
themeToggle?.addEventListener('click', () => {
    const newTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(newTheme);
    localStorage.setItem('theme', newTheme);
});

// 监听系统主题变化
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
        applyTheme(e.matches ? 'dark' : 'light');
    }
});

// ================================
// 移动端菜单
// ================================
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const navMenu = document.querySelector('.nav-menu');

mobileMenuToggle?.addEventListener('click', () => {
    navMenu?.classList.toggle('active');
    const icon = mobileMenuToggle.querySelector('i');
    icon.className = navMenu?.classList.contains('active') ? 'fas fa-times' : 'fas fa-bars';
});

// 点击导航链接后关闭移动端菜单
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu?.classList.remove('active');
        if (mobileMenuToggle) {
            mobileMenuToggle.querySelector('i').className = 'fas fa-bars';
        }
    });
});

// ================================
// 导航栏滚动效果
// ================================
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // 添加/移除滚动样式
    if (currentScroll > 50) {
        navbar?.classList.add('scrolled');
    } else {
        navbar?.classList.remove('scrolled');
    }
    
    // 隐藏/显示导航栏
    if (currentScroll > lastScroll && currentScroll > 100) {
        navbar?.style.transform = 'translateY(-100%)';
    } else {
        navbar?.style.transform = 'translateY(0)';
    }
    
    lastScroll = currentScroll;
});

// ================================
// 滚动动画
// ================================
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// 观察需要动画的元素
document.querySelectorAll('.post-card, .tech-card, .stat-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// 添加动画类样式
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`;
document.head.appendChild(style);

// ================================
// 平滑滚动到锚点
// ================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            e.preventDefault();
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ================================
// 订阅表单处理
// ================================
const newsletterForm = document.querySelector('.newsletter-form');

newsletterForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = newsletterForm.querySelector('input[type="email"]').value;
    
    // 模拟提交
    const button = newsletterForm.querySelector('button');
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 提交中...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> 订阅成功!';
        button.style.background = '#22c55e';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = '';
            button.disabled = false;
            newsletterForm.reset();
        }, 2000);
    }, 1500);
});

// ================================
// 联系表单处理
// ================================
const contactForm = document.querySelector('.contact-form form');

contactForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const submitBtn = contactForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    submitBtn.textContent = '发送中...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        submitBtn.textContent = '发送成功!';
        submitBtn.style.background = '#22c55e';
        
        setTimeout(() => {
            submitBtn.textContent = originalText;
            submitBtn.style.background = '';
            submitBtn.disabled = false;
            contactForm.reset();
        }, 2000);
    }, 1500);
});

// ================================
// 打字机效果（可选）
// ================================
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// 为英雄区域的标题添加打字机效果（可选）
const heroTitle = document.querySelector('.hero-title');
if (heroTitle && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const originalText = heroTitle.innerHTML;
    // 保存原始HTML，简化版本不启用打字机效果
    // typeWriter(heroTitle, originalText, 50);
}

// ================================
// 代码高亮（简单实现）
// ================================
function highlightCode() {
    document.querySelectorAll('pre code').forEach(block => {
        // 简单的语法高亮
        let html = block.innerHTML;
        
        // 关键字
        html = html.replace(/\b(const|let|var|function|return|if|else|for|while|class|import|export|from|async|await|try|catch)\b/g, 
            '<span style="color: #c678dd;">$1</span>');
        
        // 字符串
        html = html.replace(/(['"`])(.*?)\1/g, 
            '<span style="color: #98c379;">$1$2$1</span>');
        
        // 注释
        html = html.replace(/(\/\/.*$|\/\*[\s\S]*?\*\/)/gm, 
            '<span style="color: #5c6370; font-style: italic;">$1</span>');
        
        // 数字
        html = html.replace(/\b(\d+)\b/g, 
            '<span style="color: #d19a66;">$1</span>');
        
        block.innerHTML = html;
    });
}

// 页面加载完成后执行代码高亮
document.addEventListener('DOMContentLoaded', highlightCode);

// ================================
// 阅读量计数（模拟）
// ================================
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const updateCounter = () => {
        current += increment;
        if (current < target) {
            element.textContent = Math.floor(current).toLocaleString() + '+';
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toLocaleString() + '+';
        }
    };
    
    updateCounter();
}

// 当统计区域进入视口时触发动画
const statsSection = document.querySelector('.hero-stats');
if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.stat-number');
                counters.forEach(counter => {
                    const text = counter.textContent;
                    const num = parseInt(text.replace(/[^\d]/g, ''));
                    if (!isNaN(num)) {
                        animateCounter(counter, num);
                    }
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    statsObserver.observe(statsSection);
}

// ================================
// 返回顶部按钮
// ================================
const backToTopButton = document.createElement('button');
backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopButton.className = 'back-to-top';
backToTopButton.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    border: none;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
`;

document.body.appendChild(backToTopButton);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 500) {
        backToTopButton.style.opacity = '1';
        backToTopButton.style.visibility = 'visible';
    } else {
        backToTopButton.style.opacity = '0';
        backToTopButton.style.visibility = 'hidden';
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ================================
// 页面加载动画
// ================================
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

console.log('🚀 TechBlog loaded successfully!');
