import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont

bucket = "hackathonrferl"
photo = "crowded.jpg"
# photo = "scared.jpg"
# photo = "bribe.jpg"
client_rekognition = boto3.client("rekognition")
client_s3 = boto3.resource("s3")

s3_object = client_s3.Object(bucket, photo)
s3_response = s3_object.get()
stream = io.BytesIO(s3_response["Body"].read())


def process_image_rekognition(image):
    response = client_rekognition.detect_labels(Image={"Bytes": image.stream.read()})
    image.stream.seek(0)
    draw = ImageDraw.Draw(image.stream)
    imgWidth, imgHeight = image.size

    for label in response["Labels"]:
        name = label["Name"]
        if len(label["Instances"]) == 0:
            continue
        highset_bbox = label["Instances"][0]
        box = highset_bbox["BoundingBox"]
        left = imgWidth * box["Left"]
        top = imgHeight * box["Top"]
        width = imgWidth * box["Width"]
        height = imgHeight * box["Height"]
        points = (
            (left, top),
            (left + width, top),
            (left + width, top + height),
            (left, top + height),
            (left, top)

        )
        draw.line(points, fill='#00d400', width=2)
        font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)

        draw.text((left + 15, top + 15), name, font=font,
                  fill=(255, 0, 0, 255))  # , font=ImageFont.truetype("font_path123"))
    image.save(output)

# image = Image.open(stream)
# draw = ImageDraw.Draw(image)

# imgWidth, imgHeight = image.size
# # response = client.detect_labels(Image={"S3Object": {"Bucket":"hackathonrferl", "Name": }})
# stream.seek(0)
# response = client_rekognition.detect_labels(Image={"Bytes": stream.read()})

# for label in response["Labels"]:
#     name = label["Name"]
#     if len(label["Instances"]) == 0:
#         continue
#     highset_bbox = label["Instances"][0]
#     box = highset_bbox["BoundingBox"]
#     left = imgWidth * box["Left"]
#     top = imgHeight * box["Top"]
#     width = imgWidth * box["Width"]
#     height = imgHeight * box["Height"]
#     points = (
#         (left, top),
#         (left + width, top),
#         (left + width, top + height),
#         (left, top + height),
#         (left, top)

    # )
    # draw.line(points, fill='#00d400', width=2)
    # font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 15)

    # draw.text((left + 15, top + 15), name, font=font,
    #           fill=(255, 0, 0, 255))  # , font=ImageFont.truetype("font_path123"))

# image.show()
