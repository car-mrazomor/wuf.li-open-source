# wuf.li - Privacy-Focused Email Hosting

[wuf.li](https://wuf.li) is an open-source email hosting service designed for privacy-conscious users. It allows anyone to use and host their own secure email service with ease. Built on [Mailcow](https://mailcow.email/), wuf.li provides a reliable and user-friendly email experience.

## Features
- **Privacy First** – No tracking, no ads, just email.
- **Self-Hostable** – Deploy on your own server for full control.
- **Cloudflare Turnstile Integration** – Protects against spam and abuse.
- **Open Source** – Transparent and community-driven development.

## Installation
To set up wuf.li on your own server, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/car-mrazomor/wuf.li-open-source.git
   cd wuf.li-open-source
   ```
2. Configure Mailcow as per the official [Mailcow setup guide](https://mailcow.email/).
3. Update the Cloudflare Turnstile secret key:
   - In `app.py` (or relevant file), find line 251 and change:
     ```python
     secret: str = "<SUPER_SECRET_CF_KEY>"
     ```
   - Replace `<SUPER_SECRET_CF_KEY>` with your actual Cloudflare Turnstile secret key.
4. Add your Mailcow API key:
   - Inside `static/.secret_key`, place your Mailcow API key.
5. Deploy your instance and enjoy private, secure email hosting!

## Contributing
We welcome contributions! If you'd like to improve wuf.li, submit a pull request or open an issue.

## Support
For questions or support, please open an issue on GitHub or reach out to the community.

