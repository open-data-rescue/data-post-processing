# Dockerfile
# To run the Python post processing
# 
FROM python:3

# WORKDIR /setup
ADD ./DRAW-post-processing /opt/draw-post-processing
WORKDIR /opt/draw-post-processing

RUN mkdir /opt/draw-post-processing/SEF

# Install the packages that are needed
RUN pip install --no-cache-dir -r requirements.txt

# Run the post process script
CMD [ "python", "./execute_post_process.py" ]
