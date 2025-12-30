import azure.functions as func
import json
import logging
import os
import smtplib
import ssl
from urllib.parse import urlsplit, urlunsplit
from email.message import EmailMessage


app = func.FunctionApp()


@app.route(route="/", auth_level=func.AuthLevel.ANONYMOUS)
def home(req: func.HttpRequest) -> func.HttpResponse:
    if req.url:
        parts = urlsplit(req.url)
        if parts.path.startswith("//"):
            normalized = urlunsplit((parts.scheme, parts.netloc, "/", parts.query, parts.fragment))
            return func.HttpResponse(status_code=301, headers={"Location": normalized})
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="description" data-i18n="meta_description" data-i18n-attr="content" content="#1 Barbershop delivers crisp cuts, fades, and beard work with a sporty edge in Largo, FL." />
        <meta name="keywords" data-i18n="meta_keywords" data-i18n-attr="content" content="Largo barber, #1 barbershop, fades, tapers, beard trim, hot towel shave, Largo Florida" />
        <meta name="author" content="#1 Barbershop" />
        <title data-i18n="meta_title">#1 Barbershop | Sporty, Modern Barber Shop</title>

        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Sora:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
        <link rel="icon" href="https://no1barbershop.com/wp-content/uploads/2025/09/Untitled-Logo-2.png" type="image/png" />

        <style>
            :root {
                --bg: #0c0b0f;
                --panel: #14121a;
                --text: #f5f1e8;
                --muted: #c6bfb2;
                --accent: #ff4d2e;
                --accent-2: #f5b641;
                --accent-3: #0fd1c9;
                --border: rgba(255, 255, 255, 0.08);
                --shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
            }
            * { box-sizing: border-box; }
            html, body {
                margin: 0;
                padding: 0;
                font-family: "Sora", "Helvetica Neue", Arial, sans-serif;
                background: radial-gradient(120% 80% at 10% 10%, #1e1a2d 0%, #0c0b0f 65%, #07060a 100%);
                color: var(--text);
                scroll-behavior: smooth;
            }
            body::before {
                content: "";
                position: fixed;
                inset: 0;
                background: linear-gradient(120deg, rgba(255, 77, 46, 0.15), rgba(15, 209, 201, 0.05) 40%, transparent 70%);
                pointer-events: none;
                z-index: 0;
            }
            .noise {
                position: fixed;
                inset: 0;
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E");
                pointer-events: none;
                z-index: 0;
            }
            .shell {
                position: relative;
                z-index: 1;
                max-width: 1200px;
                margin: 0 auto;
                padding: 30px 22px 96px;
            }
            header {
                position: sticky;
                top: 0;
                z-index: 10;
                background: rgba(12, 11, 15, 0.8);
                backdrop-filter: blur(16px);
                border-bottom: 1px solid var(--border);
            }
            .nav {
                max-width: 1200px;
                margin: 0 auto;
                padding: 18px 22px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .brand {
                display: flex;
                align-items: center;
                gap: 12px;
                font-family: "Bebas Neue", sans-serif;
                font-size: 1.6rem;
                letter-spacing: 0.08em;
            }
            .brand-logo {
                width: 84px;
                height: 84px;
                border-radius: 18px;
                object-fit: cover;
                border: 1px solid var(--border);
                background: #0f0e14;
            }
            .nav-links {
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .nav-links a {
                color: var(--muted);
                text-decoration: none;
                margin-left: 18px;
                font-size: 0.95rem;
                transition: color 0.2s ease;
            }
            .nav-links a:hover { color: var(--accent-2); }
            .lang-toggle {
                border-radius: 999px;
                border: 1px solid var(--border);
                background: rgba(255, 255, 255, 0.06);
                color: var(--text);
                font-size: 0.85rem;
                font-weight: 600;
                padding: 8px 14px;
                cursor: pointer;
                transition: border-color 0.2s ease, color 0.2s ease, transform 0.2s ease;
            }
            .lang-toggle:hover {
                border-color: rgba(255, 255, 255, 0.2);
                color: var(--accent-2);
                transform: translateY(-1px);
            }

            .hero {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 36px;
                align-items: center;
                padding: 42px 0 32px;
            }
            .eyebrow {
                text-transform: uppercase;
                letter-spacing: 0.2em;
                color: var(--accent-2);
                font-size: 0.75rem;
                font-weight: 600;
                margin-bottom: 12px;
            }
            h1 {
                font-family: "Bebas Neue", sans-serif;
                font-size: clamp(2.8rem, 6vw, 4.4rem);
                line-height: 0.95;
                margin: 0 0 16px;
            }
            .lede {
                color: var(--muted);
                font-size: 1.05rem;
                line-height: 1.7;
                max-width: 560px;
            }
            .cta-row {
                margin-top: 24px;
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
            }
            .btn {
                padding: 12px 18px;
                border-radius: 12px;
                border: 1px solid var(--border);
                color: var(--text);
                text-decoration: none;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            }
            .btn-primary {
                background: linear-gradient(135deg, var(--accent), var(--accent-2));
                color: #140c0a;
                box-shadow: 0 14px 30px rgba(255, 77, 46, 0.35);
            }
            .btn-secondary {
                background: rgba(255, 255, 255, 0.04);
            }
            .btn:hover {
                transform: translateY(-2px);
                border-color: rgba(255, 255, 255, 0.2);
                box-shadow: 0 16px 32px rgba(0, 0, 0, 0.35);
            }
            a:not(.btn) {
                color: var(--accent-2);
                text-decoration: none;
            }
            a:not(.btn):hover {
                color: var(--accent);
            }
            .hero-card {
                background: linear-gradient(135deg, rgba(255, 77, 46, 0.12), rgba(20, 18, 26, 0.8));
                border: 1px solid var(--border);
                border-radius: 22px;
                padding: 26px;
                box-shadow: var(--shadow);
                position: relative;
                overflow: hidden;
            }
            .hero-card::after {
                content: "";
                position: absolute;
                width: 180px;
                height: 180px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(15, 209, 201, 0.4), transparent 70%);
                top: -40px;
                right: -40px;
                filter: blur(6px);
            }
            .hero-card h3 {
                margin: 0 0 12px;
                font-size: 1.3rem;
            }
            .hero-card p {
                margin: 0;
                color: var(--muted);
                line-height: 1.6;
            }
            .badge-row {
                margin-top: 20px;
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .badge {
                padding: 8px 12px;
                border-radius: 999px;
                border: 1px solid var(--border);
                background: rgba(255, 255, 255, 0.04);
                font-size: 0.85rem;
                color: var(--muted);
            }

            section {
                margin-top: 64px;
            }
            .section-title {
                font-family: "Bebas Neue", sans-serif;
                font-size: 2.2rem;
                margin-bottom: 12px;
                letter-spacing: 0.08em;
            }
            .section-sub {
                color: var(--muted);
                max-width: 720px;
                line-height: 1.7;
                margin-bottom: 24px;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 18px;
            }
            .card {
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 18px;
                padding: 20px;
                box-shadow: var(--shadow);
            }
            .card h4 {
                margin: 0 0 8px;
                font-size: 1.1rem;
            }
            .card p {
                margin: 0;
                color: var(--muted);
                line-height: 1.6;
                font-size: 0.95rem;
            }
            .profile {
                display: grid;
                grid-template-columns: 96px 1fr;
                gap: 14px;
                align-items: center;
            }
            .profile img {
                width: 96px;
                height: 96px;
                border-radius: 18px;
                object-fit: cover;
                border: 1px solid var(--border);
                box-shadow: var(--shadow);
            }
            .profile-card {
                position: relative;
                overflow: hidden;
            }
            .profile-card::before {
                content: "";
                position: absolute;
                inset: 0;
                background-image: var(--bg-image);
                background-size: cover;
                background-position: center;
                opacity: 0;
                transform: scale(0.25);
                transform-origin: 28px 28px;
                transition: opacity 0.35s ease, transform 0.4s ease;
            }
            .profile-card::after {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(140deg, rgba(12, 11, 15, 0.2), rgba(12, 11, 15, 0.85));
                opacity: 0;
                transition: opacity 0.35s ease;
            }
            .profile-card:hover::before,
            .profile-card:hover::after {
                opacity: 1;
                transform: scale(1);
            }
            .profile-card .profile {
                position: relative;
                z-index: 1;
                transition: color 0.35s ease;
            }
            .profile-card:hover h4,
            .profile-card:hover p {
                color: #fef9f0;
            }
            .price {
                font-weight: 700;
                color: var(--accent-2);
                margin-top: 10px;
                font-size: 1.05rem;
            }
            .gallery {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 12px;
            }
            .shot {
                height: 220px;
                border-radius: 16px;
                border: 1px solid var(--border);
                background: #0f0e14;
                position: relative;
                overflow: hidden;
            }
            .shot img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            }
            .shot::after {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(160deg, transparent 40%, rgba(0, 0, 0, 0.35));
            }
            details {
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 14px 16px;
                box-shadow: var(--shadow);
            }
            details + details {
                margin-top: 12px;
            }
            summary {
                cursor: pointer;
                list-style: none;
                font-weight: 600;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            summary::-webkit-details-marker { display: none; }
            summary::after {
                content: "+";
                font-size: 1.2rem;
                color: var(--accent-2);
            }
            details[open] summary::after {
                content: "–";
            }
            details p {
                margin: 10px 0 0;
                color: var(--muted);
                line-height: 1.6;
            }
            .contact-panel {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 18px;
            }
            .contact-panel .card {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 12px;
                margin-top: 12px;
            }
            label {
                font-size: 0.85rem;
                color: var(--muted);
            }
            input, textarea {
                width: 100%;
                padding: 12px;
                border-radius: 10px;
                border: 1px solid var(--border);
                background: rgba(255, 255, 255, 0.04);
                color: var(--text);
                font-family: inherit;
                font-size: 0.95rem;
            }
            textarea { min-height: 120px; resize: vertical; }
            .status {
                margin-top: 12px;
                color: #9be5b0;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .status.hidden { display: none; }
            .error {
                margin-top: 12px;
                color: #ff9a9a;
                font-weight: 600;
            }
            .checkmark {
                width: 18px;
                height: 18px;
                border-radius: 50%;
                background: #2dd36f;
                display: inline-block;
                position: relative;
                flex: 0 0 auto;
            }
            .checkmark::after {
                content: "";
                position: absolute;
                left: 6px;
                top: 3px;
                width: 4px;
                height: 8px;
                border: 2px solid #fff;
                border-top: 0;
                border-left: 0;
                transform: rotate(45deg);
            }
            .callout {
                background: linear-gradient(140deg, rgba(255, 77, 46, 0.2), rgba(20, 18, 26, 0.9));
                border: 1px solid rgba(255, 77, 46, 0.3);
            }
            footer {
                margin-top: 80px;
                padding-top: 28px;
                border-top: 1px solid var(--border);
                color: var(--muted);
                font-size: 0.9rem;
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                justify-content: space-between;
            }

            .reveal {
                opacity: 0;
                transform: translateY(18px);
                animation: reveal 0.8s ease forwards;
            }
            .reveal.delay-1 { animation-delay: 0.2s; }
            .reveal.delay-2 { animation-delay: 0.4s; }
            .reveal.delay-3 { animation-delay: 0.6s; }

            @keyframes reveal {
                to { opacity: 1; transform: translateY(0); }
            }
            @media (max-width: 760px) {
                .nav-links { display: none; }
                .hero-card { margin-top: 10px; }
                footer { flex-direction: column; }
            }
        </style>
    </head>
    <body>
        <div class="noise"></div>
        <header>
            <div class="nav">
                <div class="brand">
                    <img class="brand-logo" src="https://no1barbershop.com/wp-content/uploads/2025/09/Untitled-Logo-2.png" alt="#1 Barbershop logo" data-i18n="logo_alt" data-i18n-attr="alt" />
                    <span>#1 Barbershop</span>
                </div>
                <div class="nav-links">
                    <a href="#services" data-i18n="nav_services">Services</a>
                    <a href="#team" data-i18n="nav_team">Team</a>
                    <a href="#gallery" data-i18n="nav_gallery">Gallery</a>
                    <a href="#visit" data-i18n="nav_visit">Visit</a>
                    <a href="#contact" data-i18n="nav_contact">Contact</a>
                </div>
                <button class="lang-toggle" id="lang-toggle" type="button" data-i18n="lang_toggle">Español</button>
            </div>
        </header>

        <main class="shell">
            <section class="hero">
                <div class="reveal">
                    <div class="eyebrow" data-i18n="eyebrow">Sporty. Sharp. Local.</div>
                    <h1 data-i18n="hero_title">Look sharp. Feel great. Largo's #1 barbershop.</h1>
                    <p class="lede" data-i18n="hero_lede">
                        #1 Barbershop serves Clearwater, Largo, and Pinellas Park with precision haircuts, clean
                        fades, and classic hot towel shaves. Walk out looking crisp and feeling unstoppable.
                    </p>
                    <div class="cta-row">
                        <a class="btn btn-primary" href="https://booksy.com/en-us/1416187_1-barbershop_barber-shop_15985_largo#ba_s=sr_1" target="_blank" rel="noopener" data-i18n="cta_book">Book on Booksy</a>
                        <a class="btn btn-secondary" href="tel:17272664047" data-i18n="cta_call">Call Now</a>
                        <a class="btn btn-secondary" href="#visit" data-i18n="cta_visit">Visit Info</a>
                    </div>
                    <div class="badge-row">
                        <span class="badge" data-i18n="badge_spanish">Se habla Español</span>
                        <span class="badge" data-i18n="badge_walkins">Walk-ins welcome</span>
                        <span class="badge" data-i18n="badge_rating">4.9 rating, 200+ reviews</span>
                    </div>
                </div>
                <div class="hero-card reveal delay-2">
                    <h3 data-i18n="hero_card_title">Game-ready grooming</h3>
                    <p data-i18n="hero_card_text">
                        From skin fades to sharp line-ups, we keep the details locked in. Walk-ins welcome; appointments
                        recommended for evenings and Saturdays.
                    </p>
                    <div class="badge-row">
                        <span class="badge" data-i18n="badge_fades">Fades & tapers</span>
                        <span class="badge" data-i18n="badge_beard">Beard shaping</span>
                        <span class="badge" data-i18n="badge_designs">Designs available</span>
                    </div>
                </div>
            </section>

            <section id="services">
                <div class="section-title" data-i18n="services_title">Services</div>
                <div class="section-sub" data-i18n="services_sub">
                    Quick, clean, and consistent. Below are our core services with straightforward pricing. Walk-ins
                    welcome; appointments recommended.
                </div>
                <div class="grid">
                    <div class="card">
                        <h4 data-i18n="service_haircut">Haircut</h4>
                        <p data-i18n="service_haircut_desc">Classic or modern styles, tailored to your hair type and face shape.</p>
                        <div class="price">$30</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_haircut_beard">Haircut & Beard (Includes Hot Towel)</h4>
                        <p data-i18n="service_haircut_beard_desc">Full refresh: precise haircut plus beard trim with hot-towel finish.</p>
                        <div class="price">$35</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_shapeup">Shape Up</h4>
                        <p data-i18n="service_shapeup_desc">Edges and lines cleaned up between full cuts.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_beard">Beard Trim</h4>
                        <p data-i18n="service_beard_desc">Detailed beard shaping and length control.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_hot_towel">Hot Towel Shave</h4>
                        <p data-i18n="service_hot_towel_desc">Traditional straight-razor shave with hot-towel prep.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_lineup">Line-Up & Hot-Towel Shave</h4>
                        <p data-i18n="service_lineup_desc">Crisp hairline/neckline plus a relaxing hot-towel shave.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_kids">Kids (12 & Under)</h4>
                        <p data-i18n="service_kids_desc">Patient, kid-friendly cuts for a polished look.</p>
                        <div class="price">$25</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_senior">Senior (65+)</h4>
                        <p data-i18n="service_senior_desc">Gentle, precise haircut with extra care.</p>
                        <div class="price">$25</div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="service_senior_combo">Senior (Haircut & Shave)</h4>
                        <p data-i18n="service_senior_combo_desc">Value combo for a clean, classic finish.</p>
                        <div class="price">$30</div>
                    </div>
                </div>
            </section>

            <section id="team">
                <div class="section-title" data-i18n="team_title">Meet the barbers</div>
                <div class="section-sub" data-i18n="team_sub">
                    Skilled, bilingual, and tuned into the latest style. Each barber brings a fresh eye and steady
                    hands to every cut.
                </div>
                <div class="grid">
                    <div class="card profile-card" style="--bg-image: url('https://no1barbershop.com/wp-content/uploads/2025/09/AF591CC4-6DE7-48EE-9BDE-0A37A49999F8.jpg');">
                        <div class="profile">
                            <img src="https://no1barbershop.com/wp-content/uploads/2025/09/AF591CC4-6DE7-48EE-9BDE-0A37A49999F8.jpg" alt="Bismark Rodriguez" />
                            <div>
                                <h4>Bismark Rodriguez</h4>
                                <p data-i18n="team_bismark">Cuban entrepreneur and Florida barber with 14 years of experience blending classic and modern style.</p>
                            </div>
                        </div>
                    </div>
                    <div class="card profile-card" style="--bg-image: url('https://no1barbershop.com/wp-content/uploads/2025/09/IMG_5047-scaled.jpg');">
                        <div class="profile">
                            <img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_5047-scaled.jpg" alt="Ery Lantigua" />
                            <div>
                                <h4>Ery Lantigua</h4>
                                <p data-i18n="team_ery">Dedicated barber with 8 years of experience crafting precise cuts and modern styles.</p>
                            </div>
                        </div>
                    </div>
                    <div class="card profile-card" style="--bg-image: url('https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2356-scaled.jpg');">
                        <div class="profile">
                            <img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2356-scaled.jpg" alt="Carlos" />
                            <div>
                                <h4>Carlos</h4>
                                <p data-i18n="team_carlos">Blends classic technique with modern style to deliver sharp fades and friendly service.</p>
                            </div>
                        </div>
                    </div>
                    <div class="card profile-card" style="--bg-image: url('https://d2zdpiztbgorvt.cloudfront.net/region1/us/1635197/biz_photo/8b5c097d544a40299ab22c21b66028-1-barbersoop-alejandro-biz-photo-fbd144e6759c43d8869e1e99eb15c2-booksy.jpeg?size=640x427');">
                        <div class="profile">
                            <img src="https://d2zdpiztbgorvt.cloudfront.net/region1/us/1635197/biz_photo/8b5c097d544a40299ab22c21b66028-1-barbersoop-alejandro-biz-photo-fbd144e6759c43d8869e1e99eb15c2-booksy.jpeg?size=640x427" alt="Alejandro" />
                            <div>
                                <h4>Alejandro</h4>
                                <p data-i18n="team_alejandro">Clean blends, sharp line-ups, and client-first service.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="gallery">
                <div class="section-title" data-i18n="gallery_title">Gallery</div>
                <div class="section-sub" data-i18n="gallery_sub">
                    Fresh cuts and clean details from the shop floor.
                </div>
                <div class="gallery">
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2372-680x1024.jpg" alt="Gallery haircut 1" data-i18n="gallery_alt_1" data-i18n-attr="alt" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2371-670x1024.jpg" alt="Gallery haircut 2" data-i18n="gallery_alt_2" data-i18n-attr="alt" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2369-839x1024.jpg" alt="Gallery haircut 3" data-i18n="gallery_alt_3" data-i18n-attr="alt" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2368-615x1024.jpg" alt="Gallery haircut 4" data-i18n="gallery_alt_4" data-i18n-attr="alt" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/E72B41E4-FF98-491B-BB20-C50CE0E24E69-562x1024.jpg" alt="Gallery haircut 5" data-i18n="gallery_alt_5" data-i18n-attr="alt" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/ED053B7F-AAC0-45F8-8F7A-D9643EFB3665-576x1024.jpg" alt="Gallery haircut 6" data-i18n="gallery_alt_6" data-i18n-attr="alt" /></div>
                </div>
            </section>

            <section id="faq">
                <div class="section-title" data-i18n="faq_title">Frequently Asked Questions</div>
                <div class="section-sub" data-i18n="faq_sub">Got questions? We have got answers.</div>
                <details>
                    <summary data-i18n="faq_q1">Do you accept walk-ins or appointments?</summary>
                    <p data-i18n="faq_a1">We welcome walk-ins all day and also offer online appointments for faster service, especially during evenings and weekends.</p>
                </details>
                <details>
                    <summary data-i18n="faq_q2">Where are you located?</summary>
                    <p data-i18n="faq_a2">We are in Largo, FL near Clearwater and Seminole, serving all of Pinellas County. Free parking available at 1600 Missouri Ave N, Suite 60, Largo FL 33770 in Town Center Plaza.</p>
                </details>
                <details>
                    <summary data-i18n="faq_q3">What services do you offer?</summary>
                    <p data-i18n="faq_a3">Precision men’s haircuts, skin fades, tapers, scissor cuts, kids’ cuts, beard trims, line-ups/shape-ups, and relaxing hot-towel straight-razor shaves.</p>
                </details>
                <details>
                    <summary data-i18n="faq_q4">How long does a haircut take?</summary>
                    <p data-i18n="faq_a4">Most haircuts take 25 to 35 minutes. Haircut and beard services usually run 40 to 50 minutes depending on style and hair type.</p>
                </details>
                <details>
                    <summary data-i18n="faq_q5">Do you cut kids’ hair?</summary>
                    <p data-i18n="faq_a5">Yes. Kids’ haircuts are one of our specialties. We keep it quick, clean, and friendly so they leave smiling.</p>
                </details>
                <details>
                    <summary data-i18n="faq_q6">Can I request a specific barber?</summary>
                    <p data-i18n="faq_a6">Yes. When booking online or checking in, you can select your preferred barber, subject to availability.</p>
                </details>
                <details>
                    <summary data-i18n="faq_q7">Do you speak Spanish?</summary>
                    <p data-i18n="faq_a7">Yes. We speak Spanish. Ask for service in Spanish anytime.</p>
                </details>
            </section>

            <section id="visit">
                <div class="section-title" data-i18n="visit_title">Visit us</div>
                <div class="section-sub" data-i18n="visit_sub">
                    Drop in for a walk-in or call ahead for a time slot. Free parking and easy access in Largo.
                </div>
                <div class="contact-panel">
                    <div class="card callout">
                        <h4 data-i18n="location_title">Location</h4>
                        <p data-i18n="location_p1">1600 Missouri Ave N, Suite 60</p>
                        <p data-i18n="location_p2">Largo, FL 33770</p>
                        <p data-i18n="location_p3">See reviews, hours, and updates on Google Business.</p>
                        <div class="cta-row">
                            <a class="btn btn-secondary" href="https://share.google/GEwWiUlzCxeLzzzZO" target="_blank" rel="noopener" data-i18n="location_cta_google">Google Business</a>
                            <a class="btn btn-secondary" href="https://www.google.com/maps?q=1600%20Missouri%20Ave%20N%20Suite%2060%2C%20Largo%2C%20FL%2033770" target="_blank" rel="noopener" data-i18n="location_cta_map">Open Map</a>
                        </div>
                    </div>
                    <div class="card">
                        <h4 data-i18n="hours_title">Hours</h4>
                        <p data-i18n="hours_p1">Mon - Sat: 9:00am - 7:00pm</p>
                        <p data-i18n="hours_p2">Tue: 10:00am - 7:00pm</p>
                        <p data-i18n="hours_p3">Sunday: 10:00am - 4:00pm</p>
                    </div>
                    <div class="card">
                        <h4 data-i18n="contact_title">Contact</h4>
                        <p data-i18n="contact_p1">Phone: (727) 266-4047</p>
                        <p><span data-i18n="contact_p2_label">Email:</span> <a href="mailto:bismarkelnino@gmail.com">bismarkelnino@gmail.com</a></p>
                        <p><span data-i18n="contact_p3_label">Instagram:</span> <a href="https://www.instagram.com/no_1_barbershop?igsh=N2drb25yOGRxZnR1&utm_source=qr" target="_blank" rel="noopener">@no_1_barbershop</a></p>
                        <div class="cta-row">
                            <a class="btn btn-primary" href="https://booksy.com/en-us/1416187_1-barbershop_barber-shop_15985_largo#ba_s=sr_1" target="_blank" rel="noopener" data-i18n="cta_book">Book on Booksy</a>
                            <a class="btn btn-secondary" href="tel:17272664047" data-i18n="cta_call">Call Now</a>
                        </div>
                    </div>
                </div>
                <div class="card" style="margin-top: 18px;">
                    <h4 data-i18n="map_title">Map</h4>
                    <p style="color: var(--muted); margin-top: 0;" data-i18n="map_sub">Find us fast with directions straight to the shop.</p>
                    <div style="border-radius: 16px; overflow: hidden; border: 1px solid var(--border); margin-top: 12px;">
                        <iframe
                            title="Largo No 1 Barber map"
                            data-i18n="map_iframe_title"
                            data-i18n-attr="title"
                            src="https://www.google.com/maps?q=1600%20Missouri%20Ave%20N%20Suite%2060%2C%20Largo%2C%20FL%2033770&output=embed"
                            width="100%"
                            height="320"
                            style="border:0;"
                            loading="lazy"
                            referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                </div>
            </section>

            <section id="contact">
                <div class="section-title" data-i18n="contactus_title">Contact us</div>
                <div class="section-sub" data-i18n="contactus_sub">
                    Questions or ready to book? Contact our barbershop in Largo, FL. Call, book online, or send a message.
                </div>
                <div class="card">
                    <form id="contact-form">
                        <div class="form-grid">
                            <div>
                                <label for="contact-name" data-i18n="form_name">Your Name</label>
                                <input id="contact-name" name="name" type="text" placeholder="Your name" data-i18n="form_name_placeholder" data-i18n-attr="placeholder" required />
                            </div>
                            <div>
                                <label for="contact-email" data-i18n="form_email">Your Email</label>
                                <input id="contact-email" name="email" type="email" placeholder="you@email.com" data-i18n="form_email_placeholder" data-i18n-attr="placeholder" required />
                            </div>
                        </div>
                        <div style="margin-top: 12px;">
                            <label for="contact-message" data-i18n="form_message">Your Message</label>
                            <textarea id="contact-message" name="message" placeholder="How can we help?" data-i18n="form_message_placeholder" data-i18n-attr="placeholder" required></textarea>
                        </div>
                        <div class="cta-row" style="margin-top: 16px;">
                            <button class="btn btn-primary" type="submit" data-i18n="form_send">Send Message</button>
                            <a class="btn btn-secondary" href="mailto:bismarkelnino@gmail.com" data-i18n="form_email_direct">Email Directly</a>
                        </div>
                        <p id="form-status" class="status hidden"></p>
                        <p id="form-error" class="error"></p>
                    </form>
                </div>
            </section>

            <footer>
                <div data-i18n="footer_left">#1 Barbershop - Largo, FL</div>
                <div data-i18n="footer_right">Walk-ins welcome. Hablamos español. Book online today.</div>
            </footer>
        </main>
        <script>
            const translations = {
                en: {
                    meta_title: "#1 Barbershop | Sporty, Modern Barber Shop",
                    meta_description: "#1 Barbershop delivers crisp cuts, fades, and beard work with a sporty edge in Largo, FL.",
                    meta_keywords: "Largo barber, #1 barbershop, fades, tapers, beard trim, hot towel shave, Largo Florida",
                    logo_alt: "#1 Barbershop logo",
                    nav_services: "Services",
                    nav_team: "Team",
                    nav_gallery: "Gallery",
                    nav_visit: "Visit",
                    nav_contact: "Contact",
                    lang_toggle: "Español",
                    lang_toggle_aria: "Switch language to Spanish",
                    eyebrow: "Sporty. Sharp. Local.",
                    hero_title: "Look sharp. Feel great. Largo's #1 barbershop.",
                    hero_lede: "#1 Barbershop serves Clearwater, Largo, and Pinellas Park with precision haircuts, clean fades, and classic hot towel shaves. Walk out looking crisp and feeling unstoppable.",
                    cta_book: "Book on Booksy",
                    cta_call: "Call Now",
                    cta_visit: "Visit Info",
                    badge_spanish: "Se habla Español",
                    badge_walkins: "Walk-ins welcome",
                    badge_rating: "4.9 rating, 200+ reviews",
                    hero_card_title: "Game-ready grooming",
                    hero_card_text: "From skin fades to sharp line-ups, we keep the details locked in. Walk-ins welcome; appointments recommended for evenings and Saturdays.",
                    badge_fades: "Fades & tapers",
                    badge_beard: "Beard shaping",
                    badge_designs: "Designs available",
                    services_title: "Services",
                    services_sub: "Quick, clean, and consistent. Below are our core services with straightforward pricing. Walk-ins welcome; appointments recommended.",
                    service_haircut: "Haircut",
                    service_haircut_desc: "Classic or modern styles, tailored to your hair type and face shape.",
                    service_haircut_beard: "Haircut & Beard (Includes Hot Towel)",
                    service_haircut_beard_desc: "Full refresh: precise haircut plus beard trim with hot-towel finish.",
                    service_shapeup: "Shape Up",
                    service_shapeup_desc: "Edges and lines cleaned up between full cuts.",
                    service_beard: "Beard Trim",
                    service_beard_desc: "Detailed beard shaping and length control.",
                    service_hot_towel: "Hot Towel Shave",
                    service_hot_towel_desc: "Traditional straight-razor shave with hot-towel prep.",
                    service_lineup: "Line-Up & Hot-Towel Shave",
                    service_lineup_desc: "Crisp hairline/neckline plus a relaxing hot-towel shave.",
                    service_kids: "Kids (12 & Under)",
                    service_kids_desc: "Patient, kid-friendly cuts for a polished look.",
                    service_senior: "Senior (65+)",
                    service_senior_desc: "Gentle, precise haircut with extra care.",
                    service_senior_combo: "Senior (Haircut & Shave)",
                    service_senior_combo_desc: "Value combo for a clean, classic finish.",
                    team_title: "Meet the barbers",
                    team_sub: "Skilled, bilingual, and tuned into the latest style. Each barber brings a fresh eye and steady hands to every cut.",
                    team_bismark: "Cuban entrepreneur and Florida barber with 14 years of experience blending classic and modern style.",
                    team_ery: "Dedicated barber with 8 years of experience crafting precise cuts and modern styles.",
                    team_carlos: "Blends classic technique with modern style to deliver sharp fades and friendly service.",
                    team_alejandro: "Clean blends, sharp line-ups, and client-first service.",
                    gallery_title: "Gallery",
                    gallery_sub: "Fresh cuts and clean details from the shop floor.",
                    gallery_alt_1: "Gallery haircut 1",
                    gallery_alt_2: "Gallery haircut 2",
                    gallery_alt_3: "Gallery haircut 3",
                    gallery_alt_4: "Gallery haircut 4",
                    gallery_alt_5: "Gallery haircut 5",
                    gallery_alt_6: "Gallery haircut 6",
                    faq_title: "Frequently Asked Questions",
                    faq_sub: "Got questions? We have got answers.",
                    faq_q1: "Do you accept walk-ins or appointments?",
                    faq_a1: "We welcome walk-ins all day and also offer online appointments for faster service, especially during evenings and weekends.",
                    faq_q2: "Where are you located?",
                    faq_a2: "We are in Largo, FL near Clearwater and Seminole, serving all of Pinellas County. Free parking available at 1600 Missouri Ave N, Suite 60, Largo FL 33770 in Town Center Plaza.",
                    faq_q3: "What services do you offer?",
                    faq_a3: "Precision men’s haircuts, skin fades, tapers, scissor cuts, kids’ cuts, beard trims, line-ups/shape-ups, and relaxing hot-towel straight-razor shaves.",
                    faq_q4: "How long does a haircut take?",
                    faq_a4: "Most haircuts take 25 to 35 minutes. Haircut and beard services usually run 40 to 50 minutes depending on style and hair type.",
                    faq_q5: "Do you cut kids’ hair?",
                    faq_a5: "Yes. Kids’ haircuts are one of our specialties. We keep it quick, clean, and friendly so they leave smiling.",
                    faq_q6: "Can I request a specific barber?",
                    faq_a6: "Yes. When booking online or checking in, you can select your preferred barber, subject to availability.",
                    faq_q7: "Do you speak Spanish?",
                    faq_a7: "Yes. We speak Spanish. Ask for service in Spanish anytime.",
                    visit_title: "Visit us",
                    visit_sub: "Drop in for a walk-in or call ahead for a time slot. Free parking and easy access in Largo.",
                    location_title: "Location",
                    location_p1: "1600 Missouri Ave N, Suite 60",
                    location_p2: "Largo, FL 33770",
                    location_p3: "See reviews, hours, and updates on Google Business.",
                    location_cta_google: "Google Business",
                    location_cta_map: "Open Map",
                    hours_title: "Hours",
                    hours_p1: "Mon - Sat: 9:00am - 7:00pm",
                    hours_p2: "Tue: 10:00am - 7:00pm",
                    hours_p3: "Sunday: 10:00am - 4:00pm",
                    contact_title: "Contact",
                    contact_p1: "Phone: (727) 266-4047",
                    contact_p2_label: "Email:",
                    contact_p3_label: "Instagram:",
                    map_title: "Map",
                    map_sub: "Find us fast with directions straight to the shop.",
                    map_iframe_title: "Largo No 1 Barber map",
                    contactus_title: "Contact us",
                    contactus_sub: "Questions or ready to book? Contact our barbershop in Largo, FL. Call, book online, or send a message.",
                    form_name: "Your Name",
                    form_name_placeholder: "Your name",
                    form_email: "Your Email",
                    form_email_placeholder: "you@email.com",
                    form_message: "Your Message",
                    form_message_placeholder: "How can we help?",
                    form_send: "Send Message",
                    form_email_direct: "Email Directly",
                    footer_left: "#1 Barbershop - Largo, FL",
                    footer_right: "Walk-ins welcome. Hablamos español. Book online today.",
                    status_thanks: "Thank you!",
                    error_required: "All fields are required.",
                    error_prefix: "Error: ",
                    error_request_failed: "Request failed.",
                    error_send_failed: "Failed to send message.",
                    error_not_configured: "Email service not configured."
                },
                es: {
                    meta_title: "#1 Barbershop | Barbería deportiva y moderna",
                    meta_description: "#1 Barbershop ofrece cortes definidos, fades y trabajo de barba con un toque deportivo en Largo, FL.",
                    meta_keywords: "barbero en Largo, #1 barbershop, fades, tapers, recorte de barba, afeitado con toalla caliente, Largo Florida",
                    logo_alt: "Logotipo de #1 Barbershop",
                    nav_services: "Servicios",
                    nav_team: "Equipo",
                    nav_gallery: "Galería",
                    nav_visit: "Visítanos",
                    nav_contact: "Contacto",
                    lang_toggle: "English",
                    lang_toggle_aria: "Cambiar idioma a inglés",
                    eyebrow: "Deportivo. Preciso. Local.",
                    hero_title: "Luce impecable. Siéntete genial. La barbería #1 de Largo.",
                    hero_lede: "#1 Barbershop atiende Clearwater, Largo y Pinellas Park con cortes de precisión, fades limpios y afeitados clásicos con toalla caliente. Sal con un look fresco y seguro.",
                    cta_book: "Reserva en Booksy",
                    cta_call: "Llama ahora",
                    cta_visit: "Información de visita",
                    badge_spanish: "Se habla español",
                    badge_walkins: "Sin cita, bienvenido",
                    badge_rating: "4.9 de calificación, 200+ reseñas",
                    hero_card_title: "Arreglo listo para el juego",
                    hero_card_text: "De skin fades a line-ups definidos, cuidamos cada detalle. Sin cita, bienvenido; se recomiendan citas para tardes y sábados.",
                    badge_fades: "Fades y tapers",
                    badge_beard: "Perfilado de barba",
                    badge_designs: "Diseños disponibles",
                    services_title: "Servicios",
                    services_sub: "Rápido, limpio y consistente. Estos son nuestros servicios principales con precios claros. Sin cita, bienvenido; se recomiendan citas.",
                    service_haircut: "Corte de cabello",
                    service_haircut_desc: "Estilos clásicos o modernos, adaptados a tu tipo de cabello y forma del rostro.",
                    service_haircut_beard: "Corte y barba (incluye toalla caliente)",
                    service_haircut_beard_desc: "Renovación completa: corte preciso más recorte de barba con acabado de toalla caliente.",
                    service_shapeup: "Shape up",
                    service_shapeup_desc: "Líneas y contornos limpios entre cortes completos.",
                    service_beard: "Recorte de barba",
                    service_beard_desc: "Perfilado detallado y control de longitud.",
                    service_hot_towel: "Afeitado con toalla caliente",
                    service_hot_towel_desc: "Afeitado tradicional con navaja y preparación con toalla caliente.",
                    service_lineup: "Line-up y afeitado con toalla caliente",
                    service_lineup_desc: "Línea de cabello y nuca definidas con un relajante afeitado con toalla caliente.",
                    service_kids: "Niños (12 y menos)",
                    service_kids_desc: "Cortes pacientes y amigables para niños.",
                    service_senior: "Senior (65+)",
                    service_senior_desc: "Corte delicado y preciso con atención extra.",
                    service_senior_combo: "Senior (corte y afeitado)",
                    service_senior_combo_desc: "Combo con buen valor para un acabado limpio y clásico.",
                    team_title: "Conoce a los barberos",
                    team_sub: "Expertos, bilingües y al día con el estilo. Cada barbero aporta una mirada fresca y manos firmes en cada corte.",
                    team_bismark: "Empresario cubano y barbero en Florida con 14 años de experiencia combinando estilo clásico y moderno.",
                    team_ery: "Barbero dedicado con 8 años de experiencia en cortes precisos y estilos modernos.",
                    team_carlos: "Combina técnica clásica con estilo moderno para ofrecer fades definidos y servicio amable.",
                    team_alejandro: "Mezclas limpias, line-ups definidos y servicio centrado en el cliente.",
                    gallery_title: "Galería",
                    gallery_sub: "Cortes frescos y detalles limpios desde el piso de la barbería.",
                    gallery_alt_1: "Corte de cabello en galería 1",
                    gallery_alt_2: "Corte de cabello en galería 2",
                    gallery_alt_3: "Corte de cabello en galería 3",
                    gallery_alt_4: "Corte de cabello en galería 4",
                    gallery_alt_5: "Corte de cabello en galería 5",
                    gallery_alt_6: "Corte de cabello en galería 6",
                    faq_title: "Preguntas frecuentes",
                    faq_sub: "¿Tienes preguntas? Tenemos respuestas.",
                    faq_q1: "¿Aceptan sin cita o con cita?",
                    faq_a1: "Recibimos sin cita todo el día y también ofrecemos citas en línea para un servicio más rápido, especialmente en tardes y fines de semana.",
                    faq_q2: "¿Dónde están ubicados?",
                    faq_a2: "Estamos en Largo, FL cerca de Clearwater y Seminole, atendiendo todo el condado de Pinellas. Estacionamiento gratis en 1600 Missouri Ave N, Suite 60, Largo FL 33770 en Town Center Plaza.",
                    faq_q3: "¿Qué servicios ofrecen?",
                    faq_a3: "Cortes de cabello para hombres, skin fades, tapers, cortes con tijera, cortes para niños, recortes de barba, line-ups/shape-ups y afeitados relajantes con toalla caliente y navaja.",
                    faq_q4: "¿Cuánto dura un corte?",
                    faq_a4: "La mayoría de los cortes toman de 25 a 35 minutos. Los servicios de corte y barba suelen durar de 40 a 50 minutos según el estilo y tipo de cabello.",
                    faq_q5: "¿Cortan el cabello a niños?",
                    faq_a5: "Sí. Los cortes para niños son una de nuestras especialidades. Lo hacemos rápido, limpio y amable para que salgan sonriendo.",
                    faq_q6: "¿Puedo pedir un barbero específico?",
                    faq_a6: "Sí. Al reservar en línea o registrarte, puedes seleccionar tu barbero preferido según disponibilidad.",
                    faq_q7: "¿Hablan español?",
                    faq_a7: "Sí. Hablamos español. Pide servicio en español cuando quieras.",
                    visit_title: "Visítanos",
                    visit_sub: "Pasa sin cita o llama para reservar un horario. Estacionamiento gratis y fácil acceso en Largo.",
                    location_title: "Ubicación",
                    location_p1: "1600 Missouri Ave N, Suite 60",
                    location_p2: "Largo, FL 33770",
                    location_p3: "Ve reseñas, horarios y actualizaciones en Google Business.",
                    location_cta_google: "Google Business",
                    location_cta_map: "Abrir mapa",
                    hours_title: "Horario",
                    hours_p1: "Lun - Sáb: 9:00am - 7:00pm",
                    hours_p2: "Mar: 10:00am - 7:00pm",
                    hours_p3: "Domingo: 10:00am - 4:00pm",
                    contact_title: "Contacto",
                    contact_p1: "Teléfono: (727) 266-4047",
                    contact_p2_label: "Correo:",
                    contact_p3_label: "Instagram:",
                    map_title: "Mapa",
                    map_sub: "Encuéntranos rápido con direcciones directas a la barbería.",
                    map_iframe_title: "Mapa de Largo No 1 Barber",
                    contactus_title: "Contáctanos",
                    contactus_sub: "¿Preguntas o listo para reservar? Contacta nuestra barbería en Largo, FL. Llama, reserva en línea o envía un mensaje.",
                    form_name: "Tu nombre",
                    form_name_placeholder: "Tu nombre",
                    form_email: "Tu correo",
                    form_email_placeholder: "tu@correo.com",
                    form_message: "Tu mensaje",
                    form_message_placeholder: "¿En qué podemos ayudar?",
                    form_send: "Enviar mensaje",
                    form_email_direct: "Enviar correo",
                    footer_left: "#1 Barbershop - Largo, FL",
                    footer_right: "Sin cita, bienvenido. Hablamos español. Reserva en línea hoy.",
                    status_thanks: "¡Gracias!",
                    error_required: "Todos los campos son obligatorios.",
                    error_prefix: "Error: ",
                    error_request_failed: "La solicitud falló.",
                    error_send_failed: "No se pudo enviar el mensaje.",
                    error_not_configured: "El servicio de correo no está configurado."
                }
            };

            const languageToggle = document.getElementById("lang-toggle");
            let currentLang = "en";

            const t = (key) => {
                const table = translations[currentLang] || translations.en;
                return table[key] || translations.en[key] || "";
            };

            const applyTranslations = () => {
                document.documentElement.lang = currentLang;
                document.querySelectorAll("[data-i18n]").forEach((el) => {
                    const key = el.getAttribute("data-i18n");
                    const value = t(key);
                    if (!value) {
                        return;
                    }
                    const attr = el.getAttribute("data-i18n-attr");
                    if (attr) {
                        el.setAttribute(attr, value);
                    } else {
                        el.textContent = value;
                    }
                });

                if (languageToggle) {
                    languageToggle.setAttribute("aria-label", t("lang_toggle_aria"));
                }
            };

            const getPreferredLanguage = () => {
                const saved = localStorage.getItem("lang");
                if (saved && translations[saved]) {
                    return saved;
                }
                const languages = navigator.languages || [navigator.language || "en"];
                const matched = languages.find((lang) => lang && lang.toLowerCase().startsWith("es"));
                return matched ? "es" : "en";
            };

            const setLanguage = (lang, persist = false) => {
                if (!translations[lang]) {
                    return;
                }
                currentLang = lang;
                if (persist) {
                    localStorage.setItem("lang", lang);
                }
                applyTranslations();
            };

            if (languageToggle) {
                languageToggle.addEventListener("click", () => {
                    const nextLang = currentLang === "en" ? "es" : "en";
                    setLanguage(nextLang, true);
                });
            }

            setLanguage(getPreferredLanguage());

            const form = document.getElementById("contact-form");
            const statusEl = document.getElementById("form-status");
            const errorEl = document.getElementById("form-error");

            const translateServerError = (message) => {
                const trimmed = message.trim();
                if (!trimmed) {
                    return t("error_request_failed");
                }
                if (trimmed === "All fields are required.") {
                    return t("error_required");
                }
                if (trimmed === "Failed to send message.") {
                    return t("error_send_failed");
                }
                if (trimmed === "Email service not configured.") {
                    return t("error_not_configured");
                }
                return message;
            };

            form.addEventListener("submit", async (event) => {
                event.preventDefault();
                statusEl.classList.add("hidden");
                statusEl.innerHTML = "";
                errorEl.textContent = "";

                const payload = {
                    name: document.getElementById("contact-name").value.trim(),
                    email: document.getElementById("contact-email").value.trim(),
                    message: document.getElementById("contact-message").value.trim()
                };

                if (!payload.name || !payload.email || !payload.message) {
                    errorEl.textContent = t("error_required");
                    return;
                }

                try {
                    const resp = await fetch("/contact", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    });
                    if (!resp.ok) {
                        const txt = await resp.text();
                        throw new Error(translateServerError(txt) || t("error_request_failed"));
                    }
                    statusEl.innerHTML = `<span class="checkmark"></span> ${t("status_thanks")}`;
                    statusEl.classList.remove("hidden");
                    form.reset();
                } catch (err) {
                    errorEl.textContent = t("error_prefix") + err.message;
                }
            });
        </script>
    </body>
    </html>
    """
    return func.HttpResponse(html_content, mimetype="text/html")


@app.route(route="contact", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def contact(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        body = {}

    name = str(body.get("name", "")).strip()
    email = str(body.get("email", "")).strip()
    message = str(body.get("message", "")).strip()

    if not name or not email or not message:
        return func.HttpResponse("All fields are required.", status_code=400)

    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USERNAME")
    smtp_pass = os.environ.get("SMTP_PASSWORD")
    smtp_use_ssl = os.environ.get("SMTP_USE_SSL", "false").lower() in ("1", "true", "yes")
    smtp_starttls = os.environ.get("SMTP_STARTTLS", "true").lower() in ("1", "true", "yes")

    if not smtp_host:
        logging.error("Missing SMTP configuration (SMTP_HOST)")
        return func.HttpResponse("Email service not configured.", status_code=500)

    to_email = os.environ.get("CONTACT_TO_EMAIL", "bismarkelnino@gmail.com")
    from_email = os.environ.get("CONTACT_FROM_EMAIL", smtp_user or "no-reply@example.com")

    subject = f"New contact from {name}"
    plain_content = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Reply-To"] = email
    msg.set_content(plain_content)

    try:
        if smtp_use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10, context=context) as server:
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                if smtp_starttls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                if smtp_user and smtp_pass:
                    server.login(smtp_user, smtp_pass)
                server.send_message(msg)
        logging.info("Contact email sent via SMTP to %s", to_email)
        return func.HttpResponse(json.dumps({"ok": True}), mimetype="application/json", status_code=200)
    except Exception as e:
        logging.error("Failed to send contact email: %s", e)
        return func.HttpResponse("Failed to send message.", status_code=500)
