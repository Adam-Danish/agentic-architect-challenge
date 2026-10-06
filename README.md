# Part 1: Customer support email system

The system checks each email for urgent issues and repeated contacts before the AI drafts a reply. For other emails, the AI classifies the topic, searches approved FAQs and PDFs, and drafts a response using supported information. A human reviews the draft before sending it.

Emails mentioning data loss, service outage, or a security breach, and customers with more than 3 contacts in 7 days, go to a human before any AI draft. Refund answers must use the approved policy; unclear cases go to a human.

![Part 1 flowchart](part1-flowchart.png)


# Part 2: Web summarizer

The script extracts a webpage’s main text with Trafilatura. If it finds fewer than 30 words, Playwright loads the page in Chromium and extraction is tried again. Long text is split into chunks and summarized with Gemini. The final summary is limited to 100 words.

### Run locally

Open a terminal in the repository folder, then run:

```bat
cd part2
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python web_summarizer.py
```

Enter a webpage URL when prompted. If enough text is found, enter your own Gemini API key in the terminal; the key will not be displayed as you type. An internet connection is required.

Test pages: [Python About](https://www.python.org/about/) for a short page and [JavaScript Quotes](https://quotes.toscrape.com/js/) for browser fallback. On the JavaScript Quotes page, normal extraction found 6 words; browser fallback found 189 words.

### Bottlenecks and fixes

- **JavaScript pages:** Trafilatura may miss text added after the page loads. If it finds fewer than 30 words, Playwright opens the page in a browser and the script tries again. A genuinely short page may trigger this step unnecessarily.
- **Long pages:** The script splits the text into chunks (smaller sections). Gemini summarizes each chunk, then combines them into a final summary of no more than 100 words. A page with many chunks may hit Gemini's request limit.
