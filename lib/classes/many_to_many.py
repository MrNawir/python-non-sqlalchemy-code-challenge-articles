class Article:
    """
    Represents an article, which serves as the 'join' model between an Author and a Magazine.
    This class holds the relationship data (the title) and references to the related objects.
    """
    all = []  # Class attribute to store all Article instances, acting as a single source of truth.
    
    def __init__(self, author, magazine, title):
        """
        Initializes an Article instance.
        
        Args:
            author (Author): The author who wrote the article.
            magazine (Magazine): The magazine where the article is published.
            title (str): The title of the article.
        """
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)  # Register the new instance in the class-level list.
    
    @property
    def title(self):
        """Returns the title of the article."""
        return self._title
    
    @title.setter
    def title(self, value):
        """
        Sets the title of the article.
        Enforces validation:
        1. Immutable: Cannot be changed once set.
        2. Type check: Must be a string.
        3. Length check: Must be between 5 and 50 characters.
        """
        # Title should be immutable - only set if not already set
        if not hasattr(self, '_title'):
            if isinstance(value, str) and 5 <= len(value) <= 50:
                self._title = value
            else:
                raise Exception("Title must be a string between 5 and 50 characters")
        
class Author:
    """
    Represents an author who creates articles.
    An author has a name and can write multiple articles for various magazines.
    """
    def __init__(self, name):
        """
        Initializes an Author instance.
        
        Args:
            name (str): The name of the author.
        """
        self.name = name

    @property
    def name(self):
        """Returns the name of the author."""
        return self._name
    
    @name.setter
    def name(self, value):
        """
        Sets the name of the author.
        Enforces validation:
        1. Immutable: Cannot be changed once set.
        2. Type check: Must be a string.
        3. Length check: Must be longer than 0 characters.
        """
        # Name should be immutable - only set if not already set
        if not hasattr(self, '_name'):
            if isinstance(value, str) and len(value) > 0:
                self._name = value
            else:
                raise Exception("Name must be a non-empty string")

    def articles(self):
        """
        Returns a list of all articles written by this author.
        Uses a list comprehension to filter the global Article.all list.
        """
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        """
        Returns a unique list of magazines this author has contributed to.
        """
        # Get magazines from the author's articles and use set() to remove duplicates.
        return list(set([article.magazine for article in self.articles()]))

    def add_article(self, magazine, title):
        """
        Creates a new Article associated with this author and the given magazine.
        
        Args:
            magazine (Magazine): The magazine to publish in.
            title (str): The title of the article.
            
        Returns:
            Article: The newly created Article instance.
        """
        return Article(self, magazine, title)

    def topic_areas(self):
        """
        Returns a unique list of category names (topic areas) of magazines the author has contributed to.
        Returns None if the author has no articles.
        """
        if not self.articles():
            return None
        # Extract categories from the magazines and unique them.
        return list(set([article.magazine.category for article in self.articles()]))

class Magazine:
    """
    Represents a magazine that publishes articles.
    A magazine has a name and a category.
    """
    all = []  # Class attribute to store all Magazine instances.
    
    def __init__(self, name, category):
        """
        Initializes a Magazine instance.
        
        Args:
            name (str): The name of the magazine.
            category (str): The category of the magazine.
        """
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        """Returns the name of the magazine."""
        return self._name
    
    @name.setter
    def name(self, value):
        """
        Sets the name of the magazine.
        Enforces validation:
        1. Mutable: Can be changed.
        2. Type check: Must be a string.
        3. Length check: Must be between 2 and 16 characters.
        """
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise Exception("Name must be a string between 2 and 16 characters")
    
    @property
    def category(self):
        """Returns the category of the magazine."""
        return self._category
    
    @category.setter
    def category(self, value):
        """
        Sets the category of the magazine.
        Enforces validation:
        1. Mutable: Can be changed.
        2. Type check: Must be a string.
        3. Length check: Must be longer than 0 characters.
        """
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise Exception("Category must be a non-empty string")

    def articles(self):
        """
        Returns a list of all articles published in this magazine.
        """
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """
        Returns a unique list of authors who have written for this magazine.
        """
        return list(set([article.author for article in self.articles()]))

    def article_titles(self):
        """
        Returns a list of titles of all articles in this magazine.
        Returns None if there are no articles.
        """
        if not self.articles():
            return None
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        """
        Returns a list of authors who have written more than 2 articles for this magazine.
        Returns None if no such authors exist.
        """
        authors = {}
        # Count articles per author for this magazine
        for article in self.articles():
            if article.author in authors:
                authors[article.author] += 1
            else:
                authors[article.author] = 1
        
        # Filter authors with more than 2 articles
        result = [author for author, count in authors.items() if count > 2]
        return result if result else None
    
    @classmethod
    def top_publisher(cls):
        """
        Returns the Magazine instance with the most articles.
        Returns None if there are no articles.
        """
        if not Article.all:
            return None
        
        # Count articles for all magazines
        magazine_counts = {}
        for article in Article.all:
            if article.magazine in magazine_counts:
                magazine_counts[article.magazine] += 1
            else:
                magazine_counts[article.magazine] = 1
        
        if not magazine_counts:
            return None
        
        # Return the magazine with the maximum count
        return max(magazine_counts, key=magazine_counts.get)