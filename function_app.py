import azure.functions as func


app = func.FunctionApp()


@app.route(route="/", auth_level=func.AuthLevel.ANONYMOUS)
def home(req: func.HttpRequest) -> func.HttpResponse:
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="description" content="Largo No 1 Barber delivers crisp cuts, fades, and beard work with a sporty edge in Largo, FL." />
        <meta name="keywords" content="Largo barber, fades, tapers, beard trim, Hispanic barber shop, Largo Florida" />
        <meta name="author" content="Largo No 1 Barber" />
        <title>Largo No 1 Barber | Sporty, Modern Barber Shop</title>

        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Sora:wght@300;400;500;600;700&display=swap" rel="stylesheet" />

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
            .brand-badge {
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--accent), var(--accent-2));
                display: grid;
                place-items: center;
                color: #120c0a;
                font-weight: 700;
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
            .price {
                font-weight: 700;
                color: var(--accent-2);
                margin-top: 10px;
                font-size: 1.05rem;
            }
            .gallery {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 12px;
            }
            .shot {
                height: 160px;
                border-radius: 16px;
                border: 1px solid var(--border);
                background: linear-gradient(135deg, rgba(255, 77, 46, 0.25), rgba(15, 209, 201, 0.25));
                position: relative;
                overflow: hidden;
            }
            .shot::after {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(160deg, transparent 40%, rgba(0, 0, 0, 0.4));
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
                    <div class="brand-badge">1</div>
                    <span>Largo No 1 Barber</span>
                </div>
                <div class="nav-links">
                    <a href="#services">Services</a>
                    <a href="#team">Team</a>
                    <a href="#gallery">Gallery</a>
                    <a href="#visit">Visit</a>
                </div>
            </div>
        </header>

        <main class="shell">
            <section class="hero">
                <div class="reveal">
                    <div class="eyebrow">Sporty. Sharp. Local.</div>
                    <h1>Fresh cuts, clean fades, and detail that pops.</h1>
                    <p class="lede">
                        Largo No 1 Barber is the neighborhood spot for modern tapers, precision beard work, and
                        high-energy vibes. Walk out looking crisp and feeling unstoppable.
                    </p>
                    <div class="cta-row">
                        <a class="btn btn-primary" href="https://booksy.com/en-us/1416187_1-barbershop_barber-shop_15985_largo#ba_s=sr_1" target="_blank" rel="noopener">Book on Booksy</a>
                        <a class="btn btn-secondary" href="#services">View Services</a>
                        <a class="btn btn-secondary" href="#visit">Visit Info</a>
                    </div>
                    <div class="badge-row">
                        <span class="badge">Se habla Espanol</span>
                        <span class="badge">Walk-ins welcome</span>
                        <span class="badge">Youth + athletic styles</span>
                    </div>
                </div>
                <div class="hero-card reveal delay-2">
                    <h3>Game-ready grooming</h3>
                    <p>
                        From skin fades to sharp line-ups, we keep the details locked in. Come through solo or with the
                        squad and leave camera-ready.
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
                    Fast, clean, consistent. Choose your cut and we will make it yours. Ask about custom designs
                    and combo packages.
                </div>
                <div class="grid">
                    <div class="card">
                        <h4>Signature Fade</h4>
                        <p>Skin, mid, or low fades with crisp lines and texture finishing.</p>
                        <div class="price">$30</div>
                    </div>
                    <div class="card">
                        <h4>Classic Cut</h4>
                        <p>Scissor and clipper work with a clean neckline and style finish.</p>
                        <div class="price">$25</div>
                    </div>
                    <div class="card">
                        <h4>Beard Sculpt</h4>
                        <p>Shape, line, and clean up with hot towel service.</p>
                        <div class="price">$18</div>
                    </div>
                    <div class="card">
                        <h4>Cut + Beard</h4>
                        <p>Full service combo for a sharp head-to-chin refresh.</p>
                        <div class="price">$42</div>
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
                    <div class="card">
                        <h4>Alex - Owner</h4>
                        <p>Fade specialist with a focus on athletic cuts and clean detail work.</p>
                    </div>
                    <div class="card">
                        <h4>Chris - Barber</h4>
                        <p>Known for beard sculpting, razor line-ups, and precision tapers.</p>
                    </div>
                    <div class="card">
                        <h4>Marcos - Barber</h4>
                        <p>Creative designs, modern texture, and a smooth client experience.</p>
                    </div>
                </div>
            </section>

            <section id="gallery">
                <div class="section-title">Gallery</div>
                <div class="section-sub">
                    Swap in real photos of your best work. These placeholders keep the layout ready for new shots.
                </div>
                <div class="gallery">
                    <div class="shot"></div>
                    <div class="shot"></div>
                    <div class="shot"></div>
                    <div class="shot"></div>
                    <div class="shot"></div>
                    <div class="shot"></div>
                </div>
            </section>

            <section id="visit">
                <div class="section-title">Visit us</div>
                <div class="section-sub">
                    Drop in for a walk-in or call ahead for a time slot. Update the details below with the shop address,
                    phone, and socials.
                </div>
                <div class="contact-panel">
                    <div class="card callout">
                        <h4>Location</h4>
                        <p>Largo No 1 Barber - Largo, FL</p>
                        <p>See reviews, hours, and updates on Google Business.</p>
                        <div class="cta-row">
                            <a class="btn btn-secondary" href="https://share.google/GEwWiUlzCxeLzzzZO" target="_blank" rel="noopener">Google Business</a>
                            <a class="btn btn-secondary" href="https://www.google.com/maps?q=Largo%20No%201%20Barber%20Largo%20FL" target="_blank" rel="noopener">Open Map</a>
                        </div>
                    </div>
                    <div class="card">
                        <h4>Hours</h4>
                        <p>Mon - Fri: 10:00am - 7:00pm</p>
                        <p>Saturday: 9:00am - 6:00pm</p>
                        <p>Sunday: 10:00am - 4:00pm</p>
                    </div>
                    <div class="card">
                        <h4>Contact</h4>
                        <p>Phone: (727) 555-0101</p>
                        <p>Instagram: @LargoNo1Barber</p>
                        <div class="cta-row">
                            <a class="btn btn-primary" href="https://booksy.com/en-us/1416187_1-barbershop_barber-shop_15985_largo#ba_s=sr_1" target="_blank" rel="noopener">Book on Booksy</a>
                            <a class="btn btn-secondary" href="tel:17275550101">Call Now</a>
                        </div>
                    </div>
                </div>
                <div class="card" style="margin-top: 18px;">
                    <h4>Map</h4>
                    <p style="color: var(--muted); margin-top: 0;">Find us fast with directions straight to the shop.</p>
                    <div style="border-radius: 16px; overflow: hidden; border: 1px solid var(--border); margin-top: 12px;">
                        <iframe
                            title="Largo No 1 Barber map"
                            src="https://www.google.com/maps?q=Largo%20No%201%20Barber%20Largo%20FL&output=embed"
                            width="100%"
                            height="320"
                            style="border:0;"
                            loading="lazy"
                            referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                </div>
            </section>

            <footer>
                <div>Largo No 1 Barber - Largo, FL</div>
                <div>Built for walk-ins, fades, and game-day confidence.</div>
            </footer>
        </main>
    </body>
    </html>
    """
    return func.HttpResponse(html_content, mimetype="text/html")
