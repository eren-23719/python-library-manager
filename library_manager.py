"""面向对象图书管理系统。"""

import json
from pathlib import Path


class Book:
    """保存单本图书的信息，并负责图书与字典之间的转换。"""

    def __init__(self,title,author,price,isbn,count):
        self.title = title
        self.author = author
        self.price = price
        self.isbn = isbn
        self.count = count

    def book_to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'isbn': self.isbn,
            'count': self.count

        }
    @staticmethod
    def from_dict(book_dict):
        return Book(title = book_dict['title'],
                    author = book_dict['author'],
                    price = book_dict['price'],
                    isbn = book_dict['isbn'],
                    count = book_dict['count']
                    )


class BookManager:
    """管理按 ISBN 索引的图书记录、命令行菜单以及 JSON 读写。"""

    instance = None
    #单例模式（所以对象都相同）
    def __new__(cls,file_path):
        if BookManager.instance is None:
            BookManager.instance = super().__new__(cls)
        return BookManager.instance

    def __init__(self,file_path):
        self.books = {}
        self.file_path = Path(file_path)
        self.__load_from_file()

    def __load_from_file(self):
        if not self.file_path.exists():
            print('文件不存在')
            return

        with open(self.file_path,'r',encoding='utf-8') as f:
             data = json.load(f)

        self.books = {item['isbn']:Book.from_dict(item) for item in data}
        print('图书信息已经加载')


    def showmenu(self):
        while True:
              print('*'*10,'图书管理系统','*'*10)
              print('1.添加图书')
              print('2.删除图书')
              print('3,修改图书信息')
              print('4.根据编号查看图书信息')
              print('5.将图书信息存储到本地')
              print('6.通过页码查看图书列表')
              print('7.输入quit退出系统')
              input_num = input("请输入您的操作编号:")
              if input_num == '7' or input_num == 'quit' :
                  print(f'系统退出')
                  break

              if input_num == '1':
                  self.add_book()
                  continue

              if input_num == '2':
                  self.del_book()
                  continue
              if input_num == '3':
                  self.modify_book()
                  continue
              if input_num == '4':
                  self.check_book()
                  continue
              if input_num == '5':
                  self.save_to_file()
                  continue
              if input_num == '6':
                  self.show_list()
                  continue
              print('非法操作，请继续')


    def add_book(self):
        book_id = input('请输入图书编号:')
        count = int(input('请输入录入数量:'))
        name = input('请输入书名:')
        author = input('请输入作者:')
        price = float(input('请输入价格:'))
        book  = Book(title=name,author=author,price=price,isbn=book_id,count=count)
        self.books[book_id] = book
        print('图书添加成功！！！')

    def __find_book_by_id(self,book_id):
        if book_id not in self.books:
            print('没有找到该图书！')
            return None
        return self.books[book_id]

    def del_book(self):
        book_id = input('请输入要删除的图书编号:')
        book = self.__find_book_by_id(book_id)
        if book is None:
            return
        #有这本书
        del_count = int(input('请输入删除的数量:'))
        if del_count < book.count:
            book.count -= del_count
            print('图书数量删除成功')
            return

        del self.books[book_id]
        print('该图书已经全部删除')

    def check_book(self):
        book_id = input('请输入要查看的图书编号:')
        book = self.__find_book_by_id(book_id)
        if book is None:
            return
        print(f'图书信息:\n书名:{book.title}\n'
              f'作者:{book.author}\n'
              f'价格:{book.price}\n'
              f'编号:{book.isbn}\n'
              f'数量:{book.count}')

    def modify_book(self):
        book_id = input('请输入要修改的图书编号:')
        book = self.__find_book_by_id(book_id)
        if book is None:
            return

        book.title = input('请输入要改成的名字:')
        book.price = float(input('请输入要改成的价格:'))
        book.count = int(input('请输入图书的数量:'))
        book.author =input('请输入图书的作者:')
        print(f'图书信息修改成功')

    def show_list(self):
        if not self.books:
            print('暂无图书信息')
            return

        page = int(input('请输入查看的页码:'))
        page_size = 5
        # 页码从 1 开始，列表下标从 0 开始。
        start = (page - 1) * page_size
        end = start + page_size
        book_list = list(self.books.values())
        page_books = book_list[start:end]
        if not page_books:
            print('该页没有数据')
            return
        for book in page_books:
            print(
                f'编号:{book.isbn} |'
                f'书名:{book.title} |'
                f'作者:{book.author} |'
                f'价格:{book.price} |'
                f'数量:{book.count} |'
            )

    def save_to_file(self):
        data = [book.book_to_dict() for book in self.books.values()]
        with open(self.file_path, 'w', encoding='utf-8') as f:
            # 使用 UTF-8 保存中文，缩进便于直接查看文件。
            json.dump(data, f, ensure_ascii=False, indent=4)
            print('图书信息已保存')


if __name__ == '__main__':
    # 数据文件相对于脚本定位，避免切换运行目录后读错库。
    data_path = Path(__file__).resolve().parent / 'book_datas' / 'books.json'
    m = BookManager(data_path)
    m.showmenu()
