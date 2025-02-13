from mongoengine import Document, fields


class DigitImage(Document):
    image = fields.ImageField(required=True)
    label = fields.IntField(null=True, blank=True)
    predicted_label = fields.IntField(null=True, blank=True)
    accuracy = fields.FloatField(null=True, blank=True)
    verified = fields.BooleanField(default=False)

    def __str__(self):
        return f'Image {self.id}'
