def main():
	print("what")

def remove_files():
    data_dir = '/home/ubuntu/yolov5/input_data'
    for f in os.listdir(data_dir):
        os.remove(os.path.join(data_dir, f))

def save_file(s3_bucket,s3_object):
    file_name = s3_object.split('/')[-1]
    boto3.client('s3').download_file(s3_bucket, s3_object, f'{UPLOAD_FOLDER}/{file_name}')

def get_source_target_name():
    UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'
    f = open('/home/ubuntu/yolov5/input_info/names.txt')
    lines = f.read().splitlines()
    f.close()
    s3_object_pdf = lines[1]
    file_name = s3_object_pdf.split('/')[-1]
    return file_name

def download_files():
    UPLOAD_FOLDER = '/home/ubuntu/yolov5/input_data'
    f = open('/home/ubuntu/yolov5/input_info/names.txt') # Open file on read mode
    lines = f.read().splitlines() # List with stripped line-breaks
    f.close() # Close file
    s3_bucket = lines[0]
    s3_object_pdf = lines[1]
    s3_object_img = lines[2]
    save_file(s3_bucket,s3_object_pdf)
    save_file(s3_bucket,s3_object_pdf)


if __name__ == "__main__":
    print(main("target_search.png"))