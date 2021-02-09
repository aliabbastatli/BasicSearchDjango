from django.core.management.base import BaseCommand
from core.models import Journal, Author, Category
import random
import datetime

categories = [
    'Sport',
    'Lifestyle',
    'Music',
    'Coding',
    'Travelling',
]

authors = [
    'John', 'Michael', 'Luke', 'Sally', 'Joe', 'Dude', 'Guy', 'Barbara'
]

def generateAuthorName():

    index = random.randint(0,7)
    return authors[index]

def generateCategoryName():
    
    index = random.randint(0,4)

    return categories[index]

def generateViewCount():

    return random.randint(0,100)

def generateIsReviewed():

    val = random.randint(0,1)

    if val == 0:
        return False
    else:
        return True

def generatePublishDate ():
    year = random.randint(2000,2030)
    mounth = random.randint(1,12)
    day = random.randint(1,28)

    return datetime.date(year, mounth, day)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help = 'The txt file that contains the journal titles')
    
    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.txt') as file:
            for row in file:
                title = row
                authorName = generateAuthorName() 
                categoryName = generateCategoryName()
                publishDate = generatePublishDate()
                views = generateViewCount()
                reviewed = generateIsReviewed()

                author = Author.objects.get_or_create(
                    name = authorName
                )

                journal = Journal(
                    title = title,
                    author = Author.objects.get(name=authorName),
                    publishDate = publishDate,
                    views = views,
                    reviewed = reviewed
                )

                journal.save()

                category = Category.objects.get_or_create(name=categoryName)

                journal.categories.add(Category.objects.get(name=categoryName))

        
        self.stdout.write(self.style.SUCCESS('Data imported succesfully'))