from faker import Faker


class MyFaker(Faker):
    def __init__(self):
        super().__init__(locale='zh_CN')
        self.model = "自动化测试"

    def phone(self):
        return self.phone_number()

    def mobile(self):
        return self.phone_number()

    def str(self):
        return self.model + self.word()

    def string(self):
        return self.model + self.word() + self.numerify()

    def int(self, *args, **kwargs):
        return self.random_int(*args, **kwargs)

    def int2(self, min=1, max=99):
        return self.random_int(min, max)

    def int3(self, min=1, max=999):
        return self.random_int(min, max)

    def date_time_str(self, start_date="now", end_date="now"):
        return str(self.date_time_between(start_date=start_date, end_date=end_date))[:19]

    def date_str(self, start_date="now", end_date="now"):
        return self.date_time_str(start_date=start_date, end_date=end_date)[:10]


if __name__ == '__main__':
    out = MyFaker()
    print(out.date_str())

