# 🗞️ News Sumup Collector

A Python script that collects articles from RSS feeds, cleans their content, and automatically generates summaries in **French or English**.  
I use it to stay up to date with tech news — without having to read 6000-word articles. 😅

## 🚀 Features

- 🔗 Multilingual RSS feed parsing
- 🧠 Automatic summarization using transformer models (`bart`, `barthez`)
- 📝 Saves results as JSON
- 📜 Basic structured logging throughout the process

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/news_sumup_collector.git
cd news_sumup_collector

```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r config/requirements.txt
```

4. Add the RSS feed URLs you want to follow in feeds/feeds.txt, then run the main script:
   By default, the app summarizes 3 articles per source — you can change that in main.py.

```bash
python main.py
```

5. Summaries will be saved as JSON files in the data/ folder (for now).

## 🧰 Tech Stack

- newspaper3k
- feedparser
- transformers

## 🤖 Models Used

BARThez for French summarization (by Moussa Kamal Eddine)
🔗 https://huggingface.co/moussaKam/barthez
📜 License: Apache 2.0

DistilBART for English summarization (by Hugging Face)
🔗 https://huggingface.co/sshleifer/distilbart-cnn-12-6
📜 License: Apache 2.0

🧠 TODO

- Send summaries as an email newsletter

- Automate the collection to run periodically

- Add more RSS feeds

- Add content filters

## 👤 Author

2521 — myself.

## 🪪 License

This project is licensed under the MIT License.
It also makes use of external models released under the Apache 2.0 License (see the LICENSE file for details).
