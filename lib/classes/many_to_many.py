class Article:
    all = []
    
    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        # Title should be immutable - only set if not already set
        if not hasattr(self, '_title'):
            if isinstance(value, str) and 5 <= len(value) <= 50:
                self._title = value
            else:
                raise Exception("Title must be a string between 5 and 50 characters")
        
class Author:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        # Name should be immutable - only set if not already set
        if not hasattr(self, '_name'):
            if isinstance(value, str) and len(value) > 0:
                self._name = value
            else:
                raise Exception("Name must be a non-empty string")

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list(set([article.magazine for article in self.articles()]))

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self.articles():
            return None
        return list(set([article.magazine.category for article in self.articles()]))

class Magazine:
    all = []
    
    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise Exception("Name must be a string between 2 and 16 characters")
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise Exception("Category must be a non-empty string")

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set([article.author for article in self.articles()]))

    def article_titles(self):
        if not self.articles():
            return None
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        authors = {}
        for article in self.articles():
            if article.author in authors:
                authors[article.author] += 1
            else:
                authors[article.author] = 1
        
        result = [author for author, count in authors.items() if count > 2]
        return result if result else None
    
    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        
        magazine_counts = {}
        for article in Article.all:
            if article.magazine in magazine_counts:
                magazine_counts[article.magazine] += 1
            else:
                magazine_counts[article.magazine] = 1
        
        if not magazine_counts:
            return None
        
        return max(magazine_counts, key=magazine_counts.get)