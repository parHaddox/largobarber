import azure.functions as func
import json
import logging
import os
import smtplib
import ssl
from email.message import EmailMessage


app = func.FunctionApp()


@app.route(route="/", auth_level=func.AuthLevel.ANONYMOUS)
def home(req: func.HttpRequest) -> func.HttpResponse:
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="description" content="#1 Barbershop delivers crisp cuts, fades, and beard work with a sporty edge in Largo, FL." />
        <meta name="keywords" content="Largo barber, #1 barbershop, fades, tapers, beard trim, hot towel shave, Largo Florida" />
        <meta name="author" content="#1 Barbershop" />
        <title>#1 Barbershop | Sporty, Modern Barber Shop</title>

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
            .nav-links a {
                color: var(--muted);
                text-decoration: none;
                margin-left: 18px;
                font-size: 0.95rem;
                transition: color 0.2s ease;
            }
            .nav-links a:hover { color: var(--accent-2); }

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
                    <img class="brand-logo" src="https://no1barbershop.com/wp-content/uploads/2025/09/Untitled-Logo-2.png" alt="#1 Barbershop logo" />
                    <span>#1 Barbershop</span>
                </div>
                <div class="nav-links">
                    <a href="#services">Services</a>
                    <a href="#team">Team</a>
                    <a href="#gallery">Gallery</a>
                    <a href="#visit">Visit</a>
                    <a href="#contact">Contact</a>
                </div>
            </div>
        </header>

        <main class="shell">
            <section class="hero">
                <div class="reveal">
                    <div class="eyebrow">Sporty. Sharp. Local.</div>
                    <h1>Look sharp. Feel great. Largo's #1 barbershop.</h1>
                    <p class="lede">
                        #1 Barbershop serves Clearwater, Largo, and Pinellas Park with precision haircuts, clean
                        fades, and classic hot towel shaves. Walk out looking crisp and feeling unstoppable.
                    </p>
                    <div class="cta-row">
                        <a class="btn btn-primary" href="https://booksy.com/en-us/1416187_1-barbershop_barber-shop_15985_largo#ba_s=sr_1" target="_blank" rel="noopener">Book on Booksy</a>
                        <a class="btn btn-secondary" href="tel:17272664047">Call Now</a>
                        <a class="btn btn-secondary" href="#visit">Visit Info</a>
                    </div>
                    <div class="badge-row">
                        <span class="badge">Se habla Espanol</span>
                        <span class="badge">Walk-ins welcome</span>
                        <span class="badge">4.9 rating, 200+ reviews</span>
                    </div>
                </div>
                <div class="hero-card reveal delay-2">
                    <h3>Game-ready grooming</h3>
                    <p>
                        From skin fades to sharp line-ups, we keep the details locked in. Walk-ins welcome; appointments
                        recommended for evenings and Saturdays.
                    </p>
                    <div class="badge-row">
                        <span class="badge">Fades & tapers</span>
                        <span class="badge">Beard shaping</span>
                        <span class="badge">Designs available</span>
                    </div>
                </div>
            </section>

            <section id="services">
                <div class="section-title">Services</div>
                <div class="section-sub">
                    Quick, clean, and consistent. Below are our core services with straightforward pricing. Walk-ins
                    welcome; appointments recommended.
                </div>
                <div class="grid">
                    <div class="card">
                        <h4>Haircut</h4>
                        <p>Classic or modern styles, tailored to your hair type and face shape.</p>
                        <div class="price">$30</div>
                    </div>
                    <div class="card">
                        <h4>Haircut & Beard (Includes Hot Towel)</h4>
                        <p>Full refresh: precise haircut plus beard trim with hot-towel finish.</p>
                        <div class="price">$35</div>
                    </div>
                    <div class="card">
                        <h4>Shape Up</h4>
                        <p>Edges and lines cleaned up between full cuts.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4>Barba / Beard Trim</h4>
                        <p>Detailed beard shaping and length control.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4>Hot Towel Shave</h4>
                        <p>Traditional straight-razor shave with hot-towel prep.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4>Line-Up & Hot-Towel Shave</h4>
                        <p>Crisp hairline/neckline plus a relaxing hot-towel shave.</p>
                        <div class="price">$15</div>
                    </div>
                    <div class="card">
                        <h4>Kids (12 & Under)</h4>
                        <p>Patient, kid-friendly cuts for a polished look.</p>
                        <div class="price">$25</div>
                    </div>
                    <div class="card">
                        <h4>Senior (65+)</h4>
                        <p>Gentle, precise haircut with extra care.</p>
                        <div class="price">$25</div>
                    </div>
                    <div class="card">
                        <h4>Senior (Haircut & Shave)</h4>
                        <p>Value combo for a clean, classic finish.</p>
                        <div class="price">$30</div>
                    </div>
                </div>
            </section>

            <section id="team">
                <div class="section-title">Meet the barbers</div>
                <div class="section-sub">
                    Skilled, bilingual, and tuned into the latest style. Each barber brings a fresh eye and steady
                    hands to every cut.
                </div>
                <div class="grid">
                    <div class="card profile-card" style="--bg-image: url('https://no1barbershop.com/wp-content/uploads/2025/09/AF591CC4-6DE7-48EE-9BDE-0A37A49999F8.jpg');">
                        <div class="profile">
                            <img src="https://no1barbershop.com/wp-content/uploads/2025/09/AF591CC4-6DE7-48EE-9BDE-0A37A49999F8.jpg" alt="Bismark Rodriguez" />
                            <div>
                                <h4>Bismark Rodriguez</h4>
                                <p>Cuban entrepreneur and Florida barber with 14 years of experience blending classic and modern style.</p>
                            </div>
                        </div>
                    </div>
                    <div class="card profile-card" style="--bg-image: url('https://no1barbershop.com/wp-content/uploads/2025/09/IMG_5047-scaled.jpg');">
                        <div class="profile">
                            <img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_5047-scaled.jpg" alt="Ery Lantigua" />
                            <div>
                                <h4>Ery Lantigua</h4>
                                <p>Dedicated barber with 8 years of experience crafting precise cuts and modern styles.</p>
                            </div>
                        </div>
                    </div>
                    <div class="card profile-card" style="--bg-image: url('https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2356-scaled.jpg');">
                        <div class="profile">
                            <img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2356-scaled.jpg" alt="Carlos" />
                            <div>
                                <h4>Carlos</h4>
                                <p>Blends classic technique with modern style to deliver sharp fades and friendly service.</p>
                            </div>
                        </div>
                    </div>
                    <div class="card profile-card" style="--bg-image: url('https://d2zdpiztbgorvt.cloudfront.net/region1/us/1635197/biz_photo/8b5c097d544a40299ab22c21b66028-1-barbersoop-alejandro-biz-photo-fbd144e6759c43d8869e1e99eb15c2-booksy.jpeg?size=640x427');">
                        <div class="profile">
                            <img src="https://d2zdpiztbgorvt.cloudfront.net/region1/us/1635197/biz_photo/8b5c097d544a40299ab22c21b66028-1-barbersoop-alejandro-biz-photo-fbd144e6759c43d8869e1e99eb15c2-booksy.jpeg?size=640x427" alt="Alejandro" />
                            <div>
                                <h4>Alejandro</h4>
                                <p>Clean blends, sharp line-ups, and client-first service.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <section id="gallery">
                <div class="section-title">Gallery</div>
                <div class="section-sub">
                    Fresh cuts and clean details from the shop floor.
                </div>
                <div class="gallery">
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2372-680x1024.jpg" alt="Gallery haircut 1" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2371-670x1024.jpg" alt="Gallery haircut 2" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2369-839x1024.jpg" alt="Gallery haircut 3" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/IMG_2368-615x1024.jpg" alt="Gallery haircut 4" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/E72B41E4-FF98-491B-BB20-C50CE0E24E69-562x1024.jpg" alt="Gallery haircut 5" /></div>
                    <div class="shot"><img src="https://no1barbershop.com/wp-content/uploads/2025/09/ED053B7F-AAC0-45F8-8F7A-D9643EFB3665-576x1024.jpg" alt="Gallery haircut 6" /></div>
                </div>
            </section>

            <section id="faq">
                <div class="section-title">Frequently Asked Questions</div>
                <div class="section-sub">Got questions? We have got answers.</div>
                <details>
                    <summary>Do you accept walk-ins or appointments?</summary>
                    <p>We welcome walk-ins all day and also offer online appointments for faster service, especially during evenings and weekends.</p>
                </details>
                <details>
                    <summary>Where are you located?</summary>
                    <p>We are in Largo, FL near Clearwater and Seminole, serving all of Pinellas County. Free parking available at 1600 Missouri Ave N, Suite 60, Largo FL 33770 in Town Center Plaza.</p>
                </details>
                <details>
                    <summary>What services do you offer?</summary>
                    <p>Precision men’s haircuts, skin fades, tapers, scissor cuts, kids’ cuts, beard trims, line-ups/shape-ups, and relaxing hot-towel straight-razor shaves.</p>
                </details>
                <details>
                    <summary>How long does a haircut take?</summary>
                    <p>Most haircuts take 25 to 35 minutes. Haircut and beard services usually run 40 to 50 minutes depending on style and hair type.</p>
                </details>
                <details>
                    <summary>Do you cut kids’ hair?</summary>
                    <p>Yes. Kids’ haircuts are one of our specialties. We keep it quick, clean, and friendly so they leave smiling.</p>
                </details>
                <details>
                    <summary>Can I request a specific barber?</summary>
                    <p>Yes. When booking online or checking in, you can select your preferred barber, subject to availability.</p>
                </details>
                <details>
                    <summary>Do you speak Spanish?</summary>
                    <p>Si. Hablamos espanol. Ask for service in Spanish anytime.</p>
                </details>
            </section>

            <section id="visit">
                <div class="section-title">Visit us</div>
                <div class="section-sub">
                    Drop in for a walk-in or call ahead for a time slot. Free parking and easy access in Largo.
                </div>
                <div class="contact-panel">
                    <div class="card callout">
                        <h4>Location</h4>
                        <p>1600 Missouri Ave N, Suite 60</p>
                        <p>Largo, FL 33770</p>
                        <p>See reviews, hours, and updates on Google Business.</p>
                        <div class="cta-row">
                            <a class="btn btn-secondary" href="https://share.google/GEwWiUlzCxeLzzzZO" target="_blank" rel="noopener">Google Business</a>
                            <a class="btn btn-secondary" href="https://www.google.com/maps?q=1600%20Missouri%20Ave%20N%20Suite%2060%2C%20Largo%2C%20FL%2033770" target="_blank" rel="noopener">Open Map</a>
                        </div>
                    </div>
                    <div class="card">
                        <h4>Hours</h4>
                        <p>Mon - Sat: 9:00am - 7:00pm</p>
                        <p>Tue: 10:00am - 7:00pm</p>
                        <p>Sunday: 10:00am - 4:00pm</p>
                    </div>
                    <div class="card">
                        <h4>Contact</h4>
                        <p>Phone: (727) 266-4047</p>
                        <p>Email: <a href="mailto:bismarkelnino@gmail.com">bismarkelnino@gmail.com</a></p>
                        <p>Instagram: <a href="https://www.instagram.com/no_1_barbershop?igsh=N2drb25yOGRxZnR1&utm_source=qr" target="_blank" rel="noopener">@no_1_barbershop</a></p>
                        <div class="cta-row">
                            <a class="btn btn-primary" href="https://booksy.com/en-us/1416187_1-barbershop_barber-shop_15985_largo#ba_s=sr_1" target="_blank" rel="noopener">Book on Booksy</a>
                            <a class="btn btn-secondary" href="tel:17272664047">Call Now</a>
                        </div>
                    </div>
                </div>
                <div class="card" style="margin-top: 18px;">
                    <h4>Map</h4>
                    <p style="color: var(--muted); margin-top: 0;">Find us fast with directions straight to the shop.</p>
                    <div style="border-radius: 16px; overflow: hidden; border: 1px solid var(--border); margin-top: 12px;">
                        <iframe
                            title="Largo No 1 Barber map"
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
                <div class="section-title">Contact us</div>
                <div class="section-sub">
                    Questions or ready to book? Contact our barbershop in Largo, FL. Call, book online, or send a message.
                </div>
                <div class="card">
                    <form id="contact-form">
                        <div class="form-grid">
                            <div>
                                <label for="contact-name">Your Name</label>
                                <input id="contact-name" name="name" type="text" placeholder="Your name" required />
                            </div>
                            <div>
                                <label for="contact-email">Your Email</label>
                                <input id="contact-email" name="email" type="email" placeholder="you@email.com" required />
                            </div>
                        </div>
                        <div style="margin-top: 12px;">
                            <label for="contact-message">Your Message</label>
                            <textarea id="contact-message" name="message" placeholder="How can we help?" required></textarea>
                        </div>
                        <div class="cta-row" style="margin-top: 16px;">
                            <button class="btn btn-primary" type="submit">Send Message</button>
                            <a class="btn btn-secondary" href="mailto:bismarkelnino@gmail.com">Email Directly</a>
                        </div>
                        <p id="form-status" class="status hidden"></p>
                        <p id="form-error" class="error"></p>
                    </form>
                </div>
            </section>

            <footer>
                <div>#1 Barbershop - Largo, FL</div>
                <div>Walk-ins welcome. Hablamos espanol. Book online today.</div>
            </footer>
        </main>
        <script>
            const form = document.getElementById("contact-form");
            const statusEl = document.getElementById("form-status");
            const errorEl = document.getElementById("form-error");

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
                    errorEl.textContent = "All fields are required.";
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
                        throw new Error(txt || "Request failed");
                    }
                    statusEl.innerHTML = '<span class="checkmark"></span> Thank you!';
                    statusEl.classList.remove("hidden");
                    form.reset();
                } catch (err) {
                    errorEl.textContent = "Error: " + err.message;
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
