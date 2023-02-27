class Flat:
    def __init__(self, link, reference=None, price=None, title=None, description=None, date=None, photos='None'):
        self.link = link
        self.reference = reference
        self.price = price
        self.title = title
        self.description = description
        self.date = date
        self.photos = photos


class FlatInfo(Flat):
    def __init__(self, link, reference=None, price=None, title=None, description=None, date=None, photos='None',
                 floor=None, room=None, apartment_area=None, phone=None, address=None, views=None, preview=None):
        super().__init__(link, reference, price, title, description, date, photos)
        self.floor = floor
        self.room = room
        self.apartment_area = apartment_area
        self.phone = phone
        self.address = address
        self.views = views
        self.preview = preview
