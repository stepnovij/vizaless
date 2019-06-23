import io
import os
# from pdf2image import convert_from_bytes
from upload_file import get_blob, upload_blob
from wand.image import Image


def convert_pdf_to_jpeg(blob):
    pdf = Image(blob=blob)

    pages = len(pdf.sequence)

    image = Image(
        width=pdf.width,
        height=pdf.height * pages
    )

    for i in range(pages):
        image.composite(
            pdf.sequence[i],
            top=pdf.height * i,
            left=0
        )

    return image.make_blob('jpeg')


def convert_image_object_to_bytes_io(bytes_seq):
    bytes_io = io.BytesIO()
    bytes_io.write(bytes_seq)
    bytes_io.seek(0)
    return bytes_io


def convert_pdf_file_from_path_to_image(path):
    all_files = []
    blob = get_blob(path)
    img_obj = convert_pdf_to_jpeg(blob)
    pages = [img_obj]
    # pages = convert_from_bytes(blob, 200)
    file_path = os.path.dirname(path)
    for indx, page in enumerate(pages):
        new_file_path = os.path.join(file_path, '{}.jpeg'.format(str(indx)))
        byte_obj = convert_image_object_to_bytes_io(page)
        upload_blob(new_file_path, byte_obj)
        # page.save(new_file_path, 'JPEG')
        all_files.append(new_file_path)
    return all_files
