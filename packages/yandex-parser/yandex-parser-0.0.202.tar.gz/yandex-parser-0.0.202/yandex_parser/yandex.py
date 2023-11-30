from pyquery import PyQuery as pq

from yandex_parser.exceptions import YandexParserError


class Elements:
    elements_class = '.serp-item.serp-item_card:not([data-fast-name]) .Organic'
    title_class = 'span.OrganicTitleContentSpan.organic__title'
    href_class = '.OrganicTitle-Link'
    description_classes = [('.Organic-ContentWrapper.organic__content-wrapper '
                            '.TextContainer.OrganicText.organic__text.text-container.Typo.Typo_text_m.Typo_line_m '
                            '.OrganicTextContentSpan'),
                           ('.Organic-ContentWrapper.organic__content-wrapper '
                            '.Organic-ByLink.Typo.Typo_text_m.Typo_line_m'),
                           ('.Organic-ContentWrapper.organic__content-wrapper '
                            '.OrganicForum-Item .OrganicForum-Text'),
                           ('.Organic-ContentWrapper.organic__content-wrapper '
                            '.ExtendedText-Short'),
                           ('.Organic-ContentWrapper.organic__content-wrapper '
                            '.OrganicTextContentSpan'),
                           ]
    domen_classes = ['.Organic .Organic-Subtitle .Organic-Path a.Link.organic__greenurl b',
                     '.Organic .Organic-Subtitle .Organic-Path a.Link.organic__greenurl']
    captcha_class = 'form#checkbox-captcha-form'
    # Different character 'e' unicode
    advertisment_classes = ['span:contains("Реклама")', 'span:contains("Рeклама")']


class YandexSerpCleaner:
    tags = ['script', 'style', 'noframes', 'svg', 'ymaps', 'noscript', 'div[role="complementary"]',
            'nav[aria-labelledby="Pager"]']
    attributes = ['class', 'href', 'data-bem', 'content', 'data-counter', 'data-log-node', 'style', 'data-vnl',
                  'aria-label', 'target', 'data-fast', 'data-cid', 'data-ricg', 'data-wq1l', 'id']
    empty_tags = ['div', 'ul', 'li', 'a']

    @classmethod
    def clean(cls, html):
        content = pq(html)

        for tag in cls.tags:
            content(tag).remove()

        for attribute in cls.attributes:
            elements = content(f'[{attribute}]')
            for element in elements:
                pq_element = content(element)
                pq_element.attr(attribute, '')

        for empty_tag in cls.empty_tags:
            content(f'{empty_tag}:empty').remove()

        return content.html()


class YandexParser(Elements):
    default_snippet_fields = ('p', 'd', 'u', 't', 's')

    def __init__(self, html, snippet_fields=default_snippet_fields, exclude_market_yandex=True,
                 exclude_realty_yandex=True):
        self.html = html
        self.pq = pq(html) if html != '' else None
        self.snippet_fields = snippet_fields
        self.exclude_market_yandex = exclude_market_yandex
        self.exclude_realty_yandex = exclude_realty_yandex

    @property
    def snippets(self):
        return self.snippet_fields

    def _check_url(self, actual_url, expected_urls):
        for expected_url in expected_urls:
            if f'{expected_url}.' in actual_url:
                return True
        return False

    # def _is_advertisement(self, doc_element):
    #     if href := doc_element(self.href_class).attr('href'):
    #         return self._check_url(href, ['yabs.yandex'])
    #
    #     return False

    def _is_advertisement(self, doc_element):
        for advertisment_class in self.advertisment_classes:

            if doc_element(advertisment_class):
                return True

    def _is_yandex_market(self, doc_element):
        return self._get_domen(doc_element) == 'market.yandex.ru'

    def _is_yandex_realty(self, doc_element):
        return self._get_domen(doc_element) in ['realty.yandex.ru', 'realty.ya.ru']

    def is_yandex(self):
        if url := self.pq('meta[property="og:url"]').attr('content'):
            return self._check_url(url, ['yandex', 'ya'])
        return False

    def is_yandex_captcha(self):
        if action := self.pq(self.captcha_class).attr('action'):
            return '/checkcaptcha' in action
        return False

    def _get_description(self, doc_element):
        for description_class in self.description_classes:
            description = doc_element(description_class).text()
            if description:
                return description

    def _get_domen(self, doc_element):
        for domen_class in self.domen_classes:
            domen = doc_element(domen_class).text().split(' ')[0]
            if domen:
                return domen

    def _form_sn_data(self, doc_element, position):
        title = doc_element(self.title_class).text()
        href = doc_element(self.href_class).attr('href')
        description = self._get_description(doc_element)
        domain = self._get_domen(doc_element)

        if not title:
            raise YandexParserError('Title not found')

        if not href:
            raise YandexParserError('Href not found')

        if self._check_url(href, ['yabs.yandex']):
            raise YandexParserError('Adv')

        if not domain:
            raise YandexParserError('Domen not found')

        sn_data = {snippet: None for snippet in self.default_snippet_fields}

        if 'p' in self.snippet_fields:
            sn_data['p'] = position
        if 'd' in self.snippet_fields:
            sn_data['d'] = domain.lower()
        if 'u' in self.snippet_fields:
            sn_data['u'] = href
        if 't' in self.snippet_fields:
            sn_data['t'] = title
        if 's' in self.snippet_fields:
            sn_data['s'] = description

        return sn_data

    def _handle_data(self):
        if not self.html:
            raise YandexParserError('Html is empty')

        if self.is_yandex_captcha():
            raise YandexParserError('Html is captcha')

        if not self.is_yandex():
            raise YandexParserError('Html is not from yandex')

        elements = self.pq(self.elements_class)

        sn = []

        position = 0
        for element in elements:
            doc_element = pq(element)

            if self._is_advertisement(doc_element):
                continue

            if self.exclude_market_yandex and self._is_yandex_market(doc_element):
                continue

            if self.exclude_realty_yandex and self._is_yandex_realty(doc_element):
                continue

            position += 1
            if doc_element := self._form_sn_data(doc_element, position):
                sn.append(doc_element)

        return {'sn': sn, 'pc': None}

    def get_serp(self):
        try:
            return self._handle_data()
        except Exception as ex:
            raise YandexParserError(str(ex))

    def get_clean_html(self):
        return YandexSerpCleaner.clean(self.pq)
