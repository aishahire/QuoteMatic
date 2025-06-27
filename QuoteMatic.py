import requests
from bs4 import BeautifulSoup
import random
import pyperclip

BASE_URL = "https://quotes.toscrape.com"

# 🧠 Get quotes from a page
def get_quotes(page_url="/"):
    full_url = BASE_URL + page_url
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []
    for quote in soup.select('.quote'):
        text = quote.find('span', class_='text').text.strip()
        author = quote.find('small', class_='author').text.strip()
        tags = [tag.text for tag in quote.select('.tags .tag')]
        quotes.append({
            'text': text,
            'author': author,
            'tags': tags
        })
    return quotes


# 🎯 Display quote
def display_quote(quote):
    print("\n📝 Quote:")
    print(f"\"{quote['text']}\"")
    print(f"— {quote['author']}  | Tags: {', '.join(quote['tags'])}")
    return quote


# 🎛️ Main Menu
def main():
    all_quotes = []
    current_page = "/"

    while True:
        print("\n🌟 QuoteMatic — Your Daily Dose of Inspiration 🌟")
        print("1. Show a random quote")
        print("2. Filter by tag (e.g., life, love, humor)")
        print("3. Search by author")
        print("4. Copy last quote to clipboard")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            all_quotes = get_quotes("/")
            quote = display_quote(random.choice(all_quotes))

        elif choice == "2":
            tag = input("Enter tag to filter (e.g., love, humor, life): ").lower()
            all_quotes = get_quotes("/")
            filtered = [q for q in all_quotes if tag in [t.lower() for t in q['tags']]]
            if filtered:
                quote = display_quote(random.choice(filtered))
            else:
                print("❌ No quotes found for that tag.")

        elif choice == "3":
            author_name = input("Enter author name (e.g., Albert Einstein): ").lower()
            found = False
            page = "/"
            while True:
                quotes = get_quotes(page)
                for q in quotes:
                    if author_name in q['author'].lower():
                        display_quote(q)
                        found = True
                        break
                if found or 'next' not in BeautifulSoup(requests.get(BASE_URL + page).text, 'html.parser').select_one('.next a', href=True):
                    break
                next_link = BeautifulSoup(requests.get(BASE_URL + page).text, 'html.parser').select_one('.next a', href=True)
                page = next_link['href'] if next_link else None

            if not found:
                print("❌ No quotes found by that author.")

        elif choice == "4":
            try:
                pyperclip.copy(quote['text'] + " — " + quote['author'])
                print("✅ Quote copied to clipboard!")
            except:
                print("⚠️ No quote available or clipboard feature not supported.")

        elif choice == "5":
            print("👋 Thank you for using QuoteMatic!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
