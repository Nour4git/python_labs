import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    elements = soup.find_all(class_="ind")  #correct
    comments = [e.find_next(class_="comment") for e in elements if e.find_next(class_="comment")]
    
    keywords = {"python": 0, "javascript": 0, "typescript": 0, "go": 0, "c#": 0, "java": 0, "rust": 0}

    for comment in comments:
        comment_text = comment.get_text().lower()  
        words = [w.strip(".,/:;!@") for w in comment_text.split()]  # correct here

        for word in words:
            if word in keywords:
                keywords[word] += 1

    plt.bar(keywords.keys(), keywords.values())
    plt.xlabel("Language")
    plt.ylabel("# of Mentions")
    plt.title("Keyword Mentions in Comments")
    plt.show()

if __name__ == "__main__":
    main()
