`markdown
<div align="center">

<img width="100%" alt="Deepanshu Lathar working across product analytics, AI, document verification, real-time chat and campus events" src="assets/hero-banner.webp">

# Deepanshu Lathar

### Full-stack & AI engineer · Founder's Office at PicaPool

**I take B2C products from idea to deployment — I scope what matters from user behaviour, build the AI workflow hands-on, and measure what ships through funnels, attribution and cohort retention.**

Founder's Office Intern at PicaPool, Delhi · B.Tech, Computer Science & Engineering, Lovely Professional University (2024–2028)

[Website](https://deepanshulathar.com/) · [CV](https://cv.143.lat/) · [LinkedIn](https://www.linkedin.com/in/deepanshulathar/) · [Résumé](https://deepanshulathar.com/Deepanshu-Lathar-Resume.pdf) · [Email](mailto:deepanshulathar@gmail.com)

**Available full-time, on-site in Bengaluru for Jan–Jun 2027**

</div>

---

## Skills — what I work with

<div align="center">

### Languages & core tech

<img alt="Skill bubbles: TypeScript, JavaScript, Python, React, Next.js, Node.js, FastAPI, PostgreSQL, Supabase, Firebase, Tailwind CSS, HTML, CSS" src="https://skillicons.dev/icons?i=ts,js,python,react,nextjs,nodejs,fastapi,postgres,supabase,firebase,tailwind,html,css">

### Shipping & quality

<img alt="Skill bubbles: Vercel, Docker, Git, GitHub" src="https://skillicons.dev/icons?i=vercel,docker,git,github">

### AI, product & the rest of the stack

<img alt="Claude" src="https://img.shields.io/badge/Claude-191919?style=for-the-badge">
<img alt="OpenAI" src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge">
<img alt="Groq" src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge">
<img alt="Gemini" src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge">
<img alt="Prompt engineering" src="https://img.shields.io/badge/Prompt_Engineering-5B4DFF?style=for-the-badge">
<img alt="RAG · pgvector" src="https://img.shields.io/badge/RAG_%C2%B7_pgvector-336791?style=for-the-badge">
<img alt="n8n automation" src="https://img.shields.io/badge/n8n_Automation-EA4B71?style=for-the-badge">
<img alt="Claude Code" src="https://img.shields.io/badge/Claude_Code-191919?style=for-the-badge">
<img alt="Cursor" src="https://img.shields.io/badge/Cursor-000000?style=for-the-badge">
<img alt="SQL" src="https://img.shields.io/badge/SQL-336791?style=for-the-badge">
<img alt="Socket.IO" src="https://img.shields.io/badge/Socket.IO-010101?style=for-the-badge">
<img alt="WebRTC" src="https://img.shields.io/badge/WebRTC-333333?style=for-the-badge">
<img alt="Razorpay" src="https://img.shields.io/badge/Razorpay-0C2451?style=for-the-badge">
<img alt="OCR" src="https://img.shields.io/badge/OCR-2F855A?style=for-the-badge">
<img alt="Vitest" src="https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge">
<img alt="Playwright" src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge">
<img alt="CI/CD" src="https://img.shields.io/badge/CI%2FCD-2088FF?style=for-the-badge">

</div>

**In words, so nothing is hidden behind an icon:**

- **Product:** user research & pain-point discovery · product-opportunity identification · idea-to-deployment ownership · prioritisation · GTM strategy · funnel & cohort analysis · retention · A/B testing · attribution modelling · UX copywriting
- **AI & LLM:** LLM APIs (OpenAI, Anthropic Claude, Groq, Gemini) · prompt engineering · multi-provider failover · RAG (pgvector, hybrid retrieval) · agent & workflow automation (n8n) · LLM-output validation · Claude Code · Cursor
- **Programming & engineering:** TypeScript / JavaScript · Python · SQL · Next.js · React · Node.js · FastAPI · PostgreSQL · Supabase · Firebase · Vercel · Docker · CI/CD · automated testing & reliability (Vitest, Playwright)

---

## Top projects

### 1. Gapl — see what a recruiter sees in your resume

[Live beta](https://gapl.143.lat/) · [Sample report](https://gapl.vercel.app/demo) · [Repo](https://github.com/latharrr/gapl)

<img width="100%" alt="Gapl homepage hero — a printed resume with yellow highlights on a sunlit table, beside pens and a glass of chai" src="https://gapl.vercel.app/living/img/hero.jpg">
<sub>The hero image live on gapl.143.lat — open the live beta or the sample report to see the product itself.</sub>

A candidate uploads a resume and a job description, and Gapl reads it the way a recruiter at that company tier would: a readiness score, an ATS fit, the line that sank it, and a learning roadmap that ends in projects to build — then it helps rewrite the CV.

- **Stack:** Next.js, TypeScript, Firebase, Razorpay, Tailwind. One LLM gateway with provider fallback and output validation powers the parsing, scoring and recruiter-verdict simulator.
- **The proof:** a synthetic-fixture evaluation harness of 44 documents found and fixed a false-rejection bug affecting billing-domain resumes — 41/44 → **44/44**. These are synthetic pipeline tests, not a claim of real-world AI accuracy.
- **In use:** live beta with **10+ early testers**, with HMAC-verified Razorpay billing and full email-open to paid-conversion attribution.

### 2. ProofMart — bank statements, re-added

[Live beta](https://proofmart.shop/) · [Repo](https://github.com/latharrr/Proofmart.shop)

<img width="100%" alt="ProofMart landing page showing a sample statement with ticked and ringed balances" src="https://raw.githubusercontent.com/latharrr/Proofmart.shop/main/docs/images/home.png">
<sub>Real screenshot from the ProofMart repo: the landing page re-foots a built-in sample statement.</sub>

Bank statements lie by arithmetic, and nobody re-adds the rows. ProofMart runs an upload → classify → extract → OCR → verify pipeline over a PDF statement, re-adds its own numbers, and pins every finding to real page coordinates, so each verdict is auditable and reproducible.

<img width="100%" alt="ProofMart Evidence Rail flagging a running balance that is 1,500.00 too high on a synthetic statement" src="https://raw.githubusercontent.com/latharrr/Proofmart.shop/main/docs/images/evidence-rail.png">
<sub>Real screenshot from the ProofMart repo: the Evidence Rail on a synthetic statement generated by the repo's own test fixtures — no real data.</sub>

- **Stack:** Next.js, TypeScript, Supabase, OCR. Public API and Node CLI on the same pipeline.
- **The proof:** six deterministic markers and a fixed verdict order — `INCONCLUSIVE`, `FAIL`, `REVIEW`, `CLEAR`. No AI model sits in the verdict path, dossiers are Ed25519-signed, and anyone can verify one with no account.
- **Testing:** 15 Vitest suites and 4 Playwright end-to-end specs.

### 3. LPU Connect (LpuTV) — anonymous chat that stays anonymous

[Live](https://lputv.vercel.app/) · [Repo](https://github.com/latharrr/lpuconnect)

| Landing | Dashboard | A chat |
|---|---|---|
| <img width="100%" alt="LpuTV landing page screenshot" src="https://raw.githubusercontent.com/latharrr/lpuconnect/main/docs/screenshots/landing.png"> | <img width="100%" alt="LpuTV dashboard screenshot" src="https://raw.githubusercontent.com/latharrr/lpuconnect/main/docs/screenshots/dashboard.png"> | <img width="100%" alt="LpuTV anonymous chat screenshot" src="https://raw.githubusercontent.com/latharrr/lpuconnect/main/docs/screenshots/chat.png"> |
<sub>All three are real screenshots from the lpuconnect repo.</sub>

Talk to a random LPU student for ten minutes. Nobody sees who you are until you both say yes: a matchmaking engine pairs users into timed sessions, video unlocks only if both want it, and names are revealed only after a mutual friend accept — every step enforced by the server, not just the UI.

- **Stack:** React, Node.js, Socket.IO, WebRTC, SQLite.
- **The proof:** the test suite scans the database to prove message text is never stored. The backend carries 47 tests at about 84% line coverage, and a load test ran 10,000 simulated users with zero failures.
- **Hardened:** rate limiting, CORS lockdown and XSS sanitisation.

### 4. Dandiya Nights — PicaPool's partner-matching app

Built at PicaPool · Consumer event web app, Delhi edition

<img width="100%" alt="Illustration of the Dandiya Nights partner-matching app — phone mockups with a profile card and a match celebration, garba dancers behind" src="assets/dandiya-nights-illustration.webp">
<sub>Illustration, not a screenshot — Dandiya Nights was a live PicaPool product with no public screenshot, so this picture shows the idea, not the real interface.</sub>

For Navratri, PicaPool needed to pair people who wanted a Dandiya partner. I owned the product decisions end to end: onboarding, a swipe-pacing economy with referral bonuses, and a privacy-first cross-promotion into the PicaPool app.

- **The proof:** the activation funnel (visitor → OTP → profile) was tracked daily while live — the Delhi edition recorded **640 signups and 174 matches over 5 days**.
- **Why it matters here:** it is the product side of the same job — growth mechanics, funnels and retention, not just code.

---

## Experience

**Founder's Office Intern — PicaPool, Jul 2025 – Present.** Hyperlocal group-buying and discovery platform, Delhi. Shipped **15+ production internal tools in 8 weeks** — CRM with role-based access, WhatsApp Business API dashboard, campaign attribution, merchant onboarding — owning ideation through implementation. Replaced download-count reporting with an event-fingerprinting and deduplication attribution system that supported a two-month campus push reaching **3,000+ students**. Built an AI-assisted analytics workflow so founders query business data in natural language and receive daily KPI digests, with generated SQL constrained by AST validation to read-only queries.

**Product & Growth Intern, Founder's Office — UniLyf, Jan 2026 – May 2026.** Pre-launch campus social platform (UK), remote. Built a demand-validation framework from 15 deeply profiled beta users, using cohort analysis to isolate the actions correlated with Day-7 retention. Led a cross-functional team of 6, and ran the pre-launch Instagram channel to 360 followers and **100K+ monthly views**.

**Event Coordinator → HR Coordinator — Dept. of Student Organisations, LPU, Mar 2025 – Present.** Promoted within 4 months. Coordinate **225+ student organisations** and executed **30+ large-scale campus events** end to end.

**Freelance — Web Development & Growth, Jun 2025 – Feb 2026.** Launched and managed a Shopify storefront for Spraykart LLP, ran SEO and lead generation for a D2C accountancy practice, and delivered storefronts and site builds for other clients.

## Education & certificates

**Lovely Professional University, Phagwara — B.Tech, Computer Science and Engineering, 2024–2028** · CGPA 7.15

Young Innovator Internship Challenge, Edition 2 (Scaler School of Technology, Jun 2025) · McKinsey Forward Program (Apr 2026) · Deloitte Data Analytics Job Simulation (Sep 2025) · Summer Training in Artificial Intelligence (LPU, Aug 2026)

---

<div align="center">

**Want the checked version of something? Build with me.**

[Email](mailto:deepanshulathar@gmail.com) · [LinkedIn](https://www.linkedin.com/in/deepanshulathar/) · [Website](https://deepanshulathar.com/) · [CV](https://cv.143.lat/)

<sub>Available full-time, on-site in Bengaluru for Jan–Jun 2027</sub>

</div>
`
