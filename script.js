(function() {
    'use strict';

    // ---------- DOM 引用 ----------
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    const navAnchors = navLinks.querySelectorAll('a');
    const sections = document.querySelectorAll('section[id]');
    const fadeEls = document.querySelectorAll('.fade-up');

    // ---------- 1. 汉堡菜单 ----------
    hamburger.addEventListener('click', function() {
        const isOpen = navLinks.classList.toggle('open');
        hamburger.classList.toggle('active');
        hamburger.setAttribute('aria-expanded', isOpen);
    });

    navAnchors.forEach(anchor => {
        anchor.addEventListener('click', function() {
            navLinks.classList.remove('open');
            hamburger.classList.remove('active');
            hamburger.setAttribute('aria-expanded', 'false');
        });
    });

    // ---------- 2. 导航栏滚动效果 ----------
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;
        if (currentScroll > 20) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }, { passive: true });

    // ---------- 3. 滚动高亮当前导航项 ----------
    const sectionObserver = new IntersectionObserver(function(entries) {
        let activeId = null;
        for (const entry of entries) {
            if (entry.isIntersecting) {
                activeId = entry.target.id;
                break;
            }
        }
        if (!activeId) return;

        navAnchors.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + activeId) {
                link.classList.add('active');
            }
        });
    }, {
        threshold: 0.35,
        rootMargin: '0px 0px -40px 0px'
    });

    sections.forEach(section => {
        sectionObserver.observe(section);
    });

    // ---------- 4. 滚动渐入动画 ----------
    const fadeObserver = new IntersectionObserver(function(entries) {
        for (const entry of entries) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                fadeObserver.unobserve(entry.target);
            }
        }
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -20px 0px'
    });

    fadeEls.forEach(el => {
        fadeObserver.observe(el);
    });

    console.log('✅ 简历网站已启动 — 设计简约，内容专业。');
})();