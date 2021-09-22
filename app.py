from selenium import webdriver
import webbrowser


def convert_html_to_dict(articles_html, driver):
    articles = []

    for article in articles_html:
        driver.execute_script('arguments[0].scrollIntoView()', article)
        driver.implicitly_wait(1)
        title = article.find_element_by_css_selector('h2').text
        link = article.get_attribute('href')
        img_url = article.find_element_by_css_selector('img').get_attribute('src')
        if not img_url:
            img_url = article.find_element_by_css_selector('img').get_attribute('srcset')
        articles.append({'title': title, 'link': link, 'img_url': img_url})

    return articles


def generate_html_str(articles):
    html_str = '<h1>My TVN</h1>'

    for article in articles:
        link = article['link']
        img_url = article['img_url'].split()[0]
        html_str += f"""
        <section style='max-width: 500px; padding: 10px; margin-bottom: 20px; background: ghostwhite;'>
            <a style='color: black; text-decoration: none;' href='{link}' target='_blank'>
                <h2>{article['title']}</h2>
                <img src='{img_url}' />
            </a>
        </section>
        """

    return html_str


def main():
    driver = webdriver.Chrome('./chromedriver')
    driver.get('https://tvn24.pl')

    driver.implicitly_wait(5)

    btn_cookies = driver.find_element_by_css_selector('#onetrust-accept-btn-handler')
    btn_cookies.click()

    articles_html = driver.find_elements_by_css_selector(
        'article.teaser-wrapper__content:not(.html-teaser) .link__content>a')
    articles = convert_html_to_dict(articles_html, driver)

    driver.close()

    html = generate_html_str(articles)
    with open('news.html', 'w') as file:
        file.write(html)

    webbrowser.open('news.html')


if __name__ == '__main__':
    main()
