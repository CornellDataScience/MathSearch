# MathSearch

A next generation search engine for researchers that supports searching with LaTeX math script.


## Run Model
Deployed with aws ec2, ip: 18.207.249.45
Use url as commands to control flask.

Commands:
1. http://18.207.249.45/coord [GET]
Get best matching equation page number and bonding box coordinates.

2. http://18.207.249.45/model?b=$s3_bucket$&o=$s3_object$ [POST]
Post target image and candidate pdf file to ec2.
Inputs: s3_bucket, s3_object without _png or _image postfix
Sample usage: http://18.207.249.45/model?b=mathsearch-intermediary&o=inputs/2dd62a75-0f22-4121-9bb7-22085cfda77f

3. http://18.207.249.45/upload [POST]
Backup option to upload input data to ec2.

4. http://18.207.249.45/run
Run machine learning model